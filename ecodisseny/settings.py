from pathlib import Path
from decouple import config


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = []

# Apps instaladas
INSTALLED_APPS = [
    'jazzmin',                          # Admin personalizado
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'maestros',
    'projectes',
    'pressupostos',
     "dal",
    "dal_select2",  # O el widget que prefieras
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ecodisseny.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],  # Plantillas personalizadas
        'APP_DIRS': True,
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

WSGI_APPLICATION = 'ecodisseny.wsgi.application'

# Base de datos (MySQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT', cast=int),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    }
}

# Validadores de contraseña
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internacionalización
LANGUAGE_CODE = 'ca'
TIME_ZONE = 'Europe/Madrid'
USE_I18N = True
USE_TZ = True

# Archivos estáticos
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / "static"]

# Campo ID por defecto
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuración de Jazzmin
JAZZMIN_SETTINGS = {
    "site_title": "Administració Ecodisseny",
    "site_header": "Ecodisseny",
    "site_brand": "Ecodisseny",
    "site_logo": "logo_ecodisseny_negatiu.png",       # archivo en static/
    "login_logo": "logo_ecodisseny_positiu.png",
    "login_logo_dark": "logo_ecodisseny_positiu.png",
    "site_logo_classes": "img-fluid",
    "site_icon": "favicon.ico",                        # favicon en static/
    "welcome_sign": "Benvingut a l’administrador d’Ecodisseny!",
    "copyright": "©  Ecodisseny - A.Rasmussen",
    "show_sidebar": True,
    "navigation_expanded": True,
    "order_with_respect_to": ["auth", "clients", "maestros.Parroquia",
    "maestros.Poblacio",
    "maestros.Tipusrecurso",
    "maestros.Recurso",
    "maestros.Treballs",
    "maestros.Tasca","pressupostos"],
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "maestros.Clients": "fas fa-building",
        "pressupostos.Pressupostos": "fas fa-file-invoice",
        "projectes.Projectes": "fas fa-project-diagram",
    },
    "topmenu_links": [
        {"name": "Inici", "url": "/", "permissions": ["auth.view_user"]},
        {"model": "auth.User"},
        {"app": "auth"},
    ],
    "usermenu_links": [
        {"name": "Ajuda", "url": "https://ecodisseny.cat/ajuda", "new_window": True},
    ],
    "related_modal_active": True,
    

}

# Ajustes de estilo Jazzmin
JAZZMIN_UI_TWEAKS = {}
