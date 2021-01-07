"""
Django settings for DeskSolutions project.

Generated by 'django-admin startproject' using Django 3.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os
import django_heroku
import dj_database_url
from decouple import config



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ad^gbq0h)tg7oc9tf6_iqku6&om5p^nzq*%pnavjwd6jr9w)*-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['desksolutions.herokuapp.com']


# Application definition

INSTALLED_APPS = [

    'colorfield',
    'ckeditor',

    'DeskSolutions',
    'rest_framework',
    'rest_framework.authtoken',

    'account.apps.AccountConfig',
    'desksolutionsbase.apps.DesksolutionsbaseConfig',
    'TaskManagement.apps.TaskmanagementConfig',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'admin_interface',
    # 'leaflet',
    # 'django_extensions',
    'mapwidgets',
    "fcm_django",
    'django.contrib.gis',

]
X_FRAME_OPTIONS='SAMEORIGIN' # only if django version >= 3.0

AUTH_USER_MODEL = 'account.User'
GROUP_ALLOCATE = "OrganizationAdministrators"

GOOGLE_MAPS_API_KEY = "AIzaSyBX8TzU9ISXBXcAmW-MQhtckPprS5AOcOw"

# GDAL_LIBRARY_PATH = 'D:/deskSolutions/GDAL-3.1.4-cp38-cp38-win32.whl'
# GEOS_LIBRARY_PATH = 'C:/Users/LAPTOP MART/AppData/Local/Programs/Python/Python38/Lib/site-packages/osgeo/geos_c.dll'
GEOS_LIBRARY_PATH = os.path.join(BASE_DIR, 'env/Lib/site-packages/osgeo/geos_c.dll')

# GDAL_LIBRARY_PATH = 'C:/Users/LAPTOP MART/AppData/Local/Programs/Python/Python38/Lib/site-packages/osgeo/gdal301.dll'
GDAL_LIBRARY_PATH = os.path.join(BASE_DIR, 'env/Lib/site-packages/osgeo/gdal301.dll')

# MAP_WIDGETS = {
#     "GooglePointFieldWidget": (
#         ("zoom", 15),
#         ("mapCenterLocationName", "london"),
#         ("GooglePlaceAutocompleteOptions", {'componentRestrictions': {'country': 'uk'}}),
#         ("markerFitZoom", 12),
#     ),
#     "GOOGLE_MAP_API_KEY": "AIzaSyBX8TzU9ISXBXcAmW-MQhtckPprS5AOcOw"
# }

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # 'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

CKEDITOR_CONFIGS = {
   'default': {
       'toolbar_Full': [
            ['Styles', 'Format', 'Bold', 'Italic', 'Underline', 'Strike', 'SpellChecker', 'Undo', 'Redo'],
            # ['Link', 'Unlink', 'Anchor'],
            # ['Image', 'Flash', 'Table', 'HorizontalRule'],
            # ['TextColor', 'BGColor'],
            # ['Smiley', 'SpecialChar'], ['Source'],
            ['JustifyLeft','JustifyCenter','JustifyRight','JustifyBlock'],
            ['NumberedList','BulletedList'],
            ['Indent','Outdent'],
            # ['Maximize'],
        ],
        'extraPlugins': 'justify,liststyle,indent',
   },
}

# if not DEBUG:
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'f2018027021@umt.edu.pk'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'f2018027021@umt.edu.pk'
EMAIL_HOST_PASSWORD = 'f5Uu@2tP'
EMAIL_USE_TLS = True
# else:
#     EMAIL_BACKEND = (
#         "django.core.mail.backends.smtp.EmailBackend"
#     )

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Heroku middleware
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'DeskSolutions.urls'
print(os.path.join(BASE_DIR, 'env'))
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 'DIRS': ['D:/DeskSolutionsProject/DeskSolutions/templates',],
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'DeskSolutions.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# DATABASES = {
#     'default': {
#         'ENGINE' : 'django.db.backends.postgresql_psycopg2',
#         'NAME' : 'DSDB',
#         'USER' : 'postgres',
#         'PASSWORD' : 'custom123',
#         'HOST' : 'localhost',
#         'PORT' : '5432',
#     }
# }
DATABASES = {
    'default': {
        'ENGINE' : 'django.contrib.gis.db.backends.postgis',
        'NAME' : 'DSDB',
        'USER' : 'postgres',
        'PASSWORD' : 'custom123',
        'HOST' : 'localhost',
        'PORT' : '5432',
    }
}

db_from_env = dj_database_url.config(conn_max_age=600)
DATABASES['default'].update(db_from_env)


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# For GEOIP

GEOIP_PATH = os.path.join(BASE_DIR, 'geoip')

# For Heroku

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
#location where django collect all static files
STATIC_ROOT = os.path.join(BASE_DIR,'static')
# location where you will store your static files
STATICFILES_DIRS = [
    os.path.join(BASE_DIR,'static')
]

# Handle media files

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# FCM Token Settings

FCM_DJANGO_SETTINGS = {
        "FCM_SERVER_KEY": "AAAA-RKOFa8:APA91bGXUIUW4gfgJ-wZvppSVdbSZ_MLbJCc069LZ1eyoiNKHrBzCrlz17lB0caaqnm56gCmJxv1_LQBc6E0G7Dn4Dpp-3rrJsZY8pWioFMS5ccEUcAX5h4PntPsno3bMNw0SBIUiGu7"
}

# For heroku
django_heroku.settings(locals())

