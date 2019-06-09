import pytest

from watchtower import get_check_job
from watchtower.model import check


def test_check_record(client, app):
    ch = check('https://www.google.com/', 200, 123)
    with app.app_context():
        ch.db_insert()
    
    rsp = client.get('/')
    assert b'https://www.google.com/' in rsp.data
    assert b'200' in rsp.data
    assert b'123' in rsp.data

def test_check_repr():
    ch = check('https://www.google.com/', 200, 123)
    assert str(ch) == '<check: https://www.google.com/, code: 200, resp time: 123, notes:None>'

@pytest.mark.parametrize(
    'address,pattern,code,ok,notes',
    [('https://www.google.com/', 'search', 200, True, ''),
    ('https://bioinfo.pl/', 'cookies', 200, False, 'Pattern does not match'),
    ('https://www.nope.io/', '', 0, False, 'ConnectionError'),
])
def test_check_scenarios(address, pattern, code, ok, notes):
    checker = get_check_job(None)
    checks = checker([(address, pattern)], False)
    ch = checks[address]
    assert ch.address == address
    assert ch.code == code
    assert ch.ok == ok
    if notes:
        assert notes in ch.notes
