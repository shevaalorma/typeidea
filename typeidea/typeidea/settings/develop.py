from .base import *

DEBUG = True

INSTALLED_APPS += [
    # 'debug_toolbar',
    # 'pympler',
    # 'debug_toolbar_line_profiler',
    'silk',
]

MIDDLEWARE += [
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
    'silk.middleware.SilkyMiddleware',
]

INTERNAL_IPS = ['127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'typeidea_db',
        'USER':'root',
        'PASSWORD':'qwe123',
        'HOST':'127.0.0.1',
        'PORT':3306,
        'CONN_MAX_AGE':5*60,
        'OPTIONS':{'charset':'utf8mb4'}
    }
}

DEBUG_TOOLBAR_CONFIG = {'JQUERY_URL': r"http://code.jquery.com/jquery-2.1.1.min.js"}

DEBUG_TOOLBAR_PANELS = [
    # 'djdt_flamegraph.FlamegraphPanel',
    # 'pympler.panels.MemoryPanel',
    'debug_toolbar_line_profiler.panel.ProfilingPanel',
]
