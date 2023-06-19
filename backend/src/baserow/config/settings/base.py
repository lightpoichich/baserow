import datetime
import importlib
import json
import os
import re
import sys
from decimal import Decimal
from ipaddress import ip_network
from pathlib import Path
from urllib.parse import urljoin, urlparse

from django.core.exceptions import ImproperlyConfigured

import dj_database_url
from celery.schedules import crontab
from corsheaders.defaults import default_headers

from baserow.cachalot_patch import patch_cachalot_for_baserow
from baserow.config.settings.utils import (
    Setting,
    read_file,
    set_settings_from_env_if_present,
    str_to_bool,
)
from baserow.core.telemetry.utils import otel_is_enabled
from baserow.version import VERSION

# A comma separated list of feature flags used to enable in-progress or not ready
# features for developers. See docs/development/feature-flags.md for more info.
FEATURE_FLAGS = [
    flag.strip().lower() for flag in os.getenv("FEATURE_FLAGS", "").split(",")
]


class Everything(object):
    def __contains__(self, other):
        return True


if "*" in FEATURE_FLAGS or "pytest" in sys.modules:
    FEATURE_FLAGS = Everything()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BASEROW_PLUGIN_DIR_PATH = Path(os.environ.get("BASEROW_PLUGIN_DIR", "/baserow/plugins"))

if BASEROW_PLUGIN_DIR_PATH.exists():
    BASEROW_PLUGIN_FOLDERS = [
        file
        for file in BASEROW_PLUGIN_DIR_PATH.iterdir()
        if file.is_dir() and Path(file, "backend").exists()
    ]
else:
    BASEROW_PLUGIN_FOLDERS = []

BASEROW_BACKEND_PLUGIN_NAMES = [d.name for d in BASEROW_PLUGIN_FOLDERS]
BASEROW_OSS_ONLY = bool(os.getenv("BASEROW_OSS_ONLY", ""))
if BASEROW_OSS_ONLY:
    BASEROW_BUILT_IN_PLUGINS = []
else:
    BASEROW_BUILT_IN_PLUGINS = ["baserow_premium", "baserow_enterprise"]

# SECURITY WARNING: keep the secret key used in production secret!
if "SECRET_KEY" in os.environ:
    SECRET_KEY = os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("BASEROW_BACKEND_DEBUG", "off") == "on"

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
ALLOWED_HOSTS += os.getenv("BASEROW_EXTRA_ALLOWED_HOSTS", "").split(",")

INSTALLED_APPS = [
    "daphne",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt",
    "corsheaders",
    "drf_spectacular",
    "djcelery_email",
    "health_check",
    "health_check.db",
    "health_check.cache",
    "health_check.contrib.migrations",
    "health_check.contrib.redis",
    "health_check.contrib.celery_ping",
    "health_check.contrib.psutil",
    "health_check.contrib.s3boto3_storage",
    "baserow.core",
    "baserow.api",
    "baserow.ws",
    "baserow.contrib.database",
    *BASEROW_BUILT_IN_PLUGINS,
]


if "builder" in FEATURE_FLAGS:
    INSTALLED_APPS.append("baserow.contrib.builder")

ADDITIONAL_APPS = os.getenv("ADDITIONAL_APPS", "").split(",")
if ADDITIONAL_APPS is not None:
    INSTALLED_APPS += [app.strip() for app in ADDITIONAL_APPS if app.strip() != ""]

if BASEROW_BACKEND_PLUGIN_NAMES:
    print(f"Loaded backend plugins: {','.join(BASEROW_BACKEND_PLUGIN_NAMES)}")
    INSTALLED_APPS.extend(BASEROW_BACKEND_PLUGIN_NAMES)

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "baserow.middleware.BaserowCustomHttp404Middleware",
]

if otel_is_enabled():
    MIDDLEWARE += ["baserow.core.telemetry.middleware.BaserowOTELMiddleware"]

ROOT_URLCONF = "baserow.config.urls"

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
            ],
        },
    },
]

WSGI_APPLICATION = "baserow.config.wsgi.application"
ASGI_APPLICATION = "baserow.config.asgi.application"

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
REDIS_USERNAME = os.getenv("REDIS_USER", "")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "")
REDIS_PROTOCOL = os.getenv("REDIS_PROTOCOL", "redis")
REDIS_URL = os.getenv(
    "REDIS_URL",
    f"{REDIS_PROTOCOL}://{REDIS_USERNAME}:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/0",
)

BASEROW_GROUP_STORAGE_USAGE_QUEUE = os.getenv(
    "BASEROW_GROUP_STORAGE_USAGE_QUEUE", "export"
)
BASEROW_ROLE_USAGE_QUEUE = os.getenv("BASEROW_GROUP_STORAGE_USAGE_QUEUE", "export")

CELERY_BROKER_URL = REDIS_URL
CELERY_TASK_ROUTES = {
    "baserow.contrib.database.export.tasks.run_export_job": {"queue": "export"},
    "baserow.contrib.database.export.tasks.clean_up_old_jobs": {"queue": "export"},
    "baserow.core.trash.tasks.mark_old_trash_for_permanent_deletion": {
        "queue": "export"
    },
    "baserow.core.trash.tasks.permanently_delete_marked_trash": {"queue": "export"},
    "baserow.core.usage.tasks": {"queue": BASEROW_GROUP_STORAGE_USAGE_QUEUE},
    "baserow.contrib.database.table.tasks.run_row_count_job": {"queue": "export"},
    "baserow.core.jobs.tasks.clean_up_jobs": {"queue": "export"},
}
CELERY_SOFT_TIME_LIMIT = 60 * 5  # 5 minutes
CELERY_TIME_LIMIT = CELERY_SOFT_TIME_LIMIT + 60  # 60 seconds

