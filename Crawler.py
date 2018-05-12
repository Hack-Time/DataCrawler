# -*- coding: UTF-8 -*-
import requests

api = "http://open.test.seiue.com/api/v1/oauth"
clientID = "368912"
clientSecret = "KuGCMO-WBu6ciGEV_Mchp_44-X2TSCJ3omWxatfj"

token = ""

def fetchToken(api, clientID, clientSecret):
    headers = {"grant_type": "client_credentials", "client_id":clientID, "client_secret":clientSecret}
    response = requests.post(api, data = headers)
    json = response.json()

    token = json["access_token"]
    return token

token = fetchToken(api, clientID, clientSecret)
