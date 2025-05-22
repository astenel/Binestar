# apps/clients/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import crear_usuario
from .views import crear_usuario, ClienteViewSet, google_login
# Si luego creas un ClienteViewSet, regístralo aquí:
# from .views import ClienteViewSet
# router = DefaultRouter()
# router.register(r'clientes', ClienteViewSet, basename='clientes')
router = DefaultRouter()
router.register(r'clientes', ClienteViewSet, basename='clientes')

urlpatterns = [
    path('crear-usuario/', crear_usuario, name='crear_usuario'),
    path('google-login/',    google_login,    name='google_login'),
    path('', include(router.urls)),
]
