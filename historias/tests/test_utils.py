import pytest
from django.test import SimpleTestCase, tag
from ..utils import flatten_medical_record, _filter_empty_titles

def test_flatten_medical_record_return_correct_result():
    content = {
        'order': ['tab'],
        'tab': {
            'nombre': 'tab',
            'fields': {
                'order': [
                    'titulo',
                    'titulo2',
                    'text',
                    'textarea',
                    'number',
                    'space',
                    'switch',
                    'relacion',
                    'select',
                    'canvas',
                    'date'
                ],
                'titulo': {'tipo': 'titulo', 'nombre': 'titulo'},
                'titulo2': {'tipo': 'titulo2', 'nombre': 'titulo 2'},
                'text': {'tipo': 'text', 'nombre': 'text'},
                'textarea': {'tipo': 'textarea', 'nombre': 'textarea'},
                'number': {'tipo': 'number', 'nombre': 'number'},
                'space': {'tipo': 'space'},
                'switch': {'tipo': 'switch', 'nombre': 'switch'},
                'relacion': {'nombre': 'relacion', 'tipo': 'relacion', 'url': '/globales/cies/?search'},
                'select': {'tipo': 'select', 'nombre': 'select', 'options': [{'value': 1, 'label': 'Bueno'}]},
                'canvas': {
                    'helpText': '',
                    'image': '/static/img/cuerpo-frontal.png',
                    'nombre': 'canvas',
                    'tipo': 'canvas'
                },
                'date': {
                    'tipo': 'date',
                    'nombre': 'date'
                },
            }
        }
    }

    data = {
        'tab': {
            'text': 'text',
            'textarea': 'textarea',
            'number': 'number',
            'switch': True,
            'relacion': 1,
            'relacionItem': {
                'codigo': 'A021',
                'label': 'A021 - SEPTICEMIA DEBIDA A SALMONELLA',
                'nombre': 'SEPTICEMIA DEBIDA A SALMONELLA',
                'value': 1
            },
            'select': 1,
            'canvas': [{'a': 1}],
            'date': '2019-10-20'
        }
    }

    expected = [
        {'type': 'title', 'label': 'tab'},
        {'type': 'subtitle', 'label': 'titulo'},
        {'type': 'subtitle2', 'label': 'titulo 2'},
        {'type': 'text', 'label': 'text', 'value': 'text'},
        {'type': 'text', 'label': 'textarea', 'value': 'textarea'},
        {'type': 'text', 'label': 'number', 'value': 'number'},
        {'type': 'space'},
        {'type': 'text', 'label': 'switch', 'value': 'Si'},
        {'type': 'text', 'label': 'relacion', 'value': 'A021 - SEPTICEMIA DEBIDA A SALMONELLA'},
        {'type': 'text', 'label': 'select', 'value': 'Bueno'},
        {'type': 'canvas', 'label': 'canvas', 'image': '/static/img/cuerpo-frontal.png', 'value': '[{"a": 1}]'},
        {'type': 'text', 'label': 'date', 'value': '2019-10-20'}
    ]

    result = flatten_medical_record(content, data)
    assert result == expected

def test_flatten_medical_record_not_add_empty_field():
    content = {
        'order': ['tab'],
        'tab': {
            'nombre': 'tab',
            'fields': {
                'order': [
                    'titulo',
                    'titulo2',
                    'text',
                    'textarea',
                    'number'
                ],
                'titulo': {'tipo': 'titulo', 'nombre': 'titulo'},
                'titulo2': {'tipo': 'titulo2', 'nombre': 'titulo 2'},
                'text': {'tipo': 'text', 'nombre': 'text'},
                'textarea': {'tipo': 'textarea', 'nombre': 'textarea'},
                'number': {'tipo': 'number', 'nombre': 'number'}
            }
        }
    }

    data = {
        'tab': {
            'text': 'text',
            'number': 'number'
        }
    }

    expected = [
        {'type': 'title', 'label': 'tab'},
        {'type': 'subtitle', 'label': 'titulo'},
        {'type': 'subtitle2', 'label': 'titulo 2'},
        {'type': 'text', 'label': 'text', 'value': 'text'},
        {'type': 'text', 'label': 'number', 'value': 'number'}
    ]

    result = flatten_medical_record(content, data)
    assert result == expected

def test_flatten_medical_record_not_add_empty_tab():
    content = {
        'order': ['tab'],
        'tab': {
            'nombre': 'tab',
            'fields': {
                'order': [
                    'text',
                    'number'
                ],
                'text': {'tipo': 'text', 'nombre': 'text'},
                'number': {'tipo': 'number', 'nombre': 'number'}
            }
        },
        'tab2': {
            'nombre': 'tab 2',
            'fields': {
                'order': [
                    'text',
                ],
                'text': {'tipo': 'text', 'nombre': 'text'},
            }
        }
    }

    data = {
        'tab': {
            'text': 'text',
            'number': 'number'
        }
    }

    expected = [
        {'type': 'title', 'label': 'tab'},
        {'type': 'text', 'label': 'text', 'value': 'text'},
        {'type': 'text', 'label': 'number', 'value': 'number'}
    ]

    result = flatten_medical_record(content, data)
    assert result == expected

