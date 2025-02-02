from pathlib import Path
import os

# Ruta base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# Clave secreta (asegúrate de no dejarla vacía)
SECRET_KEY = 'django-insecure-4hfj8#jsl%@fhj4h48y24%*!@3rt34v$#&'

# Modo de depuración
DEBUG = True

ALLOWED_HOSTS = []  # Asegúrate de añadir tus dominios en producción.

# Configuración del campo de auto-incremento predeterminado
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField' 

# Aplicaciones instaladas
INSTALLED_APPS = [
    'widget_tweaks', 
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'web', # Tu aplicación personalizada
    
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Configuración de URLs y WSGI
ROOT_URLCONF = 'cesfam.urls'
WSGI_APPLICATION = 'cesfam.wsgi.application' 

# Configuración de plantillas
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',  # Directorio de plantillas personalizadas globales
        ],
        'APP_DIRS': True,  # Esto permite que Django busque plantillas dentro de cada aplicación
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Configuración de la base de datos
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Validadores de contraseñas
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Configuración de internacionalización y zona horaria
LANGUAGE_CODE = 'es-es'  # Cambiado a español (si corresponde)
TIME_ZONE = 'UTC'  # Cambia a tu zona horaria local si es necesario
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Configuración de archivos estáticos
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',  # Directorio donde están tus archivos estáticos
]

# Configuración de archivos multimedia
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Configuración de autenticación personalizada
AUTHENTICATION_BACKENDS = [
    'web.backends.DoctorBackend',
    'web.backends.PacienteBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# Modelo de usuario personalizado
#AUTH_USER_MODEL = 'web.Paciente'


# Configuración de rutas de inicio de sesión y redirección
LOGIN_REDIRECT_URL = '/web/dashboard_paciente/'
LOGIN_URL = '/web/login_paciente/'

# Configuración de sesiones
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_SECURE = False  # Cambiar a True si usas HTTPS
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_AGE = 1209600  # 2 semanas

# Ajustes de seguridad
CSRF_COOKIE_SECURE = False  # Cambiar a True en producción con HTTPS
X_FRAME_OPTIONS = 'DENY'

# Configuración adicional en modo DEBUG
if DEBUG:
    # Solo sirve archivos estáticos y de medios en modo DEBUG
    from django.conf.urls.static import static
