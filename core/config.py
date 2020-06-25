from ..core import app_config

API_PREFIX = app_config('prefix',  cast=str)
APP_NAME = app_config('app_name',  cast=str)
APP_VERSION = app_config('version',  cast=str)

# =============mysql==============
DB_TYPE = ''
DB_NAME = ''
DB_USER = ''
DB_PASSWORD = ''
DB_HOST = ''
DB_PORT = ''

# =============logger================


