import sys
import json
import datetime
import traceback
import urllib.parse
import urllib.request

from . import config


def update_token(func):
    def wrapper(*args, **kwargs):
        expires_time = config['base'].get('expires_time')
        expires_time = datetime.datetime.strptime(
            expires_time, '%Y-%m-%d %H:%M:%S') if expires_time else None
        if (expires_time is None) or (datetime.datetime.now() >= expires_time):
            url = config['base']['token_url']
            data = {
                'grant_type': 'client_credential',
                'appid': config['base']['appid'],
                'secret': config['base']['appsecret']}
            url += urllib.parse.urlencode(data)
            with urllib.request.urlopen(url) as f:
                result = json.loads(f.read().decode())
            now = datetime.datetime.now()
            expires_time = (now + datetime.timedelta(hours=2)).\
                strftime('%Y-%m-%d %H:%M:%S')
            config['base'].update({'access_token': result['access_token']})
            config['base'].update({'expires_time': expires_time})
        return func(*args, **kwargs)
    return wrapper


@update_token
def send_msg(openid, url, a, b, c, d, e, f):
    data = json.dumps({
        'touser': openid,
        'template_id': config['template']['exception_id'],
        'url': url,
        'data': {
            'keyword1': {
                'value': a,
                'color': '#173177'
            },
            'keyword2': {
                'value': b,
                'color': '#173177'
            },
            'keyword3': {
                'value': c,
                'color': '#173177'
            },
            'keyword4': {
                'value': d,
                'color': '#173177'
            },
            'keyword5': {
                'value': e,
                'color': '#173177'
            },
            'keyword6': {
                'value': f,
                'color': '#173177'
            },
        }
    }).encode()
    url = config['template']['send']
    url += config['base']['access_token']
    with urllib.request.urlopen(url, data) as f:
        print('send_msg result: {}'.format(f.read().decode()))


def output_wechat():
    from . import config
    exc_type, exc_value, exc_tb = sys.exc_info()
    exc_type_msg = exc_type.__name__ if exc_type else exc_type
    exc_tbs = sorted(
        [e for e in traceback.extract_tb(exc_tb)],
        key=lambda e: len(e.filename))
    exc_tb = exc_tbs[0] if exc_tbs else None
    exc_tb = exc_tb if exc_tb else None
    for user in eval(config['base']['maintainer']):
        send_msg(
            user,
            config['template']['url'],
            exc_type_msg,
            str(exc_value) if exc_value else None,
            *exc_tb
        ) if exc_type_msg or exc_value or exc_tb else None