CELERY_REDBEAT_REDIS_URL = REDIS_URL
# Explicitly set the same value as the default loop interval here so we can use it
# later. CELERY_BEAT_MAX_LOOP_INTERVAL < CELERY_REDBEAT_LOCK_TIMEOUT must be kept true
# as otherwise a beat instance will acquire the lock, do scheduling, go to sleep for
# CELERY_BEAT_MAX_LOOP_INTERVAL before waking up where it assumes it still owns the lock
# however if the lock timeout is less than the interval the lock will have been released
# and the beat instance will crash as it attempts to extend the lock which it no longer
# owns.
CELERY_BEAT_MAX_LOOP_INTERVAL = os.getenv("CELERY_BEAT_MAX_LOOP_INTERVAL", 20)
# By default CELERY_REDBEAT_LOCK_TIMEOUT = 5 * CELERY_BEAT_MAX_LOOP_INTERVAL
# Only one beat instance can hold this lock and schedule tasks at any one time.
# This means if one celery-beat instance crashes any other replicas waiting to take over
# will by default wait 25 minutes until the lock times out and they can acquire
# the lock to start scheduling tasks again.
# Instead we just set it to be slightly longer than the loop interval that beat uses.
# This means beat wakes up, checks the schedule and extends the lock every
# CELERY_BEAT_MAX_LOOP_INTERVAL seconds. If it crashes or fails to wake up
# then 80 seconds after the lock was last extended it will be released and a new
# scheduler will acquire the lock and take over.
CELERY_REDBEAT_LOCK_TIMEOUT = os.getenv(
    "CELERY_REDBEAT_LOCK_TIMEOUT", CELERY_BEAT_MAX_LOOP_INTERVAL + 60
)

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [REDIS_URL],
        },
    },
}

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
if "DATABASE_URL" in os.environ:
    DATABASES = {
        "default": dj_database_url.parse(os.getenv("DATABASE_URL"), conn_max_age=600)
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("DATABASE_NAME", "baserow"),
            "USER": os.getenv("DATABASE_USER", "baserow"),
            "PASSWORD": os.getenv("DATABASE_PASSWORD", "baserow"),
            "HOST": os.getenv("DATABASE_HOST", "db"),
            "PORT": os.getenv("DATABASE_PORT", "5432"),
        }
    }

GENERATED_MODEL_CACHE_NAME = "generated-models"
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
        "KEY_PREFIX": "baserow-default-cache",
        "VERSION": VERSION,
    },
    GENERATED_MODEL_CACHE_NAME: {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
        "KEY_PREFIX": f"baserow-{GENERATED_MODEL_CACHE_NAME}-cache",
        "VERSION": None,
    },
}


def install_cachalot():
    global CACHALOT_ONLY_CACHABLE_TABLES
    global CACHALOT_UNCACHABLE_TABLES
    global CACHALOT_TIMEOUT
    global INSTALLED_APPS

    INSTALLED_APPS.append("cachalot")

    BASEROW_CACHALOT_ONLY_CACHABLE_TABLES = os.getenv(
        "BASEROW_CACHALOT_ONLY_CACHABLE_TABLES", None
    )

    # This list will have priority over CACHALOT_ONLY_CACHABLE_TABLES.
    BASEROW_CACHALOT_UNCACHABLE_TABLES = os.getenv(
        "BASEROW_CACHALOT_UNCACHABLE_TABLES", None
    )

    BASEROW_CACHALOT_MODE = os.getenv("BASEROW_CACHALOT_MODE", "default")

    if BASEROW_CACHALOT_MODE == "full":
        CACHALOT_ONLY_CACHABLE_TABLES = []

    elif BASEROW_CACHALOT_ONLY_CACHABLE_TABLES:
        # Please avoid to add tables with more than 50 modifications per minute
        # to this list, as described here:
        # https://django-cachalot.readthedocs.io/en/latest/limits.html
        CACHALOT_ONLY_CACHABLE_TABLES = BASEROW_CACHALOT_ONLY_CACHABLE_TABLES.split(",")
    else:
        CACHALOT_ONLY_CACHABLE_TABLES = [
            "auth_user",
            "django_content_type",
            "core_settings",
            "core_userprofile",
            "core_application",
            "core_operation",
            "core_template",
            "core_trashentry",
            "core_workspace",
            "core_workspaceuser",
            "core_workspaceuserinvitation",
            "core_authprovidermodel",
            "core_passwordauthprovidermodel",
            "database_database",
            "database_table",
            "database_field",
            "database_fieldependency",
            "database_linkrowfield",
            "database_selectoption",
            "baserow_premium_license",
            "baserow_premium_licenseuser",
            "baserow_enterprise_role",
            "baserow_enterprise_roleassignment",
            "baserow_enterprise_team",
            "baserow_enterprise_teamsubject",
        ]

    if BASEROW_CACHALOT_UNCACHABLE_TABLES:
        CACHALOT_UNCACHABLE_TABLES += list(
            filter(bool, BASEROW_CACHALOT_UNCACHABLE_TABLES.split(","))
        )

    CACHALOT_TIMEOUT = int(os.getenv("BASEROW_CACHALOT_TIMEOUT", 60 * 60 * 24 * 7))

    patch_cachalot_for_baserow()


CACHALOT_ENABLED = os.getenv("BASEROW_CACHALOT_ENABLED", "false") == "true"
CACHALOT_CACHE = "cachalot"
CACHALOT_UNCACHABLE_TABLES = [
    "django_migrations",
    "core_action",
    "database_token",
    "baserow_enterprise_auditlogentry",
]

