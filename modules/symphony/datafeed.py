import traceback
import sys
import time

import modules.botconfig as config
import modules.botlog as botlog
import modules.symphony.callout as callout
import modules.symphony.messagedetail as msg
import modules.symphony.stream as stream
import modules.symphony.user as user

import modules.symphony.messaging as messaging
import os
import codecs
import json
#from Data.wordcloud import WordCloud
import random


#Grab the config.json main parameters
_configPathdDefault = os.path.abspath('config.json')

with codecs.open(_configPathdDefault, 'r', 'utf-8-sig') as json_file:
        _configDef = json.load(json_file)


def CreateDataFeed():
    datafeedEP = config.SymphonyBaseURL + '/agent/v1/datafeed/create'
    #datafeedEP = config.SymphonyBaseURL + '/agent/v4/datafeed/create'
    #time.sleep(5)
    return callout.SymphonyPOST(datafeedEP, None).ResponseData.id

## Implementation of V4
# def CreateDataFeed():
#     datafeedEP = config.SymphonyBaseURL + '/agent/v4/datafeed/create'
#     #time.sleep(5)
#     response = callout.SymphonyPOST(datafeedEP, None).ResponseData.id
#     return response

def PollDataFeed(datafeedId):
    datafeedEP = config.SymphonyBaseURL + '/agent/v2/datafeed/' + datafeedId + '/read'
    #datafeedEP = config.SymphonyBaseURL + '/agent/v4/datafeed/' + datafeedId + '/read'

    response = callout.SymphonyGET(datafeedEP)

    # Messages coming from the API are formatted as an array of JSON objects
    # Thus, I need to break up the array, parse the individual objects, and pass
    # the list of python objects back to the engine
    messageItems = []
    if response.Success:
        for respItem in response.ResponseData:
            #Hopefully this will

            try:
##########
# V 1/2
                if respItem.v2messageType and respItem.v2messageType == 'V2Message':
                    detail = msg.MessageDetail(respItem)
                    detail.Sender = user.GetSymphonyUserDetail(detail.FromUserId)
                    detail.ChatRoom = stream.GetStreamInfo(respItem.streamId)
                    botlog.LogSymphonyInfo(detail.GetConsoleLogLine())

                    if detail.Sender and detail.Sender.IsValidSender:
                        detail.InitiateCommandParsing()

##########
# V4
#                 if respItem.type and respItem.type == 'MESSAGESENT':
#                     detail = msg.MessageDetail(respItem)
#                     # if detail.externalRecipients: return
#                     if detail.externalRecipients == "true": return []
#                     detail.Sender = user.GetSymphonyUserDetail(detail.FromUserId)
#                     detail.ChatRoom = stream.GetStreamInfo(respItem.payload.messageSent.message.stream.streamId)
#                     botlog.LogSymphonyInfo(detail.GetConsoleLogLine())
#
#                     if detail.Sender and detail.Sender.IsValidSender:
#                         detail.InitiateCommandParsing()

##########

                    messageItems.append(detail)
                elif respItem.v2messageType != 'V2Message':
                    botlog.LogConsoleInfo('Non-chat Message Type: ' + respItem.v2messageType)
                else:
                    botlog.LogConsoleInfo('Non-chat Message Type: unknown')

            except SystemExit:
                botlog.LogConsoleInfo('Exiting Symphony Zendesk Bot.')
                #messaging.SendSymphonyMessage(_configDef['BotStreamForPing'], "Exiting Symphony Zendesk Bot.")
            except Exception as ex:
                errorStr = "Symphony REST Exception (system): " + str(ex)
                #messaging.SendSymphonyMessage(_configDef['BotStreamForPing'], "Symphony REST Exception (system): " + str(ex))
                # stackTrace = 'Stack Trace: ' + ''.join(traceback.format_stack())
                exInfo = sys.exc_info()
                stackTrace = 'Stack Trace: ' + ''.join(traceback.format_exception(exInfo[0], exInfo[1], exInfo[2]))
                botlog.LogSystemError(errorStr)
                botlog.LogSystemError(stackTrace)
                botlog.LogConsoleInfo(response.ResponseText)
                #messaging.SendSymphonyMessage(_configDef['BotStreamForPing'], response.ResponseText)


    elif response.ResponseCode == 204:
        return []
    else:
        botlog.LogConsoleInfo("datafeed.py error - Response Code: " + str(response.ResponseCode))
        botlog.LogConsoleInfo("Response Message: " + response.ResponseText)
        #messaging.SendSymphonyMessage(_configDef['BotStreamForPing'], "datafeed.py error - Response Code: " + str(response.ResponseCode) + " Response Message: " + response.ResponseText)

        # if the response is not successful, return None. This way, I can tell the datafeed call was bad
        # and attempt to reconnect to the server.
        return None

    return messageItems

