from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken
from django.apps import apps

class CustomJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        header = request.headers.get('Authorization')
        if not header or not header.startswith('Bearer '):
            return None

        try:
            token_str = header.split()[1]
            token = AccessToken(token_str)
            user_id = token.get('user_id') 
        except Exception:
            raise AuthenticationFailed('Token inválido')

        Usuario = apps.get_model('FonoAppAdministracion', 'FonoApp_Administracion')
        try:
            usuario = Usuario.objects.get(id_usuario=user_id)
            if not usuario.estado:
                raise AuthenticationFailed('Usuario inactivo')
        except Usuario.DoesNotExist:
            raise AuthenticationFailed('Usuario no encontrado')

        return (usuario, token)