from pathlib import Path
import os
import dj_database_url
import json
from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader
import cloudinary.api


# Cloudinary configuration
cloudinary.config( 
  cloud_name = "dudgux9az", 
  api_key = "841512714949838", 
  api_secret = os.environ.get('CLOUDINARY_API_SECRET')
)

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-r#!m*v1&z9ui1-#(d@brlq27kthtyf1xs94#*h^hj$=i==bkiu')

DEBUG = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.vercel.app', 'www.certifly.net']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'cloudinary',  # Add this line
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

ROOT_URLCONF = 'certifly.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'core' / 'templates',
        ],
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

WSGI_APPLICATION = 'certifly.wsgi.application'

DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3'),
        conn_max_age=600,
        ssl_require='sslmode' not in os.environ.get('DATABASE_URL', '')
    )
}

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

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files settings
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'core' / 'static' / 'core',
]



# Media files settings
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STRIPE_PUBLIC_KEY = os.environ.get('STRIPE_PUBLIC_KEY', 'pk_test_51NX0mtC3h0OOCQZlbth0hw952PRCigsefJ7JdHqgAzDLrT9duODRzg2bkVOqTDDTGu6hGSgdichP47MTQDvCvcw7000XCzWN82')
STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY', 'sk_test_51NX0mtC3h0OOCQZldCWB9Xrakj14lm9Iq7OJM0C4cDFI677ctkChuQ3ZTTSgTvnp7sJYzkdgJOJg6PpRmQxcVo7900j8c7aftW')
STRIPE_PRICE_ID = os.environ.get('STRIPE_PRICE_ID', 'price_1PfszDC3h0OOCQZlEcpfmN67')

AUTH_USER_MODEL = 'core.User'

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

GOOGLE_SERVICE_ACCOUNT_INFO = json.loads(os.environ.get('GOOGLE_SERVICE_ACCOUNT_INFO', '{}'))

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'certiflyreset@gmail.com'
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

if 'GOOGLE_CLIENT_SECRETS_JSON' in os.environ:
    client_secrets = json.loads(os.environ['GOOGLE_CLIENT_SECRETS_JSON'])
else:
    GOOGLE_OAUTH2_CLIENT_SECRETS_JSON = os.path.join(BASE_DIR, 'client_secrets.json')
    with open(GOOGLE_OAUTH2_CLIENT_SECRETS_JSON) as f:
        client_secrets = json.load(f)

GOOGLE_OAUTH2_CLIENT_ID = client_secrets['web']['client_id']
GOOGLE_OAUTH2_CLIENT_SECRET = client_secrets['web']['client_secret']