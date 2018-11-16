import requests
import os
import codecs
import json
import modules.botlog as botlog
import modules.botconfig as botconfig
import modules.crypto as crypto
import modules.symphony.messaging as messaging
import http.client
from googleapiclient.discovery import build
from Data.access import AccessFile
import ast
import modules.symphony.callout as callout
import modules.symphony.messagereader as symreader
import modules.utility_date_time as utdt

#Grab the config.json Symphony parameters
_configPath = os.path.abspath('modules/command/default.json')
with codecs.open(_configPath, 'r', 'utf-8-sig') as json_file:
    _config = json.load(json_file)

_configPathdDefault = os.path.abspath('config.json')
with codecs.open(_configPathdDefault, 'r', 'utf-8-sig') as json_file:
        _configDef = json.load(json_file)

_configPathZendesk = os.path.abspath('modules/plugins/Zendesk/config.json')
with codecs.open(_configPathZendesk, 'r', 'utf-8-sig') as json_file:
    _configZen = json.load(json_file)

def SymphonyZendeskBotHelp(messageDetail):
    botlog.LogSymphonyInfo("###############")
    botlog.LogSymphonyInfo("Bot Call - Help")
    botlog.LogSymphonyInfo("###############")

    commandCallerUID = messageDetail.FromUserId

    connComp = http.client.HTTPSConnection(_configDef['symphonyinfo']['pod_hostname'])
    sessionTok = callout.GetSessionToken()

    headersCompany = {
        'sessiontoken': sessionTok,
        'cache-control': "no-cache"
    }

    connComp.request("GET", "/pod/v3/users?uid=" + commandCallerUID, headers=headersCompany)

    resComp = connComp.getresponse()
    dataComp = resComp.read()
    data_raw = str(dataComp.decode('utf-8'))
    data_dict = ast.literal_eval(data_raw)

    dataRender = json.dumps(data_dict, indent=2)
    d_org = json.loads(str(dataRender))

    for index_org in range(len(d_org["users"])):
        firstName = str(d_org["users"][index_org]["firstName"])
        lastName = str(d_org["users"][index_org]["lastName"])
        displayName = str(d_org["users"][index_org]["displayName"])
        companyName = str(d_org["users"][index_org]["company"])
        userID = str(d_org["users"][index_org]["id"])


    if companyName in _configDef['AuthCompany']['PodList']:

        streamType = ""
        streamType = (messageDetail.ChatRoom.Type)

        if streamType == "IM":

            try:

                _moreconfigPath = os.path.abspath('modules/command/default.json')

                with codecs.open(_moreconfigPath, 'r', 'utf-8-sig') as json_file:
                    _moreconfig = json.load(json_file)

                header = "<b class =\"tempo-text-color--blue\">Symphony Zendesk Bot Help</b> For more information, please consult <b>Symphony Team</b><br/>"
                # ---------

                table_body = "<table style='border-collapse:collapse;border:2px solid black;table-layout:auto;max-width:100%;box-shadow: 5px 5px'><thead><tr style='background-color:#4D94FF;color:#ffffff;font-size:1rem' class=\"tempo-text-color--white tempo-bg-color--black\">" \
                             "<td style='border:1px solid blue;border-bottom: double blue;text-align:center;max-width:15%'>COMMAND</td>" \
                             "<td style='border:1px solid blue;border-bottom: double blue;text-align:center;max-width:15%'>PARAMETER</td>" \
                             "<td style='border:1px solid blue;border-bottom: double blue;text-align:center;max-width:20%'>SAMPLE</td>" \
                             "<td style='border:1px solid blue;border-bottom: double blue;text-align:center;max-width:25%'>DESCRIPTION</td>" \
                             "<td style='border:1px solid blue;border-bottom: double blue;text-align:center;max-width:12.5%'>CATEGORY</td>"\
                             "<td style='border:1px solid blue;border-bottom: double blue;text-align:center;max-width:12.5%'>PERMISSION</td>" \
                             "</tr></thead><tbody>"

                # Seems we need to set this to a colour the first time to work
                perm_bg_color = "green"
                for index in range(len(_configZen["commands"])):

                    caterory = _configZen["commands"][index]["category"]

                    if caterory == "Zendesk":
                        caterory_bg_color = "cyan"
                    if caterory == "Zendesk/General":
                        caterory_bg_color = "purple"
                    if caterory == "General Bot command":
                        caterory_bg_color = "blue"
                    if caterory == "Miscellaneous Bot command":
                        caterory_bg_color = "yellow"

                    permission = _configZen["commands"][index]["permission"]

                    if permission == "Bot Admin":
                        perm_bg_color = "red"
                    if permission == "Zendesk Agent":
                        perm_bg_color = "orange"
                    if permission == "All":
                        perm_bg_color = "green"
                    if permission == "Zendesk Agent/Zendesk End-user":
                        perm_bg_color = "yellow"

                    table_body += "<tr>" \
                                  "<td style='border:1px solid black;text-align:left'>" + _configZen["commands"][index]["helptext"] + "</td>" \
                                  "<td style='border:1px solid black;text-align:left'>" + _configZen["commands"][index]["param"] + "</td>" \
                                  "<td style='border:1px solid black;text-align:left'>" + _configZen["commands"][index]["example"] + "</td>" \
                                  "<td style='border:1px solid black;text-align:left'>" + _configZen["commands"][index]["description"] + "</td>" \
                                  "<td class=\"tempo-bg-color--" + caterory_bg_color + " tempo-text-color--white\">" + _configZen["commands"][index]["category"] + "</td>" \
                                  "<td class=\"tempo-bg-color--" + perm_bg_color + " tempo-text-color--white\">" + _configZen["commands"][index]["permission"] + "</td>" \
                                  "</tr>"

                _moreconfigPath = os.path.abspath('modules/command/default.json')
                with codecs.open(_moreconfigPath, 'r', 'utf-8-sig') as json_file:
                    _moreconfig = json.load(json_file)

                for index in range(len(_moreconfig["commands"])):

                    caterory = _moreconfig["commands"][index]["category"]

                    if caterory == "Zendesk":
                        caterory_bg_color = "cyan"
                    if caterory == "Zendesk/General":
                        caterory_bg_color = "purple"
                    if caterory == "General Bot command":
                        caterory_bg_color = "blue"
                    if caterory == "Miscellaneous Bot command":
                        caterory_bg_color = "yellow"

                    permission = str(_moreconfig["commands"][index]["permission"])

                    if permission == "Bot Admin":
                        perm_bg_color = "red"
                    if permission == "Zendesk Agent":
                        perm_bg_color = "orange"
                    if permission == "All":
                        perm_bg_color = "green"
                    if permission == "Zendesk Agent/Zendesk End-user":
                        perm_bg_color = "yellow"

                    table_body += "<tr>" \
                                  "<td style='border:1px solid black;text-align:left'>" + _moreconfig["commands"][index]["helptext"] + "</td>" \
                                  "<td style='border:1px solid black;text-align:left'>" + _moreconfig["commands"][index]["param"] + "</td>" \
                                  "<td style='border:1px solid black;text-align:left'>" + _moreconfig["commands"][index]["example"] + "</td>" \
                                  "<td style='border:1px solid black;text-align:left'>" + _moreconfig["commands"][index]["description"] + "</td>" \
                                  "<td class=\"tempo-bg-color--" + caterory_bg_color + " tempo-text-color--white\">" + _moreconfig["commands"][index]["category"] + "</td>" \
                                  "<td class=\"tempo-bg-color--" + perm_bg_color + " tempo-text-color--white\">" + _moreconfig["commands"][index]["permission"] + "</td>" \
                                  "</tr>"
                else:
                    pass

                table_body += "</tbody></table>"

                table_body = "<card iconSrc=\"https://thumb.ibb.co/csXBgU/Symphony2018_App_Icon_Mobile.png\" accent=\"tempo-bg-color--blue\"><header>" + header + "</header><body>" + table_body + "</body></card>"

                messaging.SendSymphonyMessageV2_noBotLog(messageDetail.StreamId, table_body)

            except:
                return messageDetail.ReplyToChat("Please check that all the config files are in the right place. I am sorry, I was working on a different task, can you please retry")
        else:
            return messageDetail.ReplyToChat("For SupportBot /help, please IM me directly")

