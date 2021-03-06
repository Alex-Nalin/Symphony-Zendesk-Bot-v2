from datetime import datetime
from datetime import timedelta
import json
import requests
from jose import jwt
import datetime
from requests_toolbelt import MultipartEncoder
import traceback
import types

import modules.botconfig as config
import modules.botlog as botlog

agentSession = requests.Session()
agentSession.cert = config.BotCertificate

agentV2Session = requests.Session()
agentV2Session.cert = config.BotCertificate

v2LastAuth: datetime = None
v2SessionToken = None
v2KeyAuthToken = None


def GetSessionToken():
    #botlog.LogConsoleInfo(config.SessionAuthEP)
    ##return GetSymphonyAuthToken(config.SessionAuthEP)
    if config.authType == 'rsa':
        return GetRSAAuthToken(config.RsaSessionAuthEP)
    else: # Cert Auth
        return GetSymphonyAuthToken(config.SessionAuthEP)


def GetKeyManagerToken():
    #botlog.LogConsoleInfo(config.KeyManagerEP)
    ##return GetSymphonyAuthToken(config.KeyManagerEP)

    if config.authType == 'rsa':
        return GetRSAAuthToken(config.RsaKeyAuthEP)
    else: # Cert Auth
        return GetSymphonyAuthToken(config.KeyManagerEP)

def GetRSAAuthToken(authEndpoint):
    """
    Get the session token by calling API using jwt token
    """

    data = {
        'token': create_jwt()
    }
    response = agentSession.post(authEndpoint, json=data)

    if response.status_code == 200:
        data = json.loads(response.text)
        return data['token']
    else:
        return ''


def create_jwt():
    """
    Create a jwt token with payload dictionary. Encode with
    RSA private key using RS512 algorithm
    :return: A jwt token valid for < 290 seconds
    """
    with open(config.RsaPrivateKeyPath, 'r') as f:
        content = f.readlines()
        private_key = ''.join(content)
        expiration_date = int(datetime.datetime.now(datetime.timezone.utc)
                              .timestamp() + (5*58))
        payload = {
            'sub': config.BotUserName,
            'exp': expiration_date
        }
        encoded = jwt.encode(payload, private_key, algorithm='RS512')
        f.close()
        return encoded



def GetSymphonyAuthToken(authEndpoint):
    response = SymphonyREST('AUTH', authEndpoint, None)
    return response.ResponseData.token


def BuildHeaders(sessionToken, keyAuthToken, contentType="application/json"):
    RESTheaders = {
        "sessionToken": sessionToken,
        "keyManagerToken": keyAuthToken,
        "Content-Type": contentType,
        "User-Agent": "SymphonyZendeskBot (Alex Nalin - API Engineer - alex.nalin@symphony.com)"
    }

    return RESTheaders

def SymphonyReAuth():
    global agentSession

    sessionToken = GetSessionToken()
    keyAuthToken = GetKeyManagerToken()

    # RESTHeaders = {"sessionToken": sessionToken, "keyManagerToken": keyAuthToken,
    #                "Content-Type": "application/json"}

    RESTHeaders = BuildHeaders(sessionToken, keyAuthToken)

    # Attempting to use requests.Session
    agentSession.headers.update(RESTHeaders)


def SymphonyGET(endpoint):
    return SymphonyREST('GET', endpoint, None)

def SymphonyPOST(endpoint, body):
    return SymphonyREST('POST', endpoint, body)

def SymphonyPOSTV2(endpoint, body):
    return SymphonyREST('POSTV2', endpoint, body)

def SymphonyPOSTV2_1(endpoint, body):
    return SymphonyREST('POSTV2_1', endpoint, body)

def SymphonyPOSTv4(endpoint, body, *attach_data):
    return SymphonyRESTv4('POST', endpoint, body, *attach_data)


