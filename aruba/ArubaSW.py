import json
import requests

HTTP_URL = "http://{}/rest/v1/"
HTTPS_URL = "https://{}/rest/v1/"


class ArubaSW:
    def __init__(self, data):
        self.data = data

    def get_url(self, action):
        if self.data['ssl']:
            url = HTTPS_URL.format(self.data['ip']) + action
        else:
            url = HTTP_URL.format(self.data['ip']) + action
        return url

    def login(self):
        username = self.data['user']
        password = self.data['password']
        params = {'userName': username, 'password': password}
        proxies = {'http': None, 'https': None}

        url_login = self.get_url(self.data, "login-sessions")
        response = requests.post(url_login, verify=False, data=json.dumps(params), proxies=proxies, timeout=3)
        if response.status_code == 201:
            print("Login to switch: {} is successful".format(url_login))
            session = response.json()
            self.data['cookie'] = session['cookie']
            return
        else:
            print("Login to switch failed")


    def logout(self):
        url_login = self.get_url(self.data, "login-sessions")
        headers = {'cookie': self.data['cookie']}
        proxies = {'http': None, 'https': None}
        r = requests.delete(url_login, headers=headers, verify=False, proxies=proxies)
        if r.status_code == 204:
            print("Logged out!", r.status_code)
        else:
            print("Logout is not successful", r.status_code)

    def send_request(self, action, type="GET", entry_item):
        if type
        header = {'cookie': self.data['cookie']}
        response = requests.get(self.get_url(self.data, action), headers=header, verify=False, timeout=2)
        return response.json()