def botStream(messageDetail):
    botlog.LogSymphonyInfo("###########################")
    botlog.LogSymphonyInfo("Bot Call - Bot Stream Check")
    botlog.LogSymphonyInfo("###########################")

    try:
        try:
            commandCallerUID = messageDetail.FromUserId

            connComp = http.client.HTTPSConnection(_configDef['symphonyinfo']['pod_hostname'])
            sessionTok = callout.GetSessionToken()

            headersCompany = {
                'sessiontoken': sessionTok,
                'cache-control': "no-cache"
            }

            connComp.request("GET", "/pod/v3/users?uid=" + commandCallerUID, headers=headersCompany)

            resComp = connComp.getresponse()
            dataComp = resComp.read()
            data_raw = str(dataComp.decode('utf-8'))
            data_dict = ast.literal_eval(data_raw)

            dataRender = json.dumps(data_dict, indent=2)
            d_org = json.loads(dataRender)

            for index_org in range(len(d_org["users"])):
                firstName = str(d_org["users"][index_org]["firstName"])
                lastName = str(d_org["users"][index_org]["lastName"])
                displayName = str(d_org["users"][index_org]["displayName"])
                companyName = str(d_org["users"][index_org]["company"])
                userID = str(d_org["users"][index_org]["id"])

                botlog.LogSymphonyInfo(str(firstName) + " " + str(lastName) + " from Company/Pod name: " + str(companyName) + " with UID: " + str(userID))
                callerCheck = (firstName + " " + lastName + " - " + displayName + " - " + companyName + " - " + str(userID))

        except:
            return messageDetail.ReplyToChat("Cannot validate user access")

        if callerCheck in (_configDef['AuthUser']['AdminList']):

            message = (messageDetail.Command.MessageText)
            message_split = message.split()
            summary = ""

            all = False
            room = False
            im = False

            for index in range(len(message_split)):
                if message_split[index] == "all" or message_split[index] == "All" or message_split[index] == "ALL":
                    all = True
                    body = {"includeInactiveStreams": 'false'}
                elif message_split[index] == "room" or message_split[index] == "Room" or message_split[index] == "ROOM":
                    room = True
                    body = {"streamTypes": [{"type": "ROOM"}], "includeInactiveStreams": 'false'}
                elif message_split[index] == "im" or message_split[index] == "Im" or message_split[index] == "IM":
                    im = True
                    body = {"streamTypes": [{"type": "IM"}, {"type": "MIM"}], "includeInactiveStreams": 'false'}
                else:
                    summary += message_split[index] + " "
            summary = summary.lstrip().rstrip()

            try:
                createEP = botconfig.SymphonyBaseURL + '/pod/v1/streams/list'
                response = callout.SymphonyPOST(createEP, json.dumps(body))
                r = json.loads(response.ResponseText)
            except:
                return messageDetail.ReplyToChat("Please use IM or Room or All after the command /checkStream. For example: /checkStream IM")

            table_body = ""
            table_header = "<table style='border-collapse:collapse;border:2px solid black;table-layout:auto;width:100%;box-shadow: 5px 5px'><thead><tr style='background-color:#4D94FF;color:#ffffff;font-size:1rem' class=\"tempo-text-color--black tempo-bg-color--black\">" \
                           "<td style='border:1px solid blue;border-bottom: double blue;width:30%;text-align:center'>STREAM ID</td>" \
                           "<td style='border:1px solid blue;border-bottom: double blue;width:5%;text-align:center'>CROSS POD</td>" \
                           "<td style='border:1px solid blue;border-bottom: double blue;width:5%;text-align:center'>ACTIVE</td>" \
                           "<td style='border:1px solid blue;border-bottom: double blue;width:5%;text-align:center'>TYPE</td>" \
                           "<td style='border:1px solid blue;border-bottom: double blue;width:50%;text-align:center'>ROOM NAME OR MEMBER ID</td>" \
                           "</tr></thead><tbody>"

            for index in range(len(r)):
                count = (len(r))
                botStreamID = r[index]["id"]
                crossPod = r[index]["crossPod"]
                active = r[index]["active"]
                streamType = r[index]["streamType"]["type"]
                if im:
                    attribute = r[index]["streamAttributes"]["members"]
                elif room:
                    attribute = r[index]["roomAttributes"]["name"]
                elif all:
                    try:
                        attribute = r[index]["streamAttributes"]["members"]
                    except:
                        attribute = r[index]["roomAttributes"]["name"]

                table_body += "<tr>" \
                              "<td style='border:1px solid black;text-align:center'>" + str(botStreamID) + "</td>" \
                              "<td style='border:1px solid black;text-align:center'>" + str(crossPod) + "</td>" \
                              "<td style='border:1px solid black;text-align:center'>" + str(active) + "</td>" \
                              "<td style='border:1px solid black;text-align:center'>" + str(streamType) + "</td>" \
                              "<td style='border:1px solid black;text-align:center'>" + str(attribute) + "</td>" \
                              "</tr>"

            table_body += "</tbody></table>"
            reply = table_header + table_body

            return messageDetail.ReplyToChatV2_noBotLog(
                "<card iconSrc =\"https://thumb.ibb.co/csXBgU/Symphony2018_App_Icon_Mobile.png\" accent=\"tempo-bg-color--blue\"><header>Please find the result below. Total number of stream with the Bot <b>" + str(
                    count) + "</b> </header><body>" + reply + "</body></card>")

        else:
            return messageDetail.ReplyToChat("You aren't authorised to use this command.")
    except:
        #return messageDetail.ReplyToChat("I am sorry, I was working on a different task, can you please retry")

        try:
            try:
                commandCallerUID = messageDetail.FromUserId

                connComp = http.client.HTTPSConnection(_configDef['symphonyinfo']['pod_hostname'])
                sessionTok = callout.GetSessionToken()

                headersCompany = {
                    'sessiontoken': sessionTok,
                    'cache-control': "no-cache"
                }

                connComp.request("GET", "/pod/v3/users?uid=" + commandCallerUID, headers=headersCompany)

                resComp = connComp.getresponse()
                dataComp = resComp.read()
                data_raw = str(dataComp.decode('utf-8'))
                data_dict = ast.literal_eval(data_raw)

                dataRender = json.dumps(data_dict, indent=2)
                d_org = json.loads(dataRender)

                for index_org in range(len(d_org["users"])):
                    firstName = str(d_org["users"][index_org]["firstName"])
                    lastName = str(d_org["users"][index_org]["lastName"])
                    displayName = str(d_org["users"][index_org]["displayName"])
                    companyName = str(d_org["users"][index_org]["company"])
                    userID = str(d_org["users"][index_org]["id"])

                    botlog.LogSymphonyInfo(str(firstName) + " " + str(lastName) + " from Company/Pod name: " + str(
                        companyName) + " with UID: " + str(userID))
                    callerCheck = (firstName + " " + lastName + " - " + displayName + " - " + companyName + " - " + str(
                        userID))

            except:
                return messageDetail.ReplyToChat("Cannot validate user access")

            if callerCheck in (_configDef['AuthUser']['AdminList']):

                message = (messageDetail.Command.MessageText)
                message_split = message.split()
                summary = ""

                all = False
                room = False
                im = False

                for index in range(len(message_split)):
                    if message_split[index] == "all" or message_split[index] == "All" or message_split[index] == "ALL":
                        all = True
                        body = {"includeInactiveStreams": 'false'}
                    elif message_split[index] == "room" or message_split[index] == "Room" or message_split[
                        index] == "ROOM":
                        room = True
                        body = {"streamTypes": [{"type": "ROOM"}], "includeInactiveStreams": 'false'}
                    elif message_split[index] == "im" or message_split[index] == "Im" or message_split[index] == "IM":
                        im = True
                        body = {"streamTypes": [{"type": "IM"}, {"type": "MIM"}], "includeInactiveStreams": 'false'}
                    else:
                        summary += message_split[index] + " "
                summary = summary.lstrip().rstrip()

                try:
                    createEP = botconfig.SymphonyBaseURL + '/pod/v1/streams/list'
                    response = callout.SymphonyPOST(createEP, json.dumps(body))
                    r = json.loads(response.ResponseText)
                except:
                    return messageDetail.ReplyToChat(
                        "Please use IM or Room or All after the command /checkStream. For example: /checkStream IM")

                table_body = ""
                table_header = "<table style='border-collapse:collapse;border:2px solid black;table-layout:auto;width:100%;box-shadow: 5px 5px'><thead><tr style='background-color:#4D94FF;color:#ffffff;font-size:1rem' class=\"tempo-text-color--black tempo-bg-color--black\">" \
                               "<td style='border:1px solid blue;border-bottom: double blue;width:30%;text-align:center'>STREAM ID</td>" \
                               "<td style='border:1px solid blue;border-bottom: double blue;width:5%;text-align:center'>CROSS POD</td>" \
                               "<td style='border:1px solid blue;border-bottom: double blue;width:5%;text-align:center'>ACTIVE</td>" \
                               "<td style='border:1px solid blue;border-bottom: double blue;width:5%;text-align:center'>TYPE</td>" \
                               "<td style='border:1px solid blue;border-bottom: double blue;width:50%;text-align:center'>ROOM NAME OR MEMBER ID</td>" \
                               "</tr></thead><tbody>"

                for index in range(len(r)):
                    count = (len(r))
                    botStreamID = r[index]["id"]
                    crossPod = r[index]["crossPod"]
                    active = r[index]["active"]
                    streamType = r[index]["streamType"]["type"]
                    if im:
                        attribute = r[index]["streamAttributes"]["members"]
                    elif room:
                        attribute = r[index]["roomAttributes"]["name"]
                    elif all:
                        try:
                            attribute = r[index]["streamAttributes"]["members"]
                        except:
                            attribute = r[index]["roomAttributes"]["name"]

                    table_body += "<tr>" \
                                  "<td style='border:1px solid black;text-align:center'>" + str(botStreamID) + "</td>" \
                                                                                                               "<td style='border:1px solid black;text-align:center'>" + str(
                        crossPod) + "</td>" \
                                    "<td style='border:1px solid black;text-align:center'>" + str(active) + "</td>" \
                                                                                                            "<td style='border:1px solid black;text-align:center'>" + str(
                        streamType) + "</td>" \
                                      "<td style='border:1px solid black;text-align:center'>" + str(attribute) + "</td>" \
                                                                                                                 "</tr>"

                table_body += "</tbody></table>"
                reply = table_header + table_body

                return messageDetail.ReplyToChatV2_noBotLog(
                    "<card iconSrc =\"https://thumb.ibb.co/csXBgU/Symphony2018_App_Icon_Mobile.png\" accent=\"tempo-bg-color--blue\"><header>Please find the result below. Total number of stream with the Bot <b>" + str(
                        count) + "</b> </header><body>" + reply + "</body></card>")

            else:
                return messageDetail.ReplyToChat("You aren't authorised to use this command.")
        except:
            return messageDetail.ReplyToChat("I am sorry, I was working on a different task, can you please retry")

