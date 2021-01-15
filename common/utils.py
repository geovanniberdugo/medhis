import json
from collections import deque
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import HtmlFormatter
from django.utils.safestring import mark_safe
from graphql.language.ast import FragmentSpread, InlineFragment


def in_query(value, info):
    """Indica si value esta definido en el query."""

    fields = deque(info.field_asts[0].selection_set.selections)
    exists = False
    while len(fields) > 0 and not exists:
        field = fields.popleft()
        exists = value == field.name.value

        if isinstance(field, FragmentSpread) and info.fragments:
            fields.extend(info.fragments[field.name.value].selection_set.selections)
        elif getattr(field, "selection_set", None):
            fields.extend(field.selection_set.selections)
    return exists

def prettified_json_data(data):
    """Prettified json field data."""

    # Convert the data to sorted, indented JSON
    response = json.dumps(data, sort_keys=True, indent=2)
    # Get the Pygments formatter
    formatter = HtmlFormatter(style='colorful')
    # Highlight the data
    response = highlight(response, JsonLexer(), formatter)
    # Get the stylesheet
    style = "<style>" + formatter.get_style_defs() + "</style><br>"
    # Safe the output
    return mark_safe(style + response)

