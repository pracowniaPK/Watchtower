sites_list = [
    ('https://www.google.com/', 'search'),
    ('https://nope.oi/', 'stuff'),
    ('https://www.yahoo.com/', 'qwerasdf'),
    ('http://www.error418.net/', 'teapot'),
]

class Config:
    DEVELOPMENT = True
    DEBUG = True
    SECRET_KEY='dev'

    JOBS = [
        {
            'id': 'check_job',
            'func': 'app:check_job',
            'args': [sites_list],
            'trigger': 'interval',
            'seconds': 60
        }
    ]
    SCHEDULER_API_ENABLED = True