def botMessageBlast(messageDetail):
    botlog.LogSymphonyInfo("##########################")
    botlog.LogSymphonyInfo("Bot Call: Send Bot Message")
    botlog.LogSymphonyInfo("##########################")

    try:
        try:
            commandCallerUID = messageDetail.FromUserId

            connComp = http.client.HTTPSConnection(_configDef['symphonyinfo']['pod_hostname'])
            sessionTok = callout.GetSessionToken()

            headersCompany = {
                'sessiontoken': sessionTok,
                'cache-control': "no-cache"
            }

            connComp.request("GET", "/pod/v3/users?uid=" + commandCallerUID, headers=headersCompany)

            resComp = connComp.getresponse()
            dataComp = resComp.read()
            data_raw = str(dataComp.decode('utf-8'))
            data_dict = ast.literal_eval(data_raw)

            dataRender = json.dumps(data_dict, indent=2)
            d_org = json.loads(dataRender)

            for index_org in range(len(d_org["users"])):
                firstName = str(d_org["users"][index_org]["firstName"])
                lastName = str(d_org["users"][index_org]["lastName"])
                displayName = str(d_org["users"][index_org]["displayName"])
                companyName = str(d_org["users"][index_org]["company"])
                userID = str(d_org["users"][index_org]["id"])

                botlog.LogSymphonyInfo(str(firstName) + " " + str(lastName) + " from Company/Pod name: " + str(companyName) + " with UID: " + str(userID))
                callerCheck = (firstName + " " + lastName + " - " + displayName + " - " + companyName + " - " + str(userID))

        except:
            return messageDetail.ReplyToChat("Cannot validate user access")

        if callerCheck in (_configDef['AuthUser']['AdminList']):

            message = (messageDetail.Command.MessageText)
            message_split = message.split()
            summary = ""

            check = len(message_split)

            if check == 1:
                return messageDetail.ReplyToChat("Please make sure to include a message")
            else:

                for index in range(len(message_split)):
                    if message_split[index] == "all" or message_split[index] == "All" or message_split[index] == "ALL":
                        body = {"includeInactiveStreams": 'false'}
                    elif message_split[index] == "room" or message_split[index] == "Room" or message_split[index] == "ROOM":
                        body = {"streamTypes": [{"type": "ROOM"}], "includeInactiveStreams": 'false'}
                    elif message_split[index] == "im" or message_split[index] == "Im" or message_split[index] == "IM":
                        body = {"streamTypes": [{"type": "IM"}, {"type": "MIM"}], "includeInactiveStreams": 'false'}
                    else:
                        summary += message_split[index] + " "
                summary = summary.lstrip().rstrip()
                # print(summary)

                try:
                    createEP = botconfig.SymphonyBaseURL + '/pod/v1/streams/list'
                    response = callout.SymphonyPOST(createEP, json.dumps(body))
                    r = json.loads(response.ResponseText)
                    #print("response: " + str(r))
                except:
                    return messageDetail.ReplyToChat("Please use IM or Room or All as well as a comment to send, after the command /botMessage. For example: /botMessage IM The bot has been updated")

                for index in range(len(r)):
                    try:
                        messaging.SendSymphonyMessage(r[index]["id"], summary)
                    except:
                        botlog.LogSystemInfo(
                            "The stream is not valid anymore, maybe the bot is no longer connected with the user")
        else:
            return messageDetail.ReplyToChat("You aren't authorised to use this command.")
    except:
        return messageDetail.ReplyToChat("I am sorry, I was working on a different task, can you please retry")

