from .models import InformacionAlbergue

def info_albergue(request):
    return {
        'info_albergue': InformacionAlbergue.objects.first()
    }
