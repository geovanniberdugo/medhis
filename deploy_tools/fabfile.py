import random
from contextlib import contextmanager
from fabric.contrib.files import append, sed
from fabric.api import env, task, run, sudo, cd, prefix, local

REPO_URL = 'git@bitbucket.org:ingeniarte/medhis.git'
PROJECT = 'dasalud'  # nombre de carpeta donde esta wsgi 
# O
# CREATE DATABASE db;
# CREATE USER user WITH PASSWORD 'pass';
# GRANT ALL PRIVILEGES ON DATABASE db TO user;
# psql -U medhis -h localhost medhis < ~/Desktop/staging_tenant.sql
# pg_dump -U medhis -h localhost --inserts medhis_staging > bk_hoy.sql
# rsync -nrv --exclude=.DS_Store . ingeniarte@staging.siiom.net:/home/ingeniarte2/sites/ingeniarte.siiom.net/media/cdr.siiom.net/
# sudo certbot certonly --cert-name staging.medhis.net --webroot -w /home/ingeniarte2/sites/staging.medhis.net -d staging.medhis.net -d umri.staging.medhis.net -d unigastro.staging.medhis.net
# sudo certbot certonly --cert-name ingeniarte.medhis.net --webroot -w /home/ingeniarte2/sites/ingeniarte.medhis.net -d ingeniarte.medhis.net -d umri.medhis.net
# /home/ingeniarte2/sites/ingeniarte.medhis.net/src/static/bower_components
# /home/ingeniarte2/sites/ingeniarte.medhis.net/bcks/2020-01-042.backup.gz
# sites/ingeniarte.medhis.net/media/
# rsync -rv ingeniarte2@50.116.33.180:/home/ingeniarte2/sites/ingeniarte.medhis.net/media .
# rsync -rv ingeniarte2@69.164.215.168:/home/ingeniarte2/

ENVIROMENT_SETTINGS = {
    'production': {
        'site': 'ingeniarte.medhis.net',
        'branch': 'master',
        # 'branch': 'feature/errores-rips',
        'allowed_host': '.medhis.net'
    },
    'staging': {
        'site': 'staging.medhis.net',
        'branch': 'develop',
        'allowed_host': '.staging.medhis.net'
    }
}

def site_dir():
    global SITE_FOLDER, PROJECT_ROOT, ENV_FILE
    env.site = env.settings['site']
    SITE_FOLDER = '/home/{user}/sites/{site}'.format(user=env.user, site=env.site)
    PROJECT_ROOT = '{}/src'.format(SITE_FOLDER)
    ENV_FILE = '/home/{user}/.envs/{site}/bin/postactivate'.format(user=env.user, site=env.site)


@contextmanager
def virtualenv():
    with prefix('workon {}'.format(env.site)):
        yield


def create_secret_key():
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
    return key


def get_database_url():
    """Constructs the db url from user input."""
    import getpass

    name = input('Nombre de la base de datos: ')
    username = input('Usuario de la base de datos: ')
    password = getpass.getpass()

    database_url = '{}:{}@127.0.0.1:5432/{}'.format(username, password, name)
    return database_url


def set_env_variables():
    """Sets the enviroment variables."""

    append(ENV_FILE, 'export DATABASE_URL=//{}'.format(get_database_url()))
    append(ENV_FILE, "export SECRET_KEY='{}'".format(create_secret_key()))
    append(ENV_FILE, 'export DJANGO_SETTINGS_MODULE={}.settings.production'.format(PROJECT))
    append(ENV_FILE, 'export ALLOWED_HOSTS={}'.format(env.settings['allowed_host']))
    append(ENV_FILE, 'export ANALYTICS=True')

  
def update_source():
    commit = local('git rev-parse origin/{}'.format(env.settings['branch']), capture=True)

    with virtualenv():
        run('git fetch')
        run('git reset --hard {}'.format(commit))


