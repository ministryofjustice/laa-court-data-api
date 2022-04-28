from asgi_correlation_id import correlation_id_filter

config = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'correlation_id': {'()': correlation_id_filter(uuid_length=32)}
    },
    'formatters': {
        'basicFormatter': {
            'class': 'logging.Formatter',
            'format': '%(asctime)s [%(correlation_id)s] loglevel=%(levelname)-6s logger=%(name)s %(funcName)s() %(message)s'
        }
    },
    'handlers': {
        'consoleHandler': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'basicFormatter',
            'filters': ['correlation_id']
        }
    },
    'loggers': {
        'root': {
            'handlers': ['consoleHandler'],
            'level': 'INFO',
            'propagate': False,
            'qualname': 'root'
        },
        '__main__': {
            'handlers': ['consoleHandler'],
            'level': 'INFO',
            'propagate': False,
            'qualname': '__main__'
        },
        'laa_court_data_api_app': {
            'handlers': ['consoleHandler'],
            'level': 'INFO',
            'propagate': False,
            'qualname': 'laa_court_data_api_app'
        }
    }
}
