module.exports = {
    client: {
        includes: ['./static/**/*.js'],
        excludes: ['./static/build/**/*', './static/bower_components/**/*', './static/node_modules/**/*'],
        service: {
            name: 'taniamhn-medhis',
            localSchemaFile: './schema.json',
        },
    },
};