if CACHALOT_ENABLED:
    install_cachalot()

    CACHES[CACHALOT_CACHE] = {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
        "KEY_PREFIX": f"baserow-{CACHALOT_CACHE}-cache",
        "VERSION": VERSION,
    }


CELERY_SINGLETON_BACKEND_CLASS = (
    "baserow.celery_singleton_backend.RedisBackendForSingleton"
)

# This flag enable automatic index creation for table views based on sortings.
AUTO_INDEX_VIEW_ENABLED = os.getenv("BASEROW_AUTO_INDEX_VIEW_ENABLED", "true") == "true"
AUTO_INDEX_LOCK_EXPIRY = os.getenv("BASEROW_AUTO_INDEX_LOCK_EXPIRY", 60 * 2)

# Should contain the database connection name of the database where the user tables
# are stored. This can be different than the default database because there are not
# going to be any relations between the application schema and the user schema.
USER_TABLE_DATABASE = "default"

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "baserow.core.user.password_validation.MaximumLengthValidator",
    },
]

# We need the `AllowAllUsersModelBackend` in order to respond with a proper error
# message when the user is not active. The only thing it does, is allowing non active
# users to authenticate, but the user still can't obtain or use a JWT token or database
# token because the user needs to be active to use that.
AUTHENTICATION_BACKENDS = ["django.contrib.auth.backends.AllowAllUsersModelBackend"]

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = "en"

LANGUAGES = [
    ("en", "English"),
    ("fr", "French"),
    ("nl", "Dutch"),
    ("de", "German"),
    ("es", "Spanish"),
    ("it", "Italian"),
    ("pl", "Polish"),
]

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = "/static/"

SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "baserow.api.authentication.JSONWebTokenAuthentication",
    ),
    "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
    "DEFAULT_SCHEMA_CLASS": "baserow.api.openapi.AutoSchema",
}

# Limits the number of concurrent requests per user.
# If BASEROW_MAX_CONCURRENT_USER_REQUESTS is not set, then the default value of -1
# will be used which means the throttling is disabled.
BASEROW_MAX_CONCURRENT_USER_REQUESTS = int(
    os.getenv("BASEROW_MAX_CONCURRENT_USER_REQUESTS", -1)
)

if BASEROW_MAX_CONCURRENT_USER_REQUESTS > 0:
    REST_FRAMEWORK["DEFAULT_THROTTLE_CLASSES"] = [
        "baserow.throttling.ConcurrentUserRequestsThrottle",
    ]

    REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"] = {
        "concurrent_user_requests": BASEROW_MAX_CONCURRENT_USER_REQUESTS
    }

    MIDDLEWARE += [
        "baserow.middleware.ConcurrentUserRequestsMiddleware",
    ]

# The maximum number of seconds that a request can be throttled for.
BASEROW_CONCURRENT_USER_REQUESTS_THROTTLE_TIMEOUT = int(
    os.getenv("BASEROW_CONCURRENT_USER_REQUESTS_THROTTLE_TIMEOUT", 30)
)

PUBLIC_VIEW_AUTHORIZATION_HEADER = "Baserow-View-Authorization"

CORS_ORIGIN_ALLOW_ALL = True
CLIENT_SESSION_ID_HEADER = "ClientSessionId"
MAX_CLIENT_SESSION_ID_LENGTH = 256

CLIENT_UNDO_REDO_ACTION_GROUP_ID_HEADER = "ClientUndoRedoActionGroupId"
MAX_UNDOABLE_ACTIONS_PER_ACTION_GROUP = 20
WEBSOCKET_ID_HEADER = "WebsocketId"

CORS_ALLOW_HEADERS = list(default_headers) + [
    WEBSOCKET_ID_HEADER,
    PUBLIC_VIEW_AUTHORIZATION_HEADER,
    CLIENT_SESSION_ID_HEADER,
    CLIENT_UNDO_REDO_ACTION_GROUP_ID_HEADER,
]

