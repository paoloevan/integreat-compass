"""
Django settings for integreat_compass project.

Generated by 'django-admin startproject' using Django 4.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
from distutils.util import strtobool
from pathlib import Path
from urllib.parse import urlparse

from django.utils.translation import gettext_lazy as _

from .logging_formatter import ColorFormatter, RequestFormatter

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(strtobool(os.environ.get("INTEGREAT_COMPASS_DEBUG", "False")))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("INTEGREAT_COMPASS_SECRET_KEY", "dummy" if DEBUG else "")

BASE_URL = os.environ.get("INTEGREAT_COMPASS_BASE_URL", "http://localhost:8082")
HOSTNAME = urlparse(BASE_URL).hostname

#: This is a security measure to prevent HTTP Host header attacks, which are possible even under many seemingly-safe
ALLOWED_HOSTS = [".localhost", "127.0.0.1", "[::1]", HOSTNAME] + [
    x.strip()
    for x in os.environ.get("INTEGREAT_COMPASS_ALLOWED_HOSTS", "").splitlines()
    if x
]

# Application definition

INSTALLED_APPS = [
    "integreat_compass.cms",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "webpack_loader",
    "widget_tweaks",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "integreat_compass.core.middleware.AccessControlMiddleware",
]

ROOT_URLCONF = "integreat_compass.core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "integreat_compass.core.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

#: A dictionary containing the settings for all databases to be used with this Django installation
#: (see :setting:`django:DATABASES`)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("INTEGREAT_COMPASS_DB_NAME", "integreat-compass"),
        "USER": os.environ.get("INTEGREAT_COMPASS_DB_USER", "integreat"),
        "PASSWORD": os.environ.get(
            "INTEGREAT_COMPASS_DB_PASSWORD", "password" if DEBUG else ""
        ),
        "HOST": os.environ.get("INTEGREAT_COMPASS_DB_HOST", "localhost"),
        "PORT": os.environ.get("INTEGREAT_COMPASS_DB_PORT", "5432"),
    }
}

AUTH_USER_MODEL = "cms.User"
LOGIN_URL = "cms:public:login"
LOGIN_REDIRECT_URL = "cms:public:index"
LOGOUT_REDIRECT_URL = "cms:public:index"

#########################
# DJANGO WEBPACK LOADER #
#########################

#: Overwrite default bundle directory
WEBPACK_LOADER = {
    "DEFAULT": {
        "BUNDLE_DIR_NAME": "",
        "STATS_FILE": os.path.join(BASE_DIR, "webpack-stats.json"),
    }
}


################
# STATIC FILES #
################

#: This setting defines the additional locations the :mod:`django.contrib.staticfiles` app will traverse to collect
#: static files for deployment or to serve them during development (see :setting:`django:STATICFILES_DIRS` and
#: :doc:`Managing static files <django:howto/static-files/index>`).
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    os.path.join(BASE_DIR, "static/dist"),
]

#: The absolute path to the output directory where :mod:`django.contrib.staticfiles` will put static files for
#: deployment (see :setting:`django:STATIC_ROOT` and :doc:`Managing static files <django:howto/static-files/index>`)
#: In debug mode, this is not required since :mod:`django.contrib.staticfiles` can directly serve these files.
STATIC_ROOT = os.environ.get("INTEGREAT_COMPASS_STATIC_ROOT")

#: URL to use in development when referring to static files located in :setting:`STATICFILES_DIRS`
#: (see :setting:`django:STATIC_URL` and :doc:`Managing static files <django:howto/static-files/index>`)
STATIC_URL = "/static/"

#: The list of finder backends that know how to find static files in various locations
#: (see :setting:`django:STATICFILES_FINDERS`)
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

########################
# INTERNATIONALIZATION #
########################

#: A list of all available languages with locale files for translated strings
AVAILABLE_LANGUAGES = {"de": _("German"), "en": _("English")}

#: The default UI languages
DEFAULT_LANGUAGES = ["de", "en"]

#: The default offer language
DEFAULT_OFFER_LANGUAGE = {"native_name": "Deutsch", "english_name": "German"}


#: The list of languages which are available in the UI
#: (see :setting:`django:LANGUAGES` and :doc:`django:topics/i18n/index`)
LANGUAGES = [
    (language, AVAILABLE_LANGUAGES[language])
    for language in filter(
        None,
        (
            language.strip()
            for language in os.environ.get(
                "INTEGREAT_CMS_LANGUAGES", "\n".join(DEFAULT_LANGUAGES)
            ).splitlines()
        ),
    )
]

#: A list of directories where Django looks for translation files
#: (see :setting:`django:LOCALE_PATHS` and :doc:`django:topics/i18n/index`)
LOCALE_PATHS = [os.path.join(BASE_DIR, "locale")]

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Media Library

#: URL that handles the media served from :setting:`MEDIA_ROOT` (see :setting:`django:MEDIA_URL`)
MEDIA_URL = "/media/"

#: Absolute filesystem path to the directory that will hold user-uploaded files (see :setting:`django:MEDIA_ROOT`)
MEDIA_ROOT = os.environ.get(
    "INTEGREAT_COMPASS_MEDIA_ROOT", os.path.join(BASE_DIR, "media")
)

#: The maximum size of media files in bytes
MEDIA_MAX_UPLOAD_SIZE = int(
    os.environ.get("INTEGREAT_COMPASS_MEDIA_MAX_UPLOAD_SIZE", 3 * 1024 * 1024)
)

#: The default offer title image
DEFAULT_TITLE_IMAGE = "fallback_title_image.png"

# Voting system settings

#: Maximum votes cast on new offers
NEW_OFFER_GREMIUM_SIZE = int(
    os.environ.get("INTEGREAT_COMPASS_NEW_OFFER_GREMIUM_SIZE", 6)
)

#: Maximum votes cast on changed offers
CHANGED_OFFER_GREMIUM_SIZE = int(
    os.environ.get("INTEGREAT_COMPASS_CHANGED_OFFER_GREMIUM_SIZE", 4)
)

###########
# LOGGING #
###########

#: The log level for integreat-cms django apps
LOG_LEVEL = os.environ.get("INTEGREAT_COMPASS_LOG_LEVEL", "DEBUG" if DEBUG else "INFO")

#: The file path of the logfile. Needs to be writable by the application.
LOGFILE = os.environ.get(
    "INTEGREAT_COMPASS_LOGFILE", os.path.join(BASE_DIR, "integreat-compass.log")
)

#: Logging configuration dictionary (see :setting:`django:LOGGING`)
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "console-colored": {
            "()": ColorFormatter,
            "format": "{asctime} {levelname} {name} - {message}",
            "datefmt": "%b %d %H:%M:%S",
            "style": "{",
        },
        "management-command": {
            "()": ColorFormatter,
            "format": "{message}",
            "style": "{",
        },
        "logfile": {
            "()": RequestFormatter,
            "format": "{asctime} {levelname:7} {name} - {message}",
            "datefmt": "%b %d %H:%M:%S",
            "style": "{",
        },
    },
    "filters": {
        "require_debug_true": {"()": "django.utils.log.RequireDebugTrue"},
        "require_debug_false": {"()": "django.utils.log.RequireDebugFalse"},
    },
    "handlers": {
        "console-colored": {
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
            "formatter": "console-colored",
        },
        "management-command": {
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
            "formatter": "management-command",
        },
        "logfile": {
            "class": "logging.FileHandler",
            "filename": LOGFILE,
            "formatter": "logfile",
        },
    },
    "loggers": {
        "integreat_compass": {
            "handlers": ["console-colored", "logfile"],
            "level": LOG_LEVEL,
        },
        "integreat_compass.core.management.commands": {
            "handlers": ["management-command", "logfile"],
            "level": LOG_LEVEL,
            "propagate": False,
        },
    },
}
