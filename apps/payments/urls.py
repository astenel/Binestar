from django.urls import path
from django.http import JsonResponse

def ping(request):
    return JsonResponse({'status': 'clients ok'})

urlpatterns = [
    # ruta de prueba
    path('ping/', ping, name='clients-ping'),
]
