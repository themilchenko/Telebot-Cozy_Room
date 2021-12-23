import config
import base64
import requests
import datetime

# making simple string using 'f-string' that makes output such as:
# de012964ebf2451e9497483bcfc5c8f3: 5dfa56d1c86341318c482f05327c81a0
clientCredits = f'{config.CLIENT_ID}: {config.CLIENT_SECRET}'

# encoding 'client_credits' string into bits and then encoding it into base64
# base64 type of encoding quite more secure way of encoding than simple bitwise encoding
clientCreditsB64 = base64.b64encode(clientCredits.encode())

# formats that Spotify requires to use:
tokenData = {'grant_type': 'client_credentials'}
# using decode method to have value not in bytes but encoded string in base 64
tokenHeaders = {'Authorization': f'Basic {clientCreditsB64.decode()}'}

postRequest = requests.post(config.TOKEN_URL, data=tokenData, headers=tokenHeaders)
requestValid = postRequest.status_code in range(200, 299)

if requestValid:
    # here we have response of our post request in JSON format
    responseData = postRequest.json()
    accessToken = responseData['tokenAccess']
    expiresIn = responseData['expiresIn']
    # time of the request
    requestTime = datetime.datetime.now()
    tempExpires = requestTime + datetime.timedelta(seconds=expiresIn)


# -------------------------------------------------------------------------------------------- #


class SpotifyAPI(object):
    accToken = None
    accessTokenExp = None  # datetime.datetime,now()
    clientID = None
    clientSecret = None
    tokenURL = config.TOKEN_URL

    def __init__(self, clientID, clientSec):
        self.clientID = clientID
        self.clientSec = clientSec

    def getClientCreditsB64(self):
        clientCredits = f'{config.CLIENT_ID}: {config.CLIENT_SECRET}'
        clientCreditsB64 = base64.b64encode(clientCredits.encode())
        return clientCreditsB64

    def getTokenHeaders(self):
        clientCreditsB64 = self.getClientCreditsB64().decode()
        return {'Authorization': f'Basic {clientCreditsB64}'}

    def getTokenData(self):
        return {'grant_type': 'client_credentials'}

    def extractAccessToken(self):
        return
