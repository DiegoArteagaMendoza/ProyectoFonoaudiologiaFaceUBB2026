from django.urls import path
from FonoAppAdministracion import views

urlpatterns = [
    # -------------------------------------------------------------------------
    # MÉTODO: POST
    # URL: /api/usuarios/crear/ (o el prefijo que uses)
    # HEADERS: Ninguno (acceso libre / AllowAny)
    # BODY (JSON): 
    # {
    #   "nombre": "Juan Pérez",
    #   "rut": "12345678-9",
    #   "email": "juan@ejemplo.com",
    #   "password": "mi_clave_secreta",
    #   "tipo": false,  # 0=vet, 1=indep
    #   "estado": true,
    #   "is_staff": false
    # }
    # -------------------------------------------------------------------------
    path('crear/', views.usuarios_create, name='usuarios-create'),

    # -------------------------------------------------------------------------
    # MÉTODO: GET
    # URL: /api/usuarios/listar/
    # HEADERS: { "Authorization": "Bearer <tu_access_token>" }
    # BODY: Ninguno
    # USO: Retorna una lista JSON con todos los usuarios que tengan estado=True.
    # -------------------------------------------------------------------------
    path('listar/', views.usuarios_list, name='usuarios-list'),

    # -------------------------------------------------------------------------
    # MÉTODO: POST
    # URL: /api/usuarios/login/
    # HEADERS: Ninguno (acceso libre / AllowAny)
    # BODY (JSON): 
    # {
    #   "correo": "juan@ejemplo.com",
    #   "password": "mi_clave_secreta"
    # }
    # USO: Retorna los tokens JWT ('access' y 'refresh') y los datos básicos del usuario.
    # -------------------------------------------------------------------------
    path('login/', views.login_view, name='login'),

    # -------------------------------------------------------------------------
    # MÉTODO: GET
    # URL: /api/usuarios/me/
    # HEADERS: { "Authorization": "Bearer <tu_access_token>" }
    # BODY: Ninguno
    # USO: Retorna todos los datos serializados del usuario dueño del token enviado.
    # -------------------------------------------------------------------------
    path('me/', views.usuario_perfil, name='usuario-perfil'),
    
    # -------------------------------------------------------------------------
    # MÉTODO: DELETE
    # URL: /api/usuarios/12345678-9/eliminar/
    # HEADERS: { "Authorization": "Bearer <tu_access_token>" }
    # BODY: Ninguno
    # USO: Desactiva a un usuario cambiando su estado a False (borrado lógico).
    # -------------------------------------------------------------------------
    path('<str:rut>/eliminar/', views.usuario_eliminar, name='usuario-eliminar'),

    # -------------------------------------------------------------------------
    # MÉTODO: PUT
    # URL: /api/usuarios/12345678-9/actualizar-password/
    # HEADERS: { "Authorization": "Bearer <tu_access_token>" }
    # BODY (JSON):
    # {
    #   "password": "mi_nueva_clave_secreta"
    # }
    # USO: Busca al usuario por su RUT y actualiza su contraseña de forma segura.
    # -------------------------------------------------------------------------
    path('<str:rut>/actualizar-password/', views.usuario_actualizar_password, name='usuario-actualizar-password'),
]