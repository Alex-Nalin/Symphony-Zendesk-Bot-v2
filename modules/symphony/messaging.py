import json
import re
import traceback
import modules.symphony.callout as callout
import modules.botconfig as config
import modules.botlog as botlog


def SendUserIM(userIds, message, endpointVersion='v1', data=None):
    # createEP = config.SymphonyBaseURL + '/pod/v1/im/create'
    # createEP = endpointIM.substitute(host=config.SymphonyBaseURL, imVersion=endpointVersion)

    createEP = config.CreateIMEndpoint

    body = [int(uid) for uid in userIds]

    response = callout.SymphonyPOST(createEP, json.dumps(body))

    streamId = response.ResponseData.id

    if endpointVersion == 'v1':
        SendSymphonyMessage(streamId, message)
    else:
        SendSymphonyMessageV2(streamId, message, data)

def SendUserIM_noBotLog(userIds, message, endpointVersion='v1', data=None):
    # createEP = config.SymphonyBaseURL + '/pod/v1/im/create'
    # createEP = endpointIM.substitute(host=config.SymphonyBaseURL, imVersion=endpointVersion)

    createEP = config.CreateIMEndpoint

    body = [int(uid) for uid in userIds]

    response = callout.SymphonyPOST(createEP, json.dumps(body))

    streamId = response.ResponseData.id

    if endpointVersion == 'v1':
        SendSymphonyMessage_noBotLog(streamId, message)
    else:
        SendSymphonyMessageV2_noBotLog(streamId, message, data)


def SendUserIMv2(userIds, message, data=None):
    SendUserIM(userIds, message, endpointVersion='v2', data=data)

def SendUserIMv2_noBotLog(userIds, message, data=None):
    SendUserIM_noBotLog(userIds, message, endpointVersion='v2', data=data)


def SendSymphonyMessage(streamId, message: str):
    if not message.startswith('<messageML>'):
        message = FormatSymphonyMessage(message)

    messageEP = config.GetSendMessageEndpoint(streamId, config.MessageMLVersion.v1)

    bodyJSON = {"message": message, "format": "MESSAGEML"}

    botlog.LogSymphonyInfo('Sending Symphony Message | StreamId: ' + streamId + ' | Message: ' + message)
    return callout.SymphonyPOST(messageEP, json.dumps(bodyJSON))

def SendSymphonyMessage_noBotLog(streamId, message: str):
    if not message.startswith('<messageML>'):
        message = FormatSymphonyMessage(message)

    messageEP = config.GetSendMessageEndpoint(streamId, config.MessageMLVersion.v1)

    bodyJSON = {"message": message, "format": "MESSAGEML"}

    #botlog.LogSymphonyInfo('Sending Symphony Message | StreamId: ' + streamId + ' | Message: ' + message)
    return callout.SymphonyPOST(messageEP, json.dumps(bodyJSON))


def SendSymphonyMessageV2(streamId, message: str, data=None):
    if not message.startswith('<messageML>'):
        message = FormatSymphonyMessage(message)

    # messageEP = endpointRoom.substitute(host=config.SymphonyBaseURL, roomVersion='v4', streamId=streamId)
    messageEP = config.GetSendMessageEndpoint(streamId, config.MessageMLVersion.v2)

    # The data payload has to be converted to a JSON string - the MultipartEncoder won't
    # convert a dict automatically
    if data is not None:
        data = json.dumps(data)

    bodyObj = {"message": message, "data": data}

    botlog.LogSymphonyInfo('Sending Symphony Message Create V4 | StreamId: ' + streamId + ' | Message: ' + message)
    return callout.SymphonyPOSTV2(messageEP, bodyObj)


# def SendSymphonyMessageV2_data(stream_id: str, message: str, data=None, attachments: List[MessageAttachment]=None):
#
#     msg = util.FormatSymphonyMessage(message)
#     endpoint = ep.SendMessage_Endpoint(stream_id, 4)
#
#     # To send multiple attachments with the same key, we need to use a slighly different
#     # submission format for requests-toolbelt. Instead, the "fields" parameter
#     # that gets passed to the MultipartEncoder should take a list of tuples
#     # for all the parameters.
#     # https://github.com/requests/toolbelt/issues/190#issuecomment-319900108
#     body_list = [('message', msg)]
#
#     # data here is for structured objects, not attachments
#     if data is not None:
#         data = json.dumps(data)
#         body_list.append(('data', data))
#
#     # if there are attachments, we need to create a tuple for each one of the form:
#     # (filename, file_data, MIME_type)
#     # then we append those tuples to the list defined by body_list
#     # We then pass body_list to SymphonyPOSTv2. Requests-Toolbelt
#     # will create the correct multipart format
#     if attachments:
#         for att in attachments:
#             att_t = (att.Filename, att.Data, att.MIME)
#             body_list.append(('attachment', att_t))
#
#
#     response = conn.SymphonyPOSTv2(endpoint, body_list)
#
#     LogMessagePost(response, stream_id, message)
#
#     return response

