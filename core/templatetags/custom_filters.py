from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(str(key))

@register.filter
def filter_by_id(items, item_id):
    return [item for item in items if str(item.id) == str(item_id)]