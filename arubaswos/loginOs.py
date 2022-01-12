import json
import requests

HTTP_URL = "http://{}/rest/v1/"
HTTPS_URL = "https://{}/rest/v1/"


def get_url(data, action):
    if data['ssl']:
        url = HTTPS_URL.format(data['ip']) + action
    else:
        url = HTTP_URL.format(data['ip']) + action
    return url

def login_os(data):
    username = data['user']
    password = data['password']
    params = {'userName': username, 'password': password}
    proxies = {'http': None, 'https': None}

    url_login = get_url(data, "login-sessions")
    response = requests.post(url_login, verify=False, data=json.dumps(params), proxies=proxies, timeout=3)
    if response.status_code == 201:
        print("Login to switch: {} is successful".format(url_login))
        session = response.json()
        data['cookie'] = session['cookie']
        return
    else:
        print("Login to switch failed")


def logout(data):
    url_login = get_url(data, "login-sessions")
    headers = {'cookie': data['cookie']}
    proxies = {'http': None, 'https': None}
    r = requests.delete(url_login, headers=headers, verify=False, proxies=proxies)
    if r.status_code == 204:
        print("Logged out!", r.status_code)
    else:
        print("Logout is not successful", r.status_code)

def send_get_request(data, action, entry_item):
    header = {'cookie': data['cookie']}
    response = requests.get(get_url(data, action), headers=header, verify=False, timeout=2)
    return response.json()[entry_item]