def SymphonyREST(method, endpoint, body):
    retVal = SymphonyAgentResponse()

    # Allowing for reauth from the async process
    if method != 'AUTH' and 'sessionToken' not in agentSession.headers:
        SymphonyReAuth()

    try:
        if method == 'GET':
            response = agentSession.get(endpoint)
        elif method == 'POST':
            response = agentSession.post(endpoint, data=body)
        elif method == 'POSTV2':
            response = PostV2(endpoint, body)
        # elif method == 'POSTV2_data':
        #     response = PostV2_data(endpoint, body, attachments)
        elif method == 'POSTV2_1':
            response = PostV2_1(endpoint, body)
        elif method == 'AUTH':
            response = agentSession.post(endpoint)
        else:
            raise MethodNotImplementedException(method + ' is not yet implemented.')

        retVal.ResponseText = response.text
        retVal.ResponseCode = response.status_code

        if response.status_code == 200:
            retVal.Success = True
            retVal.ParseResponseJSON()
        elif response.status_code // 100 == 2:  # Any other 200 code, not success but don't throw exception
            retVal.Success = True
        else:
            response.raise_for_status()

    except requests.exceptions.HTTPError as httpex:
        errorStr = "Symphony REST Exception (http): " + str(httpex)
        botlog.LogConsoleInfo("Response Code: " + str(response.status_code))
        botlog.LogConsoleInfo("Response Message: " + response.text)
        retVal.ErrorMessage = errorStr
        stackTrace = 'Stack Trace: ' + ''.join(traceback.format_stack())
        botlog.LogSymphonyError(errorStr)
        botlog.LogSymphonyError(stackTrace)

    except requests.exceptions.RequestException as connex:
        errorStr = "Symphony REST Exception (connection - Status Code " + str(response.status_code) + \
                   "): " + str(connex)
        retVal.ErrorMessage = errorStr
        stackTrace = 'Stack Trace: ' + ''.join(traceback.format_stack())
        botlog.LogSymphonyError(errorStr)
        botlog.LogSymphonyError(stackTrace)

    except Exception as ex:
        errorStr = "Symphony REST Exception (system): " + str(ex)
        retVal.ErrorMessage = errorStr
        stackTrace = 'Stack Trace: ' + ''.join(traceback.format_stack())
        botlog.LogSystemError(errorStr)
        botlog.LogSystemError(stackTrace)

    finally:
        return retVal

def SymphonyRESTv4(method, endpoint, body, *attach_data):
    # Clean up the body to ensure no funky values
    body = body.replace("&", "&amp;")

    data_unparsed = {"field1": "blah blah"}
    data = json.dumps(data_unparsed)

    if attach_data:
        dataObj = {"message": body, "attachment": attach_data[0]}
    else:
        dataObj = {"message": body}
    # dataObj = [('message', body), ('attachment', ('test_full.jpg', attachment_file, 'image/jpeg'))]
    encoder = MultipartEncoder(fields=dataObj)
    RESTHeaders = {"Content-Type": encoder.content_type}
    # RESTHeaders = {"Content-Type": "multipart/form-data"}
    agentSession.headers.update(RESTHeaders)
    return agentSession.post(endpoint, data=encoder)
    #return agentSession.post(endpoint, body)


def PostV2(endpoint, body):
    global v2LastAuth
    global v2SessionToken
    global v2KeyAuthToken
    global agentV2Session

    if v2SessionToken is None or v2LastAuth is None or datetime.datetime.now() > v2LastAuth + timedelta(days=2):
        v2SessionToken = GetSessionToken()
        v2KeyAuthToken = GetKeyManagerToken()
        v2LastAuth = datetime.datetime.now()

    encoder = MultipartEncoder(fields=body)
    v2Headers = BuildHeaders(v2SessionToken, v2KeyAuthToken, encoder.content_type)

    agentV2Session.headers.update(v2Headers)

    return agentV2Session.post(endpoint, data=encoder)


def PostV2_data(endpoint, body):
    global v2LastAuth
    global v2SessionToken
    global v2KeyAuthToken
    global agentV2Session

    if v2SessionToken is None or v2LastAuth is None or datetime.datetime.now() > v2LastAuth + timedelta(days=2):
        v2SessionToken = GetSessionToken()
        v2KeyAuthToken = GetKeyManagerToken()
        v2LastAuth = datetime.datetime.now()

    encoder = MultipartEncoder(fields=body)
    v2Headers = BuildHeaders(v2SessionToken, v2KeyAuthToken, encoder.content_type)

    agentV2Session.headers.update(v2Headers)

    return agentV2Session.post(endpoint, data=encoder)


# Does not work
# I believe the problem is the Content-Type header, which does not include the boundary
# statement. If I am prepared to build the boundary myself, I might be able to get this
# to work without the requests_toolbelt package
def PostV2_1(endpoint, body):
    import io
    ph = io.StringIO("")

    tempSession = requests.Session()
    tempSession.cert = config.BotCertificate

    tempSessionToken = GetSessionToken()
    tempKeyAuthToken = GetKeyManagerToken()

    tempHeaders = {"sessionToken": tempSessionToken, "keyManagerToken": tempKeyAuthToken,
                   "Content-Type": "multipart/form-data"}

    tempSession.headers.update(tempHeaders)

    return tempSession.post(endpoint, data=body, files=ph)


class SymphonyAgentResponse:
    def __init__(self):
        self.Success = False
        self.ResponseText = ''
        self.ResponseCode = 0
        self.ErrorMessage = ''
        self.ResponseData = {}

    def ParseResponseJSON(self):
        self.ResponseData = json.loads(self.ResponseText, object_hook=lambda d: types.SimpleNamespace(**d))


class JSONData:
    def __init__(self, jsonStr):
        self.__dict__ = json.loads(jsonStr)


class MethodNotImplementedException(Exception):
    pass

