import json
import functools
from common import logger
from contextlib import suppress

class Node:

    def __init__(self):
        self.tag = 'text'
        self.type = 'input'
    
    def name(self, content):
        return content['nombre']

    def data(self, field, data):
        return data[field]
    
    def value(self, content, data):
        return data

class Space(Node):

    def __init__(self):
        super().__init__()
        self.tag = 'space'
        self.type = 'static'
    
    def name(self, content):
        return ''
    
    def data(self, field, data):
        return ''

class Table(Node):

    def __init__(self):
        super().__init__()
        self.tag = 'table'

class Canvas(Node):

    def __init__(self):
        super().__init__()
        self.tag = 'canvas'
    
    def value(self, content, data):
        return json.dumps(data)

class Switch(Node):

    def value(self, content, data):
        return 'Si' if data else 'No'

class Select(Node):

    def value(self, content, data):
        options = content['options']
        return list(filter(lambda o: o['value'] == data, options))[0]['label']

class Relacion(Node):

    def data(self, field, data):
        return data['{}Item'.format(field)]
    
    def value(self, content, data):
        return data['label']

class Titulo(Node):

    def __init__(self):
        super().__init__()
        self.tag = 'subtitle'
        self.type = 'static'

    def data(self, field, data):
        return data
    
    def value(self, content, data):
        return ''

class Titulo2(Titulo):

    def __init__(self):
        super().__init__()
        self.tag = 'subtitle2'

def _get_node_type(content):
    NODE_TYPES = {
        'tab': Node,
        'titulo': Titulo,
        'titulo2': Titulo2,
        'space': Space,
        'switch': Switch,
        'select': Select,
        'table': Table,
        'canvas': Canvas,
        'relacion': Relacion,
        'text': Node,
        'date': Node
    }

    if 'tipo' not in content and 'nombre' in content:
        tipo = 'tab'
    elif content['tipo'] in ['textarea', 'number']:
        tipo = 'text'
    else:
        tipo = content['tipo']

    return NODE_TYPES[tipo]

def _is_leaf_content(content):
    return 'tipo' in content and content['tipo'] in [
        'text', 'table', 'number', 'textarea', 'titulo', 'titulo2',
        'switch', 'date', 'select', 'relacion', 'canvas', 'space'
    ]

def _filter_empty_titles(result):
    if len(result) == 0:
        return result

    sin_empty_titles = functools.reduce(_remove_empty_titles, result[1:], [result[0]])
    return _remove_titles_from_end(sin_empty_titles)

def _remove_empty_titles(result, actual):
    result = _remove_consecutive_titles(result, actual['type'], result[-1]['type'])
    result.append(actual)
    return result

def _remove_consecutive_titles(result, actual, anterior):
    while remove_condition(actual, anterior):
        result = result[:-1]
        if len(result) == 0:
            break
        anterior = result[-1]['type']
    
    return result

def _remove_titles_from_end(result):
    last = result[-1]['type']
    while remove_condition(last, last):
        result = result[:-1]
        if len(result) == 0:
            break
        last = result[-1]['type']
    
    return result

def remove_condition(actual, last):
    return (
        (actual == 'subtitle2' and last == 'subtitle2') or
        (actual == 'subtitle' and last == 'subtitle2') or
        (actual == 'subtitle' and last == 'subtitle') or
        (actual == 'title' and last == 'subtitle2') or
        (actual == 'title' and last == 'subtitle') or
        (actual == 'title' and last == 'title')
    )

def _valor_campo_diagnostico(data):
    return data['label']

def _valor_diagnostico(data):
    if data:
        return '{} - {}'.format(data['codigo'], data['nombre'])

    return None

