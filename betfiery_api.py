import json
import requests

URL_API = "https://api.betfiery.com"


class Browser(object):

    def __init__(self):
        self.response = None
        self.headers = None
        self.session = requests.Session()

    def set_headers(self, headers=None):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/87.0.4280.88 Safari/537.36"
        }
        if headers:
            for key, value in headers.items():
                self.headers[key] = value

    def get_headers(self):
        return self.headers

    def send_request(self, method, url, **kwargs):
        return self.session.request(method, url, **kwargs)


class BetFieryAPI(Browser):

    def __init__(self, username=None, password=None):
        super().__init__()
        self.proxies = None
        self.token = None
        self.wallet_id = None
        self.username = username
        self.password = password
        self.set_headers()
        self.headers = self.get_headers()

    def auth(self):
        data = {
            "account": self.username,
            "grecaptcha_token": "1",
            "password": self.password
        }
        self.response = self.send_request("POST",
                                          f"{URL_API}/user/login",
                                          json=data,
                                          headers=self.headers)
        print(self.response.text)
        if not self.response.json().get("error"):
            self.token = self.response.json()

        return self.response.json()

    def get_recaptcha(self):
        data = {
            "k": "6Lddn5IgAAAAADqy5RAoZ_ySpPb_OAKXM_ZGVUQG",
        }
        self.headers["content-type"] = "application/x-protobuffer"
        self.headers["cookie"] = "_GRECAPTCHA=09AMjm62U6Tn43pQOomPhXohsPc7b" \
                                 "-YmHaeX4omFRn8hXCrYpCGXwjtV6yf9vwNtZIZwrb7gFjmwyvQFZxgvOA0TE "
        self.headers["referer"] = "https://www.recaptcha.net/recaptcha/api2/anchor?ar" \
                                  "=1&k=6Lddn5IgAAAAADqy5RAoZ_ySpPb_OAKXM_ZGVUQG&co=" \
                                  "aHR0cHM6Ly9iZXRmaWVyeS5jb206NDQz&hl=pt-BR&v=5JGZgxkK" \
                                  "we0uOXDdUvSaNtk_&size=invisible&cb=uwn8p783yczm"
        self.response = self.send_request("POST",
                                          "https://www.recaptcha.net/recaptcha/api2/reload?k"
                                          "-6Lddn5IgAAAAADqy5RAoZ_ySpPb_OAKXM_ZGVUQG",
                                          data=data,
                                          headers=self.headers)
        print(self.response.url)

        return self.response

    def get_last_crashs(self):
        self.response = self.send_request("POST",
                                          f"{URL_API}/game/crash/list/ship",
                                          headers=self.headers)
        if self.response:
            result = {
                "items": [{"color": "preto" if float(i["progress"]) < 2 else "verde", "value": i["progress"]}
                          for i in self.response.json()["data"]]}
            return result
        return False

    def get_last_doubles(self):
        self.response = self.send_request("POST",
                                          f"{URL_API}/game/double/list",
                                          headers=self.headers)
        if self.response:
            result = {
                "items": [
                    {"color": "branco" if i["roll"] == "wild"
                     else "vermelho" if i["roll"].isdigit() and int(i["roll"]) < 8
                     else "preto", "value": i["roll"].isdigit() and int(i["roll"]) if i["roll"] != "wild" else 0}
                    for i in self.response.json()["data"]["list"]]}
            return result
        return False


if __name__ == "__main__":
    bfa = BetFieryAPI("user",
                      "senha")  # Não é necessário fazer login para obter os últimos crashs

    # print(bfa.get_recaptcha().text)
    # login = bfa.auth()
    # print(login)

    doubles = bfa.get_last_doubles()
    print(json.dumps(doubles, indent=4))

    # crashs = bfa.get_last_crashs()
    # print(json.dumps(crashs, indent=4))