ACCESS_TOKEN_LIFETIME = datetime.timedelta(
    minutes=int(os.getenv("BASEROW_ACCESS_TOKEN_LIFETIME_MINUTES", 10))  # 10 minutes
)
REFRESH_TOKEN_LIFETIME = datetime.timedelta(
    hours=int(os.getenv("BASEROW_REFRESH_TOKEN_LIFETIME_HOURS", 24 * 7))  # 7 days
)

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": ACCESS_TOKEN_LIFETIME,
    "REFRESH_TOKEN_LIFETIME": REFRESH_TOKEN_LIFETIME,
    "AUTH_HEADER_TYPES": ("JWT",),
    # It is recommended that you set BASEROW_JWT_SIGNING_KEY so it is independent
    # from the Django SECRET_KEY. This will make changing the signing key used for
    # tokens easier in the event that it is compromised.
    "SIGNING_KEY": os.getenv("BASEROW_JWT_SIGNING_KEY", os.getenv("SECRET_KEY")),
    "USER_AUTHENTICATION_RULE": lambda user: user is not None,
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Baserow API spec",
    "DESCRIPTION": "For more information about our REST API, please visit "
    "[this page](https://baserow.io/docs/apis%2Frest-api).\n\n"
    "For more information about our deprecation policy, please visit "
    "[this page](https://baserow.io/docs/apis%2Fdeprecations).",
    "CONTACT": {"url": "https://baserow.io/contact"},
    "LICENSE": {
        "name": "MIT",
        "url": "https://gitlab.com/baserow/baserow/-/blob/master/LICENSE",
    },
    "VERSION": "1.18.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "TAGS": [
        {"name": "Settings"},
        {"name": "User"},
        {"name": "User files"},
        {"name": "Groups"},  # GroupDeprecation
        {"name": "Group invitations"},  # GroupDeprecation
        {"name": "Workspaces"},
        {"name": "Workspace invitations"},
        {"name": "Templates"},
        {"name": "Trash"},
        {"name": "Applications"},
        {"name": "Snapshots"},
        {"name": "Jobs"},
        {"name": "Database tables"},
        {"name": "Database table fields"},
        {"name": "Database table views"},
        {"name": "Database table view filters"},
        {"name": "Database table view sortings"},
        {"name": "Database table view decorations"},
        {"name": "Database table grid view"},
        {"name": "Database table gallery view"},
        {"name": "Database table form view"},
        {"name": "Database table kanban view"},
        {"name": "Database table calendar view"},
        {"name": "Database table rows"},
        {"name": "Database table export"},
        {"name": "Database table webhooks"},
        {"name": "Database tokens"},
        {"name": "Builder pages"},
        {"name": "Builder page elements"},
        {"name": "Builder domains"},
        {"name": "Builder public"},
        {"name": "Admin"},
    ],
    "ENUM_NAME_OVERRIDES": {
        "NumberDecimalPlacesEnum": [
            (0, "1"),
            (1, "1.0"),
            (2, "1.00"),
            (3, "1.000"),
            (4, "1.0000"),
            (5, "1.00000"),
        ],
        "ViewTypesEnum": [
            "grid",
            "gallery",
            "form",
            "kanban",
            "calendar",
        ],
        "FieldTypesEnum": [
            "text",
            "long_text",
            "url",
            "email",
            "number",
            "rating",
            "boolean",
            "date",
            "last_modified",
            "created_on",
            "link_row",
            "file",
            "single_select",
            "multiple_select",
            "phone_number",
            "formula",
            "count",
            "lookup",
        ],
        "ViewFilterTypesEnum": [
            "equal",
            "not_equal",
            "filename_contains",
            "has_file_type",
            "contains",
            "contains_not",
            "length_is_greater_than",
            "length_is_lower_than",
            "higher_than",
            "lower_than",
            "date_equal",
            "date_before",
            "date_after",
            "date_not_equal",
            "date_equals_today",
            "date_equals_days_ago",
            "date_equals_week",
            "date_equals_month",
            "date_equals_day_of_month",
            "date_equals_year",
            "single_select_equal",
            "single_select_not_equal",
            "link_row_has",
            "link_row_has_not",
            "boolean",
            "empty",
            "not_empty",
            "multiple_select_has",
            "multiple_select_has_not",
        ],
        "EventTypesEnum": ["rows.created", "rows.updated", "rows.deleted"],
    },
}

# Allows accessing and setting values on a dictionary like an object. Using this
# we can pass plugin authors and other functions a `settings` object which can modify
# the settings like they expect (settings.SETTING = 'test') etc.


class AttrDict(dict):
    def __getattr__(self, item):
        return super().__getitem__(item)

    def __setattr__(self, item, value):
        globals()[item] = value

    def __setitem__(self, key, value):
        globals()[key] = value


# The storage must always overwrite existing files.
DEFAULT_FILE_STORAGE = "baserow.core.storage.OverwriteFileSystemStorage"

AWS_STORAGE_ENABLED = os.getenv("AWS_ACCESS_KEY_ID", "") != ""
GOOGLE_STORAGE_ENABLED = os.getenv("GS_BUCKET_NAME", "") != ""
AZURE_STORAGE_ENABLED = os.getenv("AZURE_ACCOUNT_NAME", "") != ""

ALL_STORAGE_ENABLED_VARS = [
    AZURE_STORAGE_ENABLED,
    GOOGLE_STORAGE_ENABLED,
    AWS_STORAGE_ENABLED,
]
if sum(ALL_STORAGE_ENABLED_VARS) > 1:
    raise ImproperlyConfigured(
        "You have enabled more than one user file storage backend, please make sure "
        "you set only one of AWS_ACCESS_KEY_ID, GS_BUCKET_NAME and AZURE_ACCOUNT_NAME."
    )

if AWS_STORAGE_ENABLED:
    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
    set_settings_from_env_if_present(
        AttrDict(vars()),
        [
            "AWS_S3_SESSION_PROFILE",
            "AWS_ACCESS_KEY_ID",
            "AWS_SECRET_ACCESS_KEY",
            "AWS_STORAGE_BUCKET_NAME",
            Setting(
                "AWS_S3_OBJECT_PARAMETERS",
                parser=json.loads,
                default={
                    "CacheControl": "max-age=86400",
                },
            ),
            Setting("AWS_DEFAULT_ACL", default="public-read"),
            Setting("AWS_QUERYSTRING_AUTH", parser=str_to_bool),
            Setting("AWS_S3_MAX_MEMORY_SIZE", parser=int),
            Setting("AWS_QUERYSTRING_EXPIRE", parser=int),
            Setting("AWS_S3_FILE_OVERWRITE", parser=str_to_bool, default=True),
            "AWS_S3_URL_PROTOCOL",
            "AWS_S3_REGION_NAME",
            "AWS_S3_ENDPOINT_URL",
            "AWS_S3_CUSTOM_DOMAIN",
            "AWS_LOCATION",
            Setting("AWS_IS_GZIPPED", parser=str_to_bool),
            "GZIP_CONTENT_TYPES",
            Setting("AWS_S3_USE_SSL", parser=str_to_bool),
            Setting("AWS_S3_VERIFY", parser=str_to_bool),
            Setting(
                "AWS_SECRET_ACCESS_KEY_FILE_PATH",
                setting_name="AWS_SECRET_ACCESS_KEY",
                parser=read_file,
            ),
            "AWS_S3_ADDRESSING_STYLE",
            Setting("AWS_S3_PROXIES", parser=json.loads),
            "AWS_S3_SIGNATURE_VERSION",
            Setting("AWS_CLOUDFRONT_KEY", parser=lambda s: s.encode("ascii")),
            "AWS_CLOUDFRONT_KEY_ID",
        ],
    )


