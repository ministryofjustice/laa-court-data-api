config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'structFormatter': {
            'class': 'logging.Formatter',
            'format': '%(message)s'
        }
    },
    'handlers': {
        'consoleHandler': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'structFormatter'
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
