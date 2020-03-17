from django import template

register = template.Library()

def bold(text):
    return text.replace('**','<strong>',1).replace('**','</strong>',1)

register.filter('bold', bold)