def SendSymphonyMessageV2_data(streamId: str, message: str, data=None, attachments=None):

    msg = FormatSymphonyMessage(message)
    messageEP = config.GetSendMessageEndpoint(streamId, config.MessageMLVersion.v2)

    # To send multiple attachments with the same key, we need to use a slighly different
    # submission format for requests-toolbelt. Instead, the "fields" parameter
    # that gets passed to the MultipartEncoder should take a list of tuples
    # for all the parameters.
    # https://github.com/requests/toolbelt/issues/190#issuecomment-319900108
    body_list = [('message', msg)]

    # data here is for structured objects, not attachments
    if data is not None:
        data = json.dumps(data)
        body_list.append(('data', data))

    # if there are attachments, we need to create a tuple for each one of the form:
    # (filename, file_data, MIME_type)
    # then we append those tuples to the list defined by body_list
    # We then pass body_list to SymphonyPOSTv2. Requests-Toolbelt
    # will create the correct multipart format
    if attachments is not None:
        for att in attachments:
            #att_t = (att.Filename, att.Data, att.MIME)
            #body_list.append(('attachment', att_t))
            body_list.append(('attachment', att))


    response = callout.SymphonyPOSTV2(messageEP, body_list)
    return response



def SendSymphonyMessageV2_noBotLog(streamId, message: str, data=None):

    if not message.startswith('<messageML>'):
        message = FormatSymphonyMessage(message)

    # messageEP = endpointRoom.substitute(host=config.SymphonyBaseURL, roomVersion='v4', streamId=streamId)
    messageEP = config.GetSendMessageEndpoint(streamId, config.MessageMLVersion.v2)

    # The data payload has to be converted to a JSON string - the MultipartEncoder won't
    # convert a dict automatically
    if data is not None:
        data = json.dumps(data)

    bodyObj = {"message": message, "data": data}

    #botlog.LogSymphonyInfo('Sending Symphony Message Create V4 | StreamId: ' + streamId + ' | Message: ' + message)
    return callout.SymphonyPOSTV2(messageEP, bodyObj)

def SendSymphonyMessageV2_1(streamId, message: str, data=None):
    if not message.startswith('<messageML>'):
        message = FormatSymphonyMessage(message)

    # messageEP = endpointRoom.substitute(host=config.SymphonyBaseURL, roomVersion='v4', streamId=streamId)
    messageEP = config.GetSendMessageEndpoint(streamId, config.MessageMLVersion.v2)

    # The data payload has to be converted to a JSON string - the MultipartEncoder won't
    # convert a dict automatically
    if data is not None:
        data = json.dumps(data)

    bodyObj = {"message": message, "data": data}

    botlog.LogSymphonyInfo('Sending Symphony Message Create V4 | StreamId: ' + streamId + ' | Message: ' + message)
    return callout.SymphonyPOSTV2_1(messageEP, bodyObj)


def FormatSymphonyMessage(message: str):
    return "<messageML>" + message + "</messageML>"


def FormatSymphonyLink(url: str):
    return '<a href="' + url + '"/>'


def FormatSymphonyId(streamId: str):
    return re.sub("==$", "", streamId.replace("/", "_"))

def FormatDicttoMML2(jsonObj: dict) -> str:
    json_str = json.dumps(jsonObj, indent=4, separators=(',', ': ')).replace('"', '&quot;').replace('\'', '&apos;')

    json_str = "<code>" + json_str + "\n</code>"

    return json_str


def getAttchment(streamID, messageID, attachmentID):
    attEP = config.SymphonyBaseURL+'/agent/v1/stream/'+streamID+'/attachement?messageId='+messageID+'&fileId='+attachmentID
    return callout.SymphonyGET(attEP)