if GOOGLE_STORAGE_ENABLED:
    from google.oauth2 import service_account

    # See https://django-storages.readthedocs.io/en/latest/backends/gcloud.html for
    # details on what these env variables do

    DEFAULT_FILE_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
    set_settings_from_env_if_present(
        AttrDict(vars()),
        [
            "GS_BUCKET_NAME",
            "GS_PROJECT_ID",
            Setting("GS_IS_GZIPPED", parser=str_to_bool),
            "GZIP_CONTENT_TYPES",
            Setting("GS_DEFAULT_ACL", default="publicRead"),
            Setting("GS_QUERYSTRING_AUTH", parser=str_to_bool),
            Setting("GS_FILE_OVERWRITE", parser=str_to_bool),
            Setting("GS_MAX_MEMORY_SIZE", parser=int),
            Setting("GS_BLOB_CHUNK_SIZE", parser=int),
            Setting("GS_OBJECT_PARAMETERS", parser=json.loads),
            "GS_CUSTOM_ENDPOINT",
            "GS_LOCATION",
            Setting("GS_EXPIRATION", parser=int),
            Setting(
                "GS_CREDENTIALS_FILE_PATH",
                setting_name="GS_CREDENTIALS",
                parser=service_account.Credentials.from_service_account_file,
            ),
        ],
    )

if AZURE_STORAGE_ENABLED:
    DEFAULT_FILE_STORAGE = "storages.backends.azure_storage.AzureStorage"
    set_settings_from_env_if_present(
        AttrDict(vars()),
        [
            "AZURE_ACCOUNT_NAME",
            "AZURE_ACCOUNT_KEY",
            Setting(
                "AZURE_ACCOUNT_KEY_FILE_PATH",
                setting_name="AZURE_ACCOUNT_KEY",
                parser=read_file,
            ),
            "AZURE_CONTAINER",
            Setting("AZURE_SSL", parser=str_to_bool),
            Setting("AZURE_UPLOAD_MAX_CONN", parser=int),
            Setting("AZURE_CONNECTION_TIMEOUT_SECS", parser=int),
            Setting("AZURE_URL_EXPIRATION_SECS", parser=int),
            Setting("AZURE_OVERWRITE_FILES", parser=str_to_bool),
            "AZURE_LOCATION",
            "AZURE_ENDPOINT_SUFFIX",
            "AZURE_CUSTOM_DOMAIN",
            "AZURE_CONNECTION_STRING",
            "AZURE_TOKEN_CREDENTIAL",
            "AZURE_CACHE_CONTROL",
            Setting("AZURE_OBJECT_PARAMETERS", parser=json.loads),
            "AZURE_API_VERSION",
        ],
    )


BASEROW_PUBLIC_URL = os.getenv("BASEROW_PUBLIC_URL")
if BASEROW_PUBLIC_URL:
    PUBLIC_BACKEND_URL = BASEROW_PUBLIC_URL
    PUBLIC_WEB_FRONTEND_URL = BASEROW_PUBLIC_URL
    if BASEROW_PUBLIC_URL == "http://localhost":
        print(
            "WARNING: Baserow is configured to use a BASEROW_PUBLIC_URL of "
            "http://localhost. If you attempt to access Baserow on any other hostname "
            "requests to the backend will fail as they will be from an unknown host. "
            "Please set BASEROW_PUBLIC_URL if you will be accessing Baserow "
            "from any other URL then http://localhost."
        )
else:
    PUBLIC_BACKEND_URL = os.getenv("PUBLIC_BACKEND_URL", "http://localhost:8000")
    PUBLIC_WEB_FRONTEND_URL = os.getenv(
        "PUBLIC_WEB_FRONTEND_URL", "http://localhost:3000"
    )
    if "PUBLIC_BACKEND_URL" not in os.environ:
        print(
            "WARNING: Baserow is configured to use a PUBLIC_BACKEND_URL of "
            "http://localhost:8000. If you attempt to access Baserow on any other "
            "hostname requests to the backend will fail as they will be from an "
            "unknown host."
            "Please ensure you set PUBLIC_BACKEND_URL if you will be accessing "
            "Baserow from any other URL then http://localhost."
        )
    if "PUBLIC_WEB_FRONTEND_URL" not in os.environ:
        print(
            "WARNING: Baserow is configured to use a default PUBLIC_WEB_FRONTEND_URL "
            "of http://localhost:3000. Emails sent by Baserow will use links pointing "
            "to http://localhost:3000 when telling users how to access your server. If "
            "this is incorrect please ensure you have set PUBLIC_WEB_FRONTEND_URL to "
            "the URL where users can access your Baserow server."
        )

PRIVATE_BACKEND_URL = os.getenv("PRIVATE_BACKEND_URL", "http://backend:8000")
PUBLIC_BACKEND_HOSTNAME = urlparse(PUBLIC_BACKEND_URL).hostname
PUBLIC_WEB_FRONTEND_HOSTNAME = urlparse(PUBLIC_WEB_FRONTEND_URL).hostname
PRIVATE_BACKEND_HOSTNAME = urlparse(PRIVATE_BACKEND_URL).hostname

if PUBLIC_BACKEND_HOSTNAME:
    ALLOWED_HOSTS.append(PUBLIC_BACKEND_HOSTNAME)

if PRIVATE_BACKEND_HOSTNAME:
    ALLOWED_HOSTS.append(PRIVATE_BACKEND_HOSTNAME)