def _diagnostico_consulta(data):
    result = [
        # {'type': 'text', 'label': 'Finalidad de la consulta', 'value': _valor_campo_diagnostico(data['finalidadItem'])},
        # {'type': 'text', 'label': 'Causa externa', 'value': _valor_campo_diagnostico(data['causaExternaItem'])},
        # {'type': 'text', 'label': 'Tipo de diagnostico principal', 'value': _valor_campo_diagnostico(data['tipoDiagnosticoItem'])},
        {'type': 'text', 'label': 'Diagnóstico principal', 'value': _valor_diagnostico(data['diagnosticoPrincipalItem'])},
    ]

    if data.get('diagnostico1Item', None):
        result.append({'type': 'text', 'label': 'Diagnóstico relacionado 1', 'value': _valor_diagnostico(data['diagnostico1Item'])},)
    if data.get('diagnostico2Item', None):
        result.append({'type': 'text', 'label': 'Diagnóstico relacionado 2', 'value': _valor_diagnostico(data['diagnostico2Item'])},)
    if data.get('diagnostico3Item', None):
        result.append({'type': 'text', 'label': 'Diagnóstico relacionado 3', 'value': _valor_diagnostico(data['diagnostico3Item'])},)
    
    return result

def _diagnostico_procedimiento(data):
    result = [
        # {'type': 'text', 'label': 'Ambito de realización del procedimiento', 'value': _valor_campo_diagnostico(data['ambitoItem'])},
        # {'type': 'text', 'label': 'Finalidad del procedimiento', 'value': _valor_campo_diagnostico(data['finalidadItem'])},
        # {'type': 'text', 'label': 'Personal que atiende', 'value': _valor_campo_diagnostico(data['personalAtiendeItem'])},
        # {'type': 'text', 'label': 'Forma de realización del acto quirúrgico', 'value': _valor_campo_diagnostico(data['formaActoQuirurgicoItem'])},
        # {'type': 'text', 'label': 'Diagnóstico principal', 'value': _valor_diagnostico(data['diagnosticoPrincipalItem'])},
    ]

    if data.get('diagnosticoPrincipalItem', None):
        result.append({'type': 'text', 'label': 'Diagnóstico principal', 'value': _valor_diagnostico(data['diagnosticoPrincipalItem'])})
    if data.get('diagnosticoRelacionadoItem', None):
        result.append({'type': 'text', 'label': 'Diagnóstico relacionado', 'value': _valor_diagnostico(data['diagnosticoRelacionadoItem'])},)
    if data.get('complicacionItem', None):
        result.append({'type': 'text', 'label': 'Complicación', 'value': _valor_diagnostico(data['complicacionItem'])},)
    
    return result

def flatten_diagnostico(tipo, data):
    result = [{'type': 'title', 'label': 'Diagnóstico'}]
    if tipo == 'consulta':
        result.extend(_diagnostico_consulta(data))
    elif tipo == 'procedimiento':
        result.extend(_diagnostico_procedimiento(data))
    
    return result

def flatten_medical_record(content, data, diagnostico=False, servicio=None):
    result = _recursive_flattened(content, data, [])
    if diagnostico:
        with suppress(Exception):
            result.extend(flatten_diagnostico(servicio.tipo_rips, data['rips']))
    return _filter_empty_titles(result)

def _recursive_flattened(content, data, result):
    if _is_leaf_content(content):
        result.append(_flattened_leaf_field(content, data))
        return result

    is_tab = _is_tab(content)
    if is_tab:
        result.append(_flattened_value('title', content['nombre']))

    order, fields = _get_order_fields_from_non_leaf_nodes(content)

    for field in order:
        field_content = fields[field]
        node_field = _get_node_type(field_content)()
        if node_field.type == 'static' or (field in data and data[field]):
            field_data = node_field.data(field, data)
            _recursive_flattened(field_content, field_data, result)

    return result

def _get_order_fields_from_non_leaf_nodes(content):
    if _is_tab(content):
        return content['fields']['order'], content['fields']

    return content['order'], content

def _is_tab(content):
    return 'nombre' in content

def _flattened_leaf_field(content, data):
    params = {
        'tipo': _get_field_type(content),
        'label': _get_field_name(content),
        'value': _get_field_value(content, data)
    }

    if _get_field_type(content) == 'canvas':
        params['image'] = content['image']

    return _flattened_value(**params)

def _flattened_value(tipo, label, value=None, **kwargs):
    result = {'type': tipo}

    if value:
        result.update({'value': value})

    if label:
        result.update({'label': label})

    result.update(kwargs)

    return result

def _get_field_type(content):
    return _get_node_type(content)().tag

def _get_field_value(content, data):
    return _get_node_type(content)().value(content, data)

def _get_field_name(content):
    return _get_node_type(content)().name(content)
