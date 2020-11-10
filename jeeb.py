import requests
import json
from urllib.parse import urlencode


class JeebClient:

    def __init__(self, Token):
        self.TOKEN = Token
        self.JEEBURL = "https://core.jeeb.io/"
        self.Header = {"Content-Type": "application/json"}
        self.APIURL = f"{self.JEEBURL}api/payments/{self.TOKEN}/"
        self.SANDBOX = False  # Sandbox

    def Convert(self, Amount, BaseCurrency, TargetCurrency):
        Parameters = {
            "value": Amount,
            "base": BaseCurrency,
            "target": TargetCurrency
        }
        Parameters = urlencode(Parameters)
        APIURL = f"{self.JEEBURL}api/currency?{Parameters}"
        Response = requests.get(APIURL, headers=self.Header).text
        Response = json.loads(Response)
        Result = Response['result']
        # Response with 8 decimals (0.00000000)
        Result = f"{Response['result']:.8f}"
        return Result

    def Issue(self, OrderNumber, Value, Coins, Webhook, OptionalParameters={}):
        API = f"{self.APIURL}issue"
        OrderNumber = str(OrderNumber)

        Posts = {
            "orderNo": OrderNumber,
            "value": Value,
            "coins": Coins,
            "webhookUrl": Webhook,
            "allowTestNet": self.SANDBOX,
            **OptionalParameters
        }
        Posts = json.dumps(Posts)
        Response = requests.post(API, data=Posts, headers=self.Header).text
        Result = json.loads(Response)
        return Result

    def Confirm(self, Token):
        API = f"{self.APIURL}confirm"
        Post = {
            "token": Token,
        }
        Post = json.dumps(Post)
        Response = requests.post(API, data=Post, header=self.Header).text
        Response = json.loads(Response)
        return Response

    def Status(self, Token):
        API = f"{self.APIURL}status"
        Post = {
            "token": Token,
        }
        Post = json.dumps(Post)
        Response = requests.post(API, data=Post, header=self.Header).text
        Response = json.loads(Response)
        return Response
