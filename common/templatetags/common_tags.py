from django import template
from num2words import num2words
from rest_framework.renderers import JSONRenderer

register = template.Library()

@register.filter
def to_json(campo):
    """
    :returns:
        Un json con las opciones del campo dentro de un array.
    
    :param campo:
        El campo al cual se le van a serializar las opciones.
    """

    json = []
    for option in campo.iter_options():
        json.append({'value': option.value, 'label': option.display_text})
    
    return JSONRenderer().render(json)


@register.filter
def to_words(value):
    """Converts to words the number."""

    return num2words(value, to='currency', lang='es_CO')
