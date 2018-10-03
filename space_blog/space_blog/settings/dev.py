from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '&uu8g44$=smbo$8aj!aaxjfrfjti&8!9-tx(v94)pf$+sb*uxb'


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


try:
    from .base import *
except ImportError:
    pass
