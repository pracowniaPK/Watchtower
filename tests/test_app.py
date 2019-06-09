from watchtower import create_app
from watchtower.model import check


def test_app_factory():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing

def test_show_index(client):
    rsp = client.get('/')
    assert b'Watchtower' in rsp.data

def test_site_counter(client, app):
    checks = []
    checks.append(check('https://bioinfo.pl/', 200, 123))
    checks.append(check('https://www.google.com/', 200, 123))
    checks.append(check('https://www.nope.io/', 0, 0))
    for i in range(3):
        with app.app_context():
            checks[i].db_insert()

    rsp = client.get('/')
    assert b'2 websites up, 1 warnings' in rsp.data
