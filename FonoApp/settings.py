import os
from pathlib import Path
import dj_database_url
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

# ==========================================
# 1. SEGURIDAD Y ENTORNO
# ==========================================
# Lee la variable desde el servidor, o usa tu clave local por defecto
SECRET_KEY = os.environ.get(
    'SECRET_KEY', 
    'django-insecure-)dj+y&$f2+q)elr0c!&k2fo^*^y+l$p*&l+civ#k3)fx959a0%'
)

# Render pasará DEBUG=False, en local seguirá siendo True
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# Render asignará los hosts permitidos (ej. tu-app.onrender.com), en local permite vacío/localhost
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')


# ==========================================
# 2. APLICACIONES
# ==========================================
DEV_APPS = [
    'FonoAppAdministracion',
    'FonoAppCuidados',
    'FonoAppDiagnostico',
    'FonoAppInformacion',
    'FonoAppNoticias',
]

BASE_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    # whitenoise debe ir antes de staticfiles si se usa la integración de runserver (opcional pero recomendado)
    'whitenoise.runserver_nostatic', 
    'django.contrib.staticfiles',
]

FRAMEWORKS = [
    'rest_framework',
    'corsheaders',
    'rest_framework_simplejwt'
]

INSTALLED_APPS = DEV_APPS + BASE_APPS + FRAMEWORKS


# ==========================================
# 3. MIDDLEWARE
# ==========================================
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Añadido para servir estáticos en Render
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Configuración de CORS dinámica
# En Render añadirás: CORS_ALLOWED_ORIGINS=https://tu-app-angular.vercel.app
CORS_ALLOWED_ORIGINS = os.environ.get(
    'CORS_ALLOWED_ORIGINS', 
    'http://localhost:4200'
).split(',')

ROOT_URLCONF = 'FonoApp.urls'


# ==========================================
# 4. TEMPLATES Y WSGI
# ==========================================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'FonoApp.wsgi.application'


# ==========================================
# 5. BASE DE DATOS
# ==========================================
# En Render, se leerá automáticamente la variable DATABASE_URL.
# Si no existe (como en tu local), usará esta cadena de conexión con tus credenciales.
DATABASES = {
    'default': dj_database_url.config(
        default='postgres://admin:secret@localhost:5432/fonoDevDB',
        conn_max_age=600
    )
}


# ==========================================
# 6. VALIDACIÓN DE CONTRASEÑAS E INTERNACIONALIZACIÓN
# ==========================================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# ==========================================
# 7. ARCHIVOS ESTÁTICOS
# ==========================================
STATIC_URL = 'static/'
# Directorio donde se recopilarán los estáticos al ejecutar collectstatic (Obligatorio para Render)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# Compresión y cacheo de estáticos con Whitenoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# ==========================================
# 8. REST FRAMEWORK & JWT
# ==========================================
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'FonoAppFunciones.authentication.CustomJWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

AUTH_USER_MODEL = 'FonoAppAdministracion.FonoApp_Administracion'

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id_usuario',
    'USER_ID_CLAIM': 'user_id',
}


# ==========================================
# 9. MANEJO DE IMÁGENES / MEDIA
# ==========================================
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'