FROM_EMAIL = os.getenv("FROM_EMAIL", "no-reply@localhost")
RESET_PASSWORD_TOKEN_MAX_AGE = 60 * 60 * 48  # 48 hours

ROW_PAGE_SIZE_LIMIT = int(os.getenv("BASEROW_ROW_PAGE_SIZE_LIMIT", 200))
BATCH_ROWS_SIZE_LIMIT = int(
    os.getenv("BATCH_ROWS_SIZE_LIMIT", 200)
)  # How many rows can be modified at once.

TRASH_PAGE_SIZE_LIMIT = 200  # How many trash entries can be requested at once.
ROW_COMMENT_PAGE_SIZE_LIMIT = 200  # How many row comments can be requested at once.
# How many unique row values can be requested at once.
UNIQUE_ROW_VALUES_SIZE_LIMIT = 50

# The amount of rows that can be imported when creating a table.
INITIAL_TABLE_DATA_LIMIT = None
if "INITIAL_TABLE_DATA_LIMIT" in os.environ:
    INITIAL_TABLE_DATA_LIMIT = int(os.getenv("INITIAL_TABLE_DATA_LIMIT"))

BASEROW_INITIAL_CREATE_SYNC_TABLE_DATA_LIMIT = int(
    os.getenv("BASEROW_INITIAL_CREATE_SYNC_TABLE_DATA_LIMIT", 5000)
)

MEDIA_URL_PATH = "/media/"
MEDIA_URL = os.getenv("MEDIA_URL", urljoin(PUBLIC_BACKEND_URL, MEDIA_URL_PATH))
MEDIA_ROOT = os.getenv("MEDIA_ROOT", "/baserow/media")

# Indicates the directory where the user files and user thumbnails are stored.
USER_FILES_DIRECTORY = "user_files"
USER_THUMBNAILS_DIRECTORY = "thumbnails"
BASEROW_FILE_UPLOAD_SIZE_LIMIT_MB = int(
    Decimal(os.getenv("BASEROW_FILE_UPLOAD_SIZE_LIMIT_MB", 1024 * 1024)) * 1024 * 1024
)  # ~1TB by default

EXPORT_FILES_DIRECTORY = "export_files"
EXPORT_CLEANUP_INTERVAL_MINUTES = 5
EXPORT_FILE_EXPIRE_MINUTES = 60


def get_crontab_from_env(env_var_name: str, default_crontab: str) -> crontab:
    """
    Parses a crontab from an environment variable if present or instead uses the
    default.

    Celeries crontab constructor takes the arguments in a different order than the
    actual crontab spec so we expand and re-order the arguments to match.
    """

    minute, hour, day_of_month, month_of_year, day_of_week = os.getenv(
        env_var_name, default_crontab
    ).split(" ")
    return crontab(minute, hour, day_of_week, day_of_month, month_of_year)


MIDNIGHT_CRONTAB_STR = "0 0 * * *"
BASEROW_STORAGE_USAGE_JOB_CRONTAB = get_crontab_from_env(
    "BASEROW_STORAGE_USAGE_JOB_CRONTAB", default_crontab=MIDNIGHT_CRONTAB_STR
)

ONE_AM_CRONTRAB_STR = "0 1 * * *"
BASEROW_SEAT_USAGE_JOB_CRONTAB = get_crontab_from_env(
    "BASEROW_SEAT_USAGE_JOB_CRONTAB", default_crontab=ONE_AM_CRONTRAB_STR
)

THREE_AM_CRONTAB_STR = "0 3 * * *"
BASEROW_ROW_COUNT_JOB_CRONTAB = get_crontab_from_env(
    "BASEROW_ROW_COUNT_JOB_CRONTAB", default_crontab=THREE_AM_CRONTAB_STR
)

EMAIL_BACKEND = "djcelery_email.backends.CeleryEmailBackend"

if os.getenv("EMAIL_SMTP", ""):
    CELERY_EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    # EMAIL_SMTP_USE_TLS OR EMAIL_SMTP_USE_TLS for backwards compatibility after
    # fixing #448.
    EMAIL_USE_TLS = bool(os.getenv("EMAIL_SMTP_USE_TLS", "")) or bool(
        os.getenv("EMAIL_SMPT_USE_TLS", "")
    )
    EMAIL_HOST = os.getenv("EMAIL_SMTP_HOST", "localhost")
    EMAIL_PORT = os.getenv("EMAIL_SMTP_PORT", "25")
    EMAIL_HOST_USER = os.getenv("EMAIL_SMTP_USER", "")
    EMAIL_HOST_PASSWORD = os.getenv("EMAIL_SMTP_PASSWORD", "")

    EMAIL_USE_SSL = bool(os.getenv("EMAIL_SMTP_USE_SSL", ""))
    if EMAIL_USE_SSL and EMAIL_USE_TLS:
        raise ImproperlyConfigured(
            "EMAIL_SMTP_USE_SSL and EMAIL_SMTP_USE_TLS are "
            "mutually exclusive and both cannot be set at once."
        )

    EMAIL_SSL_CERTFILE = os.getenv("EMAIL_SMTP_SSL_CERTFILE_PATH", None)
    EMAIL_SSL_KEYFILE = os.getenv("EMAIL_SMTP_SSL_KEYFILE_PATH", None)
else:
    CELERY_EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Configurable thumbnails that are going to be generated when a user uploads an image
# file.
USER_THUMBNAILS = {"tiny": [None, 21], "small": [48, 48], "card_cover": [300, 160]}