# def shutdownBot(messageDetail):
#     botlog.LogSymphonyInfo("######################")
#     botlog.LogSymphonyInfo("Bot Call: Shutdown Bot")
#     botlog.LogSymphonyInfo("######################")
#
#     try:
#         try:
#             commandCallerUID = messageDetail.FromUserId
#
#             connComp = http.client.HTTPSConnection(_configDef['symphonyinfo']['pod_hostname'])
#             sessionTok = callout.GetSessionToken()
#
#             headersCompany = {
#                 'sessiontoken': sessionTok,
#                 'cache-control': "no-cache"
#             }
#
#             connComp.request("GET", "/pod/v3/users?uid=" + commandCallerUID, headers=headersCompany)
#
#             resComp = connComp.getresponse()
#             dataComp = resComp.read()
#             data_raw = str(dataComp.decode('utf-8'))
#             data_dict = ast.literal_eval(data_raw)
#
#             dataRender = json.dumps(data_dict, indent=2)
#             d_org = json.loads(dataRender)
#
#             for index_org in range(len(d_org["users"])):
#                 firstName = d_org["users"][index_org]["firstName"]
#                 lastName = d_org["users"][index_org]["lastName"]
#                 displayName = d_org["users"][index_org]["displayName"]
#                 companyName = d_org["users"][index_org]["company"]
#                 userID = str(d_org["users"][index_org]["id"])
#
#                 botlog.LogSymphonyInfo(firstName + " " + lastName + " from Company/Pod name: " + str(companyName) + " with UID: " + str(userID))
#                 callerCheck = (firstName + " " + lastName + " - " + displayName + " - " + companyName + " - " + str(userID))
#
#         except:
#             return messageDetail.ReplyToChat("Cannot validate user access")
#
#         if callerCheck in (_configDef['AuthUser']['AdminList']):
#
#             message = (messageDetail.Command.MessageText)
#             message_split = message.split()
#             summary = ""
#             noMessage = (str(len(message_split)))
#
#             if noMessage == "0":
#                 messageDetail.ReplyToSender("Shutting down Symphony Zendesk Bot now.")
#                 botlog.LogSystemInfo("Shutdown command received from " + messageDetail.Sender.Email)
#                 exit(0)
#
#             for index in range(len(message_split)):
#
#                 if message_split[index] == "all" or message_split[index] == "All" or message_split[index] == "ALL":
#                     body = {"includeInactiveStreams": 'false'}
#                 elif message_split[index] == "room" or message_split[index] == "Room" or message_split[index] == "ROOM":
#                     body = {"streamTypes": [{"type": "ROOM"}], "includeInactiveStreams": 'false'}
#                 elif message_split[index] == "im" or message_split[index] == "Im" or message_split[index] == "IM":
#                     body = {"streamTypes": [{"type": "IM"}, {"type": "MIM"}], "includeInactiveStreams": 'false'}
#                 else:
#                     summary += message_split[index] + " "
#             summary = summary.lstrip().rstrip()
#             # print(summary)
#
#             try:
#                 createEP = botconfig.SymphonyBaseURL + '/pod/v1/streams/list'
#                 response = callout.SymphonyPOST(createEP, json.dumps(body))
#                 r = json.loads(response.ResponseText)
#             except:
#                 return messageDetail.ReplyToChat(
#                     "Please use IM or Room or All as well as a comment to send, after the command /botMessage. For example: /BotMessage IM The bot has been updated")
#
#             for index in range(len(r)):
#                 try:
#                     messaging.SendSymphonyMessage(r[index]["id"], summary)
#                 except:
#                     botlog.LogSystemInfo("The stream is not valid anymore, maybe the bot is no longer connected with the user")
#
#             messageDetail.ReplyToSender("Shutting down Symphony Zendesk Bot now.")
#             botlog.LogSystemInfo("Shutdown command received from " + messageDetail.Sender.Email)
#             exit(0)
#
#         else:
#             return messageDetail.ReplyToChat("You aren't authorised to use this command.")
#     except:
#         return messageDetail.ReplyToChat("I am sorry, I was working on a different task, can you please retry")


