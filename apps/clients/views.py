# apps/clients/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .serializers import CrearUsuarioSerializer, ClienteSerializer
from rest_framework import viewsets, permissions
from .models import Cliente
#librerias de google
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions    import AllowAny
from rest_framework.response      import Response
from rest_framework               import status
from django.conf                  import settings
from django.contrib.auth          import get_user_model
from google.oauth2                import id_token
from google.auth.transport       import requests as google_requests
from rest_framework_simplejwt.tokens import RefreshToken
from .models                      import Cliente
import datetime
from google.auth.transport import requests as google_requests

@api_view(['POST'])
@permission_classes([AllowAny])
def crear_usuario(request):
    """
    POST /api/clients/crear-usuario/
    {
      "username": "...",
      "email": "...",
      "password": "..."
    }
    """
    serializer = CrearUsuarioSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({'id': user.id_usuario}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ClienteViewSet(viewsets.ModelViewSet):
    """
    CRUD completo sobre clientes.
    """
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    
    
    
User = get_user_model()

@api_view(['POST'])
@permission_classes([AllowAny])
def google_login(request):
    """
    POST /api/clients/google-login/
    { "id_token": "<token obtenido en front-end>" }
    """
    token = request.data.get('id_token')
    if not token:
        return Response({'detail': 'id_token es requerido'},
                        status=status.HTTP_400_BAD_REQUEST)

    # 1) Verificar token con la librería de Google
    try:
        idinfo = id_token.verify_oauth2_token(
            token,
            google_requests.Request(),
            settings.GOOGLE_OAUTH2_CLIENT_ID
        )
    except ValueError:
        return Response({'detail': 'Token inválido'},
                        status=status.HTTP_400_BAD_REQUEST)

    # 2) Extraer información básica
    email       = idinfo.get('email')
    given_name  = idinfo.get('given_name', '')
    family_name = idinfo.get('family_name', '')

    # 3) Buscar o crear el Usuario
    user, created = User.objects.get_or_create(
        email=email,
        defaults={'username': email.split('@')[0]}
    )

    if created:
        # Deshabilitar login con contraseña
        user.set_unusable_password()
        user.save()
        # 4) Crear perfil Cliente mínimo (tu modelo Cliente exige campos obligatorios) :contentReference[oaicite:0]{index=0}
        cliente = Cliente.objects.create(
            nombres          = given_name or ' ',
            apellidos        = family_name or ' ',
            ci               = '',
            sexo             = '',
            fecha_nacimiento = datetime.date.today(),  # placeholder, luego actualizas
            telefono         = ''
        )
        user.cliente = cliente
        user.save()

    # 5) Emitir tokens JWT con Simple JWT
    refresh = RefreshToken.for_user(user)
    return Response({
        'access':  str(refresh.access_token),
        'refresh': str(refresh),
    }, status=status.HTTP_200_OK)    
    
    



