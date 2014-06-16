"""
Django settings for projectcm project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '5zy_3dp4q*mq#$em)c*ulg5smepc83&479f=ots!6&(@1-0jbi'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'adressbook',
    'accounts',
    'mail',
    'south',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'cal',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'projectcm.urls'

WSGI_APPLICATION = 'projectcm.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, "..", "files") 
MEDIA_URL = '/files/'
ADMIN_MEDIA_PREFIX = '/files/admin/'

# Template location
TEMPLATE_DIRS = (
	os.path.join(os.path.dirname(BASE_DIR), "static", "templates"),
)

# Disable south for unit test runs
SOUTH_TESTS_MIGRATE = False


STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static", "templates"),
)

# Timeout for registration
# ACCOUNT_ACTIVATION_DAYS = 1

# Authentication config
TEMPLATE_CONTEXT_PROCESSORS = (
    # Required by allauth template tags
    "django.core.context_processors.request",
    "django.contrib.auth.context_processors.auth",    
    # allauth specific context processors
    "allauth.account.context_processors.account",
    "allauth.socialaccount.context_processors.socialaccount",
    
)

AUTHENTICATION_BACKENDS = (

    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",

    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
    
)

SITE_ID = 1

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
