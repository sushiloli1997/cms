
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent



#newly added 

import pymysql

pymysql.install_as_MySQLdb()






SECRET_KEY = "django-insecure-&=mbft4@yg70i9bmd7)!(f$_b8u%%-_1vtm1v4rmuj*7p(aes9"



DEBUG = True

ALLOWED_HOSTS =['202.51.1.167','127.0.0.1']

# ALLOWED_HOSTS = ['202.51.1.167','127.0.0.1']


# Application definition

INSTALLED_APPS = [
    # 'jazzmin',
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'django_dump_die',
    # "storage",
    "contracts",

]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'django_dump_die.middleware.DumpAndDieMiddleware',
]

ROOT_URLCONF = "djangoProject7.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'templates'],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "djangoProject7.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases


# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }


DATABASES= { 
        "default":{ 
        "ENGINE":"django.db.backends.mysql",
        "NAME":"contract",
        "USER":"dev",
        "PASSWORD":"zmv3dL!:wmQcbcAx",
        "HOST":"localhost",
        "PORT":"3306",
}

}


# DATABASES= { 
#         "default":{ 
#         "ENGINE":"django.db.backends.mysql",
#         "NAME":"contract",
#         "USER":"dev",
#         "PASSWORD":"zmv3dL!:wmQcbcAx",
#         "HOST":"localhost",
#         "PORT":"3306",
# }

# }



# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators


AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]



# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/



LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kathmandu"

USE_I18N = True



# USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"

STATIC_ROOT = BASE_DIR / 'static'

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

STATICFILES_DIRS =  [
    # Put strings here, like "/home/html/static" or "C:/www/    
    os.path.join(BASE_DIR,"contracts/static")
]

SMS_TOKEN = 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIyIiwianRpIjoiYzU2NjIxYzNjNzFhNzZjNTRmYzE1MGEyNTA3MTNiMDdiY2JmZDJiZDUyMzU3YTZlOTVlOGViNGMwYjE4Mjk3ZmUyYmQ2Yjg1YWFjNDE2M2MiLCJpYXQiOjE2NTc4NzUwMzYuODYzMDQsIm5iZiI6MTY1Nzg3NTAzNi44NjMwNDcsImV4cCI6MTY4OTQxMTAzNi44NTc2OCwic3ViIjoiMyIsInNjb3BlcyI6W119.eWOjyZEQX1PPLFBkjkiMNm548f_2s0QrVUb4VItD2dfjCiKMp_CWGjvztGSc3lxY6SP0u0GI4Sz6oMwpJQCHjw'



# STATICFILES_STORAGE = "whitenoise.storage.CompressManufestStaticFilesStorage"


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = 'media/'


LOGIN_REDIRECT_URL = 'dashboard'
LOGIN_URL = 'login'
LOGOUT_REDIRECT_URL = 'login'