import os
from pathlib import Path

# Optional CA bundle support for outbound HTTPS calls
try:
    import certifi
except ImportError:
    certifi = None

if certifi:
    os.environ.setdefault("SSL_CERT_FILE", certifi.where())

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY
SECRET_KEY = 'django-insecure-kwc*&i89x0u)kvjfo6d3c=&iu=jxb1rt&2qilb&nbn41-+%)ac'

DEBUG = True

ALLOWED_HOSTS = ['*']


# Applications
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'corsheaders',

    'users',
    'Home',
]


# Middleware
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'backend.urls'


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


WSGI_APPLICATION = 'backend.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
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


# Internationalization
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static & Media Files
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# CORS
CORS_ALLOW_ALL_ORIGINS = True


# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}


# Custom User Model
AUTH_USER_MODEL = 'users.User'


# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp-relay.brevo.com'

EMAIL_PORT = 587

EMAIL_HOST_USER = 'aa31da001@smtp-brevo.com'

EMAIL_HOST_PASSWORD = ""

EMAIL_USE_TLS = True


# Brevo API Settings
DEFAULT_FROM_EMAIL = 'amerr.mohaamed209@gmail.com'

BREVO_API_BASE_URL = 'https://api.brevo.com/v3'

BREVO_API_KEY = ""

BREVO_SENDER_EMAIL = DEFAULT_FROM_EMAIL

BREVO_SENDER_NAME = 'Salem'

BREVO_EMAIL_TIMEOUT = 30


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

