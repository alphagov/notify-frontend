from werkzeug.http import parse_cookie


def get_cookie_by_name(response, name):
    cookies = response.headers.getlist('Set-Cookie')
    for cookie in cookies:
        if name in parse_cookie(cookie):
            return parse_cookie(cookie)
    return None
