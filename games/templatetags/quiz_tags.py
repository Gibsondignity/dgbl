from django import template
register = template.Library()

@register.filter
def get_option(quiz, option_letter):
    return getattr(quiz, f'option_{option_letter.lower()}')
