import pytest
from connection import Connection

@pytest.fixture
def instance():
    return Connection(headers = { 'cookie': 'over18=1;' })

def test_instance(instance):
    assert isinstance(instance, Connection)

@pytest.mark.parametrize(
    'url, expected',
    [
        ('https://www.ptt.cc/bbs/Beauty/index.html', True),
        ('https://ptt.cc/bbs/Beauty/index.html', True),
        ('https://ptt.cc/bbs/Beauty/index132.html', True),
        ('https://www.ptt.cc/bbs/Beauty/index.htmlasd', False),
        ('https://www.ptt.cc/bbs/Beauty/indexasd.html', False),
        ('https://www.ptt.cc/bbs/Gossiping/M.1119243418.A.790.html', True),
        ('https://ptt.cc/bbs/movie/M.1617387691.A.3B2.html', True),
        ('https://www.ptt.cc/bbs/Tech_Job/B.1617427229.A.2FB.html', False),
        ('https://www.ptt.cc/bbs/Tech_Job/M.167427229.A.2FB.html', False),
        ('https://www.ptt.cc/bbs/Tech_Job/M.1617427229.B.2FB.html', False)
    ]
)
def test__check_url(instance, url, expected):
    assert instance._check_url(url) == expected

def test_looking_for_board(instance):
    instance.get('https://www.ptt.cc/bbs/Beauty/index3614.html')
    assert instance._status == {
            'headers': {
                'cookie': 'over18=1;' 
                },
            'request_url': 'https://www.ptt.cc/bbs/Beauty/index3614.html',
            'response_code': 200,
            'looking_for': ('Beauty', 'board')
        }

def test_looking_for_article(instance):
    instance.get(
        'https://www.ptt.cc/bbs/Beauty/M.1617413202.A.764.html',
        headers = {}
        )
    assert instance._status['looking_for'] == ('Beauty', 'article')

def test__reset_status(instance):
    instance.get('https://www.ptt.cc/bbs/Beauty/M.1617413202.A.764.html')
    instance._reset_status()
    assert instance._status == {
            'headers': {
                'cookie': 'over18=1;' 
                },
            'request_url': None,
            'response_code': None,
            'looking_for': None
        }

@pytest.mark.parametrize(
    'url',
    [
        'https://www.ptt.cc/bbs/Beauty/index.htmlasd',
        'https://www.ptt.cc/bbs/Beauty/index12312.html'
    ]
)
def test_get_exception(instance, url):
    with pytest.raises(Exception):
        instance.get(url)