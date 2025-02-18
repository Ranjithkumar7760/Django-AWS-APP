import os
from pathlib import Path
import dj_database_url
from dotenv import load_dotenv
import logging


logging.basicConfig(level=logging.DEBUG)
AWS_S3_VERBOSE = True

# ✅ Load environment variables from .env file
load_dotenv()

DATABASES = {
    'default': dj_database_url.config(
        default=f"postgres://{os.getenv('DB_USER', 'postgres')}:{os.getenv('DB_PASSWORD', 'Demo12345')}@{os.getenv('DB_HOST', 'hospitaldb.cq1kcq80oqfm.us-east-1.rds.amazonaws.com')}:{os.getenv('DB_PORT', '5432')}/{os.getenv('DB_NAME', 'demo')}"
    )
}

# ✅ Base directory of the Django project
BASE_DIR = Path(__file__).resolve().parent.parent

# ✅ Security settings
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'your-default-secret-key')
DEBUG = os.getenv('DEBUG', 'True') == 'True'  # Set DEBUG=False in production

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*').split(',')  # Allow multiple hosts

# ✅ Installed applications
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',  # AWS S3 Storage
    'patients',
]

# ✅ Middleware configuration
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ✅ Root URL configuration
ROOT_URLCONF = 'healthcare.urls'

# ✅ Template settings (Fix: Ensure it looks in `patients/templates`)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR, 'patients', 'templates'),  # Ensure Django finds templates
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

# ✅ WSGI application
WSGI_APPLICATION = 'healthcare.wsgi.application'


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-cache-name',
    }
}


# ✅ Database Configuration (AWS RDS PostgreSQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'demo'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'Demo12345'),
        'HOST': os.getenv('DB_HOST', 'hospitaldb.cq1kcq80oqfm.us-east-1.rds.amazonaws.com'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

# ✅ If DATABASE_URL exists, override default database settings
if os.getenv('DATABASE_URL'):
    DATABASES['default'] = dj_database_url.config(default=os.getenv('DATABASE_URL'), conn_max_age=600, ssl_require=True)

# ✅ Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ✅ Static files settings
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "patients/static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# ✅ Media files settings (Local Storage)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ✅ AWS S3 Storage (For Media and Static Files)
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_REGION_NAME = os.getenv('AWS_REGION_NAME', 'us-east-1')
AWS_S3_CUSTOM_DOMAIN = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None  # Set to None to allow default permissions
AWS_QUERYSTRING_AUTH = False  # Remove query string parameters



if AWS_STORAGE_BUCKET_NAME:
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
    
else:
     DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
    #  STATIC_URL = '/static/'
    #  MEDIA_URL = '/media/'
    
STATIC_URL = f'{AWS_S3_CUSTOM_DOMAIN}/static/'
MEDIA_URL = f'{AWS_S3_CUSTOM_DOMAIN}/media/'
MEDIA_ROOT = BASE_DIR / 'media'    


STATICFILES_DIRS = [os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')]
MEDIA_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media')

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'


# ✅ Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ✅ Authentication Settings
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'  # Redirect to dashboard after login