def test_flatten_medical_record_not_add_empty_tab():
    content = {
        'order': ['tab', 'tab2', 'tab3'],
        'tab': {
            'nombre': 'tab',
            'fields': {
                'order': [
                    'number'
                ],
                'number': {'tipo': 'number', 'nombre': 'number'}
            }
        },
        'tab2': {
            'nombre': 'tab 2',
            'fields': {
                'order': [
                    'number'
                ],
                'number': {'tipo': 'number', 'nombre': 'number'}
            }
        },
        'tab3': {
            'nombre': 'tab 3',
            'fields': {
                'order': [
                    'number'
                ],
                'number': {'tipo': 'number', 'nombre': 'number'}
            }
        },
    }

    data = {
        'tab2': {
            'number': 'number'
        }
    }

    expected = [
        {'type': 'title', 'label': 'tab 2'},
        {'type': 'text', 'label': 'number', 'value': 'number'}
    ]

    result = flatten_medical_record(content, data)
    assert result == expected

def test_flatten_medical_record_not_add_empty_titles():
    content = {
        'order': ['tab'],
        'tab': {
            'nombre': 'tab',
            'fields': {
                'order': [
                    'textarea',
                    'title',
                    'number',
                    'title2',
                    'number2',
                    'subtitle',
                    'text',
                    'subtitle2',
                    'text2',
                    'title3',
                    'subtitle3',
                    'text3',
                    'title4',
                    'text4',
                    'title5',
                    'subtitle5',
                    'text5'
                ],
                'textarea': {'tipo': 'text', 'nombre': 'textarea'},
                'title': {'tipo': 'titulo', 'nombre': 'titulo'},
                'number': {'tipo': 'number', 'nombre': 'number'},
                'title2': {'tipo': 'titulo', 'nombre': 'titulo2'},
                'number2': {'tipo': 'number', 'nombre': 'number2'},
                'subtitle': {'tipo': 'titulo2', 'nombre': 'subtitle'},
                'text': {'tipo': 'text', 'nombre': 'text'},
                'subtitle2': {'tipo': 'titulo2', 'nombre': 'subtitle2'},
                'text2': {'tipo': 'text', 'nombre': 'text2'},
                'title3': {'tipo': 'titulo', 'nombre': 'titulo3'},
                'subtitle3': {'tipo': 'titulo2', 'nombre': 'subtitle3'},
                'text3': {'tipo': 'number', 'nombre': 'text3'},
                'title4': {'tipo': 'titulo', 'nombre': 'titulo4'},
                'text4': {'tipo': 'number', 'nombre': 'text4'},
                'title5': {'tipo': 'titulo', 'nombre': 'titulo5'},
                'subtitle5': {'tipo': 'titulo2', 'nombre': 'subtitle5'},
                'text5': {'tipo': 'number', 'nombre': 'text5'}
            }
        },
    }

    data = {
        'tab': {
            'textarea': 'textarea',
            'number2': 'number2',
            'text2': 'text2',
            'text4': 'text4',
        }
    }

    expected = [
        {'type': 'title', 'label': 'tab'},
        {'type': 'text', 'label': 'textarea', 'value': 'textarea'},
        {'type': 'subtitle', 'label': 'titulo2'},
        {'type': 'text', 'label': 'number2', 'value': 'number2'},
        {'type': 'subtitle2', 'label': 'subtitle2'},
        {'type': 'text', 'label': 'text2', 'value': 'text2'},
        {'type': 'subtitle', 'label': 'titulo4'},
        {'type': 'text', 'label': 'text4', 'value': 'text4'}
    ]

    result = flatten_medical_record(content, data)
    assert result == expected

def test_remove_empty_titles_when_first_should_be_removed():
    result = [
        {'label': 'valoración final', 'type': 'title'},
        {'label': 'Evolución', 'type': 'title'},
        {'type': 'text', 'value': 'Realiza estiramiento de flexo extensores de codo'},
        {'label': 'Diagnóstico', 'type': 'title'},
        {'label': 'Diagnóstico principal', 'type': 'text', 'value': 'M771 - EPICONDILITIS LATERAL'}
    ]

    expected = [
        {'label': 'Evolución', 'type': 'title'},
        {'type': 'text', 'value': 'Realiza estiramiento de flexo extensores de codo'},
        {'label': 'Diagnóstico', 'type': 'title'},
        {'label': 'Diagnóstico principal', 'type': 'text', 'value': 'M771 - EPICONDILITIS LATERAL'}
    ]

    assert _filter_empty_titles(result) == expected

def test_remove_empty_titles_return_empty_list():
    result = [
        {'label': 'Solicitud', 'type': 'title'},
        {'label': 'Tipo de documento solicitado', 'type': 'subtitle'},
        {'label': 'Servicio recibido', 'type': 'subtitle'}
    ]

    expected = []

    assert _filter_empty_titles(result) == expected
