import os
import cloudinary
import dj_database_url



# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-jrvd14_9qr_r(cm*zamwl-lr^9+%5kz!ij+a=y!mmt&q32@z(m"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

if DEBUG:
    ALLOWED_HOSTS = ['*']
else:
    ALLOWED_HOSTS = ['www.ikpixels.com']
    CSRF_TRUSTED_ORIGINS = ['https://*.ikpixels.com']


# Application definition
INSTALLED_APPS = [
    'music_nation',
    'widget_tweaks',
    'Store',
    'Event',
    'account',
    'ikpixels',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ckeditor',
    'crispy_forms',
    'cloudinary',
    'embed_video',
    'qr_code',
    'storages',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ftc.urls'

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

WSGI_APPLICATION = 'ftc.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases



# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators
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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT =os.path.join(BASE_DIR, 'staticfiles')


if DEBUG:
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    MEDIA_URL = '/media/'
else:#for CPANEL HOSTING-Media will be saved to public_html
    MEDIA_ROOT = "/home/ikpixel1/public_html/media"
    MEDIA_URL = "/media/"



#LOGIN_REDIRECT_URL = 'music_nation:home'
LOGOUT_REDIRECT_URL = 'music_nation:nyansavibe'
#LOGIN_URL = 'music_nation:login'
# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

if DEBUG:
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }}
else:
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ikpixel1_main_kako_dbase',
        'USER': 'ikpixel1_isaac_kakodwa',
        'PASSWORD': 'Python@#992/',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {

        'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"

    },
    }
    }
