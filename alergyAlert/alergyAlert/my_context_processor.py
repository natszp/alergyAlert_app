from datetime import time

import django


def my_cp(request):
    context = {
        'now' : django.utils.timezone.localtime(),
        'version': '1.0',
        'by': 'natszp'
    }
    return context
