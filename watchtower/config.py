sites_list = [
    ('https://www.google.com/', 'search'),
    ('https://nope.oi/', 'stuff'),
    ('https://bioinfo.pl/', 'BioInfoBank Institute'),
    ('https://www.yahoo.com/', 'qwerasdf'),
    ('https://www.google.com/teapot', 'teapot'),
    ('http://127.0.0.1:5000/timeout', 'late'),
]

class Config:
    DEVELOPMENT = True
    DEBUG = True
    SECRET_KEY='dev'