# The directory that contains the all the templates in JSON format. When for example
# the `sync_templates` management command is called, then the templates in the
# database will be synced with these files.
APPLICATION_TEMPLATES_DIR = os.path.join(BASE_DIR, "../../../templates")
# The template that must be selected when the user first opens the templates select
# modal.
# IF CHANGING KEEP IN SYNC WITH e2e-tests/wait-for-services.sh
DEFAULT_APPLICATION_TEMPLATE = "project-tracker"

MAX_FIELD_LIMIT = 1500

# If you change this default please also update the default for the web-frontend found
# in web-frontend/modules/core/module.js:55
HOURS_UNTIL_TRASH_PERMANENTLY_DELETED = int(
    os.getenv("HOURS_UNTIL_TRASH_PERMANENTLY_DELETED", 24 * 3)
)
OLD_TRASH_CLEANUP_CHECK_INTERVAL_MINUTES = 5

MAX_ROW_COMMENT_LENGTH = 10000

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# For now force the old os dependant behaviour of file uploads as users might be relying
# on it. See
# https://docs.djangoproject.com/en/3.2/releases/3.0/#new-default-value-for-the-file-upload-permissions-setting
FILE_UPLOAD_PERMISSIONS = None

MAX_FORMULA_STRING_LENGTH = 10000
MAX_FIELD_REFERENCE_DEPTH = 1000
DONT_UPDATE_FORMULAS_AFTER_MIGRATION = bool(
    os.getenv("DONT_UPDATE_FORMULAS_AFTER_MIGRATION", "")
)
EVERY_TEN_MINUTES = "*/10 * * * *"
PERIODIC_FIELD_UPDATE_TIMEOUT_MINUTES = int(
    os.getenv("BASEROW_PERIODIC_FIELD_UPDATE_TIMEOUT_MINUTES", 9)
)
PERIODIC_FIELD_UPDATE_CRONTAB = get_crontab_from_env(
    "BASEROW_PERIODIC_FIELD_UPDATE_CRONTAB", default_crontab=EVERY_TEN_MINUTES
)
PERIODIC_FIELD_UPDATE_QUEUE_NAME = os.getenv(
    "BASEROW_PERIODIC_FIELD_UPDATE_QUEUE_NAME", "export"
)

BASEROW_WEBHOOKS_MAX_CONSECUTIVE_TRIGGER_FAILURES = int(
    os.getenv("BASEROW_WEBHOOKS_MAX_CONSECUTIVE_TRIGGER_FAILURES", 8)
)
BASEROW_WEBHOOKS_MAX_RETRIES_PER_CALL = int(
    os.getenv("BASEROW_WEBHOOKS_MAX_RETRIES_PER_CALL", 8)
)
BASEROW_WEBHOOKS_MAX_PER_TABLE = int(os.getenv("BASEROW_WEBHOOKS_MAX_PER_TABLE", 20))
BASEROW_WEBHOOKS_MAX_CALL_LOG_ENTRIES = int(
    os.getenv("BASEROW_WEBHOOKS_MAX_CALL_LOG_ENTRIES", 10)
)
BASEROW_WEBHOOKS_REQUEST_TIMEOUT_SECONDS = int(
    os.getenv("BASEROW_WEBHOOKS_REQUEST_TIMEOUT_SECONDS", 5)
)
BASEROW_WEBHOOKS_ALLOW_PRIVATE_ADDRESS = bool(
    os.getenv("BASEROW_WEBHOOKS_ALLOW_PRIVATE_ADDRESS", False)
)
BASEROW_WEBHOOKS_IP_BLACKLIST = [
    ip_network(ip.strip())
    for ip in os.getenv("BASEROW_WEBHOOKS_IP_BLACKLIST", "").split(",")
    if ip.strip() != ""
]
BASEROW_WEBHOOKS_IP_WHITELIST = [
    ip_network(ip.strip())
    for ip in os.getenv("BASEROW_WEBHOOKS_IP_WHITELIST", "").split(",")
    if ip.strip() != ""
]
BASEROW_WEBHOOKS_URL_REGEX_BLACKLIST = [
    re.compile(url_regex.strip())
    for url_regex in os.getenv("BASEROW_WEBHOOKS_URL_REGEX_BLACKLIST", "").split(",")
    if url_regex.strip() != ""
]
BASEROW_WEBHOOKS_URL_CHECK_TIMEOUT_SECS = int(
    os.getenv("BASEROW_WEBHOOKS_URL_CHECK_TIMEOUT_SECS", "10")
)

# ======== WARNING ========
# Please read and understand everything at:
# https://docs.djangoproject.com/en/3.2/ref/settings/#secure-proxy-ssl-header
# before enabling this setting otherwise you can compromise your site’s security.
# This setting will ensure the "next" urls provided by the various paginated API
# endpoints will be returned with https when appropriate.
# If using gunicorn also behind the proxy you might also need to set
# --forwarded-allow-ips='*'. See the following link for more information:
# https://stackoverflow.com/questions/62337379/how-to-append-nginx-ip-to-x-forwarded
# -for-in-kubernetes-nginx-ingress-controller

if bool(os.getenv("BASEROW_ENABLE_SECURE_PROXY_SSL_HEADER", False)):
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

DISABLE_ANONYMOUS_PUBLIC_VIEW_WS_CONNECTIONS = bool(
    os.getenv("DISABLE_ANONYMOUS_PUBLIC_VIEW_WS_CONNECTIONS", "")
)

BASEROW_BACKEND_LOG_LEVEL = os.getenv("BASEROW_BACKEND_LOG_LEVEL", "INFO")
BASEROW_BACKEND_DATABASE_LOG_LEVEL = os.getenv(
    "BASEROW_BACKEND_DATABASE_LOG_LEVEL", "ERROR"
)

BASEROW_JOB_EXPIRATION_TIME_LIMIT = int(
    os.getenv("BASEROW_JOB_EXPIRATION_TIME_LIMIT", 30 * 24 * 60)  # 30 days
)
BASEROW_JOB_SOFT_TIME_LIMIT = int(
    os.getenv("BASEROW_JOB_SOFT_TIME_LIMIT", 60 * 30)  # 30 minutes
)
BASEROW_JOB_CLEANUP_INTERVAL_MINUTES = int(
    os.getenv("BASEROW_JOB_CLEANUP_INTERVAL_MINUTES", 5)  # 5 minutes
)
BASEROW_MAX_ROW_REPORT_ERROR_COUNT = int(
    os.getenv("BASEROW_MAX_ROW_REPORT_ERROR_COUNT", 30)
)
BASEROW_MAX_SNAPSHOTS_PER_GROUP = int(os.getenv("BASEROW_MAX_SNAPSHOTS_PER_GROUP", -1))
BASEROW_SNAPSHOT_EXPIRATION_TIME_DAYS = int(
    os.getenv("BASEROW_SNAPSHOT_EXPIRATION_TIME_DAYS", 360)  # 360 days
)

PERMISSION_MANAGERS = [
    "view_ownership",
    "core",
    "setting_operation",
    "staff",
    "allow_public_builder",
    "member",
    "token",
    "role",
    "basic",
]
if "baserow_enterprise" not in INSTALLED_APPS:
    PERMISSION_MANAGERS.remove("role")
if "baserow_premium" not in INSTALLED_APPS:
    PERMISSION_MANAGERS.remove("view_ownership")
if "builder" not in FEATURE_FLAGS:
    PERMISSION_MANAGERS.remove("allow_public_builder")

OLD_ACTION_CLEANUP_INTERVAL_MINUTES = os.getenv(
    "OLD_ACTION_CLEANUP_INTERVAL_MINUTES", 5
)
MINUTES_UNTIL_ACTION_CLEANED_UP = os.getenv("MINUTES_UNTIL_ACTION_CLEANED_UP", "120")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "console": {
            "format": "%(levelname)s %(asctime)s %(name)s.%(funcName)s:%(lineno)s- %("
            "message)s "
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "console",
        },
    },
    "loggers": {
        "gunicorn": {
            "level": BASEROW_BACKEND_LOG_LEVEL,
            "handlers": ["console"],
            "propagate": True,
        },
        "django": {
            "handlers": ["console"],
            "level": BASEROW_BACKEND_LOG_LEVEL,
            "propagate": True,
        },
        "django.request": {
            "handlers": ["console"],
            "level": BASEROW_BACKEND_LOG_LEVEL,
            "propagate": True,
        },
        "django.db.backends": {
            "handlers": ["console"],
            "level": BASEROW_BACKEND_DATABASE_LOG_LEVEL,
            "propagate": True,
        },
    },
    "root": {
        "handlers": ["console"],
        "level": BASEROW_BACKEND_LOG_LEVEL,
    },
}


# Now incorrectly named old variable, previously we would run `sync_templates` prior
# to starting the gunicorn server in Docker. This variable would prevent that from
# happening. Now we sync_templates in an async job triggered after migration.
# This variable if not true will now stop the async job from being triggered.
SYNC_TEMPLATES_ON_STARTUP = os.getenv("SYNC_TEMPLATES_ON_STARTUP", "true") == "true"
BASEROW_TRIGGER_SYNC_TEMPLATES_AFTER_MIGRATION = os.getenv(
    "BASEROW_TRIGGER_SYNC_TEMPLATES_AFTER_MIGRATION", None
)

if BASEROW_TRIGGER_SYNC_TEMPLATES_AFTER_MIGRATION is None:
    # If the new correctly named environment variable is not set, default to using
    # the old now incorrectly named SYNC_TEMPLATES_ON_STARTUP.
    BASEROW_TRIGGER_SYNC_TEMPLATES_AFTER_MIGRATION = SYNC_TEMPLATES_ON_STARTUP
else:
    # The new correctly named environment variable is set, so use that instead of
    # the old.
    BASEROW_TRIGGER_SYNC_TEMPLATES_AFTER_MIGRATION = (
        BASEROW_TRIGGER_SYNC_TEMPLATES_AFTER_MIGRATION == "true"
    )

BASEROW_SYNC_TEMPLATES_TIME_LIMIT = int(
    os.getenv("BASEROW_SYNC_TEMPLATES_TIME_LIMIT", 60 * 30)
)

APPEND_SLASH = False

BASEROW_DISABLE_MODEL_CACHE = bool(os.getenv("BASEROW_DISABLE_MODEL_CACHE", ""))
BASEROW_NOWAIT_FOR_LOCKS = not bool(
    os.getenv("BASEROW_WAIT_INSTEAD_OF_409_CONFLICT_ERROR", False)
)

LICENSE_AUTHORITY_CHECK_TIMEOUT_SECONDS = 10

MAX_NUMBER_CALENDAR_DAYS = 45

MIGRATION_LOCK_ID = os.getenv("BASEROW_MIGRATION_LOCK_ID", 123456)

# Indicates whether we are running the tests or not. Set to True in the test.py settings
# file used by pytest.ini
TESTS = False


for plugin in [*BASEROW_BUILT_IN_PLUGINS, *BASEROW_BACKEND_PLUGIN_NAMES]:
    try:
        mod = importlib.import_module(plugin + ".config.settings.settings")
        # The plugin should have a setup function which accepts a 'settings' object.
        # This settings object is an AttrDict shadowing our local variables so the
        # plugin can access the Django settings and modify them prior to startup.
        result = mod.setup(AttrDict(vars()))
    except ImportError as e:
        print("Could not import %s", plugin)
        print(e)