def config_gunicorn():
    file_ = 'gunicorn_start'
    with cd('{}/bin'.format(SITE_FOLDER)):
        sudo('cp {}/deploy_tools/gunicorn.template.conf {}'.format(PROJECT_ROOT, file_))
        sed(file_, 'PROJECT_ROOT', PROJECT_ROOT)
        sed(file_, 'SITE_FOLDER', SITE_FOLDER)
        sed(file_, 'SITENAME', env.site)
        sed(file_, 'USER', env.user)

        run('chmod u+x {}'.format(file_))


def config_services():
    CONFIG_FILES = {
        'supervisor': 'conf.d/{}.conf'.format(env.site),
        'nginx': 'sites-available/{}.conf'.format(env.site)
    }

    for service in ('nginx', 'supervisor'):
        with cd('/etc/{}/'.format(service)):
            sudo('cp {}/deploy_tools/{}.template.conf {}'.format(PROJECT_ROOT, service, CONFIG_FILES[service]))
            sed(CONFIG_FILES[service], 'HOSTNAME', env.settings['allowed_host'], use_sudo=True, shell=True)
            sed(CONFIG_FILES[service], 'PROJECT_ROOT', PROJECT_ROOT, use_sudo=True, shell=True)
            sed(CONFIG_FILES[service], 'SITE_FOLDER', SITE_FOLDER, use_sudo=True, shell=True)
            sed(CONFIG_FILES[service], 'SITENAME', env.site, use_sudo=True, shell=True)
            sed(CONFIG_FILES[service], 'USER', env.user, use_sudo=True, shell=True)

    sudo('ln -s {nginx}/{} {nginx}/sites-enabled'.format(CONFIG_FILES['nginx'], env.site, nginx='/etc/nginx'))
    config_gunicorn()


@task
def staging():
    """Setting staging enviroment."""

    env.user = 'ingeniarte2'
    env.hosts = ['69.164.215.168']
    env.settings = ENVIROMENT_SETTINGS['staging']

    site_dir()


@task
def production():
    """Setting production enviroment."""

    env.user = 'ingeniarte2'
    env.hosts = ['69.164.215.168']
    env.settings = ENVIROMENT_SETTINGS['production']

    site_dir()


@task
def provision():
    """Provision a new site on an already provision server."""

    for subfolder in ('static', 'media', 'src', 'bin', 'tmp/sockets', 'tmp/logs'):
        run("mkdir -p {}/{}".format(SITE_FOLDER, subfolder))

    run('git clone {} {}'.format(REPO_URL, PROJECT_ROOT))

    #  Create virtualenv
    run('mkvirtualenv {}'.format(env.site))
    with cd(PROJECT_ROOT):
        with virtualenv():
            run('setvirtualenvproject')

    set_env_variables()
    update_source()
    with virtualenv():
        run('pip install -r requirements/production.txt')
        # run('bower install')
        run('./manage.py check')
        run('./manage.py migrate_schemas --shared')
        run('./manage.py collectstatic --noinput')

    config_services()

    sudo('systemctl reload nginx')
    sudo('supervisorctl reread')
    sudo('supervisorctl update')


@task
def deploy():
    """Deploy new changes to the server."""

    update_source()
    local('cd ../static && npm run prod')
    local('rsync -rv ../static/build ingeniarte2@69.164.215.168:{}/static/'.format(PROJECT_ROOT))
    with virtualenv():
        run('pip install -r requirements/production.txt')
        # run('bower install')
        run('./manage.py migrate_schemas')
        run('./manage.py collectstatic --noinput')

    restart_server()

@task
def set_env_var():
    """Creates an enviroment variable."""

    key = input('Nombre de la variable de entorno: ')
    value = input('Valor: ')

    append(ENV_FILE, 'export {key}={value}'.format(key=key, value=value))

@task
def restart_server():
    sudo('supervisorctl restart {}'.format(env.site))
    sudo('supervisorctl status {}'.format(env.site))
