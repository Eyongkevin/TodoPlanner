from .base import *

ALLOWED_HOSTS = ["*"]

THIRD_PARTY_APPS = ["django_extensions"]

INSTALLED_APPS += THIRD_PARTY_APPS

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }
