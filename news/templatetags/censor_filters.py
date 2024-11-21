from django import template

register = template.Library()

@register.filter(name='censor')
def censor(value):
    censored_words = ['редиска', 'тыква']
    for word in censored_words:
        value = value.replace(word, '*' * len(word))
    return value
