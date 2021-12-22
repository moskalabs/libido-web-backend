import os

from pathlib import Path
import pymysql
#from django.contrib.sites.models import Site

pymysql.install_as_MySQLdb()

from my_settings import DATABASES, EMAIL_HOST, EMAIL_PORT, SECRET_KEY, ALGORITHM, YOUTUBE_DATA_API_KEY, \
    EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, AWS_IAM_ACCESS_KEY, AWS_IAM_SECRET_KEY, AWS_S3_REGION_NAME, \
        AWS_STORAGE_BUCKET_NAME, AWS_S3_CUSTOM_DOMAIN, AWS_S3_OBJECT_PARAMETERS, DEFAULT_FILE_STORAGE

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# AWS IAM
AWS_IAM_ACCESS_KEY       = AWS_IAM_ACCESS_KEY
AWS_IAM_SECRET_KEY       = AWS_IAM_SECRET_KEY
AWS_S3_REGION_NAME       = AWS_S3_REGION_NAME
AWS_STORAGE_BUCKET_NAME  = AWS_STORAGE_BUCKET_NAME
AWS_S3_CUSTOM_DOMAIN     = AWS_S3_CUSTOM_DOMAIN
AWS_S3_OBJECT_PARAMETERS = AWS_S3_OBJECT_PARAMETERS
DEFAULT_FILE_STORAGE     = DEFAULT_FILE_STORAGE

# EMAIL
EMAIL_HOST = EMAIL_HOST
EMAIL_PORT = EMAIL_PORT
EMAIL_HOST_USER = EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = EMAIL_HOST_PASSWORD

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY           = SECRET_KEY
ALGORITHM            = ALGORITHM
YOUTUBE_DATA_API_KEY = YOUTUBE_DATA_API_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition
DJANGO_APPS = [
    # 'django.contrib.admin',
    # 'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

PROJECT_APPS = [
    'core',
    'users',
    'rooms',
    'contents',
]

THIRD_PARTY_APPS = [
    'corsheaders',
    'django_crontab',
]

INSTALLED_APPS = DJANGO_APPS + PROJECT_APPS + THIRD_PARTY_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    # 'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = DATABASES


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

##CORS
CORS_ORIGIN_ALLOW_ALL=True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
)
CORS_ALLOW_HEADERS = (
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
)

# CRONTAB
CRONJOBS = [
    ('0 10,22 * * *', 'config.cron.popular_videos_get_youtube_api', '>> '+os.path.join(BASE_DIR, 'config/log/cron.log'))
]