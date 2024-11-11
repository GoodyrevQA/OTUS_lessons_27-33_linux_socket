import requests
import re
import pytest
import sys


host = "127.0.0.1"
port = 26131



def test_response_format(host=host, port=port):
    r = requests.get(f'http://{host}:{port}')
    assert r.status_code == 200
    headers = r.text.split('\r\n')
    assert headers[0] == 'Request Method: GET'
    assert re.match(r"Request Source: \('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', \d+\)", headers[1]) is not None
    assert headers[2] == 'Response Status: 200 OK'


print(test_response_format())
def test_default_headers(host=host, port=port):
    r = requests.get(f'http://{host}:{port}')
    for h in r.request.headers.items():
        assert f'{h[0]}: {h[1]}' in r.text


def test_custom_header(host=host, port=port):
    key, val = 'MyHeader', 'Agr'
    r = requests.get(f'http://{host}:{port}', headers={key: val})
    assert f'{key}: {val}' in r.text


@pytest.mark.parametrize('code, expected_code', [
    (200, 200),
    (201, 201),
    (404, 404),
    (503, 503),
    ('a', 200),
    ('', 200),
])
def test_status_code(code, expected_code, host=host, port=port):
    r = requests.get(f'http://{host}:{port}/?status={code}')
    assert r.status_code == expected_code


def test_status_second_parameter(host=host, port=port):
    r = requests.get(f'http://{host}:{port}/?a=1&status=500')
    assert r.status_code == 500


def test_post_method(host=host, port=port):
    r = requests.post(f'http://{host}:{port}')
    assert 'Request Method: POST' in r.text


def test_server_alive(host=host, port=port):
    for r in range(2):
        r = requests.get(f'http://{host}:{port}')
        assert r.status_code == 200