def SendStatusCheck(messageDetail):
    botlog.LogSymphonyInfo("#############################")
    botlog.LogSymphonyInfo("Bot Call: Check Status of Bot")
    botlog.LogSymphonyInfo("#############################")

    commandCallerUID = messageDetail.FromUserId

    connComp = http.client.HTTPSConnection(_configDef['symphonyinfo']['pod_hostname'])
    sessionTok = callout.GetSessionToken()

    headersCompany = {
        'sessiontoken': sessionTok,
        'cache-control': "no-cache"
    }

    connComp.request("GET", "/pod/v3/users?uid=" + commandCallerUID, headers=headersCompany)

    resComp = connComp.getresponse()
    dataComp = resComp.read()
    data_raw = str(dataComp.decode('utf-8'))
    data_dict = ast.literal_eval(data_raw)

    dataRender = json.dumps(data_dict, indent=2)
    d_org = json.loads(str(dataRender))

    for index_org in range(len(d_org["users"])):
        firstName = str(d_org["users"][index_org]["firstName"])
        lastName = str(d_org["users"][index_org]["lastName"])
        displayName = str(d_org["users"][index_org]["displayName"])
        companyName = str(d_org["users"][index_org]["company"])
        userID = str(d_org["users"][index_org]["id"])

    if companyName in _configDef['AuthCompany']['PodList']:

        import random

        caller_raw = messageDetail.Sender.Name
        caller_split = str(caller_raw).split(" ")
        callername = caller_split[0]

        replies = ["I'm up! I'm up! " + callername, "Five by Five " + callername, "Ready to serve " + callername, "Lets do something productive " + callername + "?", "Listening...",
                   "Who's asking?", "Can I <i>help</i> you " + callername + "?", "Who disturbs my slumber?!", "Eat your heart out, Siri.",
                   "On your marks, get set, go!", "More work?", "Ready for action " + callername]

        randReply = True

        if len(messageDetail.Command.UnnamedParams) > 0:
            index = messageDetail.Command.UnnamedParams[0]

            if index.isnumeric():
                indexNum = int(index)

                if indexNum < len(replies):
                    messageDetail.ReplyToChat(replies[indexNum])
                    randReply = False

        if randReply:
            #messageDetail.ReplyToChat(random.choice(replies) +  callername)
            messageDetail.ReplyToChat(random.choice(replies))