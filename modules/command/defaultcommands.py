import requests
import os
import codecs
import json
import re
import modules.botlog as botlog
import modules.botconfig as botconfig
import modules.crypto as crypto
import modules.symphony.messaging as messaging
import http.client
from googleapiclient.discovery import build
from Data.access import AccessFile
from Data.dictionary import AcronymsDictionary
import ast
import modules.symphony.callout as callout
import modules.symphony.messagereader as symreader
import modules.utility_date_time as utdt
import pdfkit

#from Data.tasker import Tasker

from requests_toolbelt import MultipartEncoder
import requests
import mimetypes

# Init task variables
# searchOrgTicketorg = ""
# searchOrgTicketstream_id = ""
# searchOrgTicketweekday = ""
# searchOrgTickethour = ""
# searchOrgTicketmin = ""

searchOrgTicketorg = []
searchOrgTicketstream_id = []
searchOrgTicketweekday = []
searchOrgTickethour = []
searchOrgTicketmin = []

task = ""
taskIndex = ""


#Grab the config.json Symphony parameters
# _configPath = os.path.abspath('modules/command/default.json')
_configPath = os.path.abspath('modules/command/defaultForHelp.json')
with codecs.open(_configPath, 'r', 'utf-8-sig') as json_file:
    _config = json.load(json_file)

_configPathdDefault = os.path.abspath('config.json')
with codecs.open(_configPathdDefault, 'r', 'utf-8-sig') as json_file:
        _configDef = json.load(json_file)

_configPathZendesk = os.path.abspath('modules/plugins/Zendesk/config.json')
with codecs.open(_configPathZendesk, 'r', 'utf-8-sig') as json_file:
    _configZen = json.load(json_file)

### FOR USER LEVEL HELP CUSTOMI ###

_configPathZendeskAdmin = os.path.abspath('modules/plugins/Zendesk/configAdmin.json')
with codecs.open(_configPathZendeskAdmin, 'r', 'utf-8-sig') as json_file:
    _configZenAdmin = json.load(json_file)

_configPathZendeskAccess = os.path.abspath('modules/plugins/Zendesk/configAccess.json')
with codecs.open(_configPathZendeskAccess, 'r', 'utf-8-sig') as json_file:
    _configZenAccess = json.load(json_file)

_configPathZendeskINT = os.path.abspath('modules/plugins/Zendesk/configINT.json')
with codecs.open(_configPathZendeskINT, 'r', 'utf-8-sig') as json_file:
    _configZenINT = json.load(json_file)

_configPathZendeskEXT = os.path.abspath('modules/plugins/Zendesk/configEXT.json')
with codecs.open(_configPathZendeskEXT, 'r', 'utf-8-sig') as json_file:
    _configZenEXT = json.load(json_file)

#Symphony API call Config/header
connComp = http.client.HTTPSConnection(_configDef['symphonyinfo']['pod_hostname'])
sessionTok = callout.GetSessionToken()

headersCompany = {
    'sessiontoken': sessionTok,
    'cache-control': "no-cache"
}

def remove_emoji(emoji):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\u200d"
                               u"\u2640-\u2642"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', emoji.decode("utf-8"))

def SymphonyZendeskBotHelp(messageDetail):
    botlog.LogSymphonyInfo("###############")
    botlog.LogSymphonyInfo("Bot Call - Help")
    botlog.LogSymphonyInfo("###############")

    numberCheck = 0
    backColor = _configDef['tableBackColor']

    try:
        commandCallerUID = messageDetail.FromUserId

        connComp = http.client.HTTPSConnection(_configDef['symphonyinfo']['pod_hostname'])
        sessionTok = callout.GetSessionToken()
        keyMan = callout.GetKeyManagerToken()

        headersCompany = {
            'sessiontoken': sessionTok,
            'cache-control': "no-cache"
        }

        connComp.request("GET", "/pod/v3/users?uid=" + commandCallerUID, headers=headersCompany)

        resComp = connComp.getresponse()
        dataComp = resComp.read()
        data_raw = str(dataComp.decode('utf-8'))
        #data_dict = ast.literal_eval(data_raw)
        data_dict = json.loads(str(data_raw))

        dataRender = json.dumps(data_dict, indent=2)
        d_org = json.loads(str(dataRender))
        botlog.LogSymphonyInfo(str(d_org))

        for index_org in range(len(d_org["users"])):
            firstName = str(d_org["users"][index_org]["firstName"])
            botlog.LogSymphonyInfo(str(firstName))
            lastName = str(d_org["users"][index_org]["lastName"])
            botlog.LogSymphonyInfo(str(lastName))
            displayName = str(d_org["users"][index_org]["displayName"])
            botlog.LogSymphonyInfo(str(displayName))
            #companyName = d_org["users"][index_org]["company"]
            companyNameTemp = d_org["users"][index_org]["company"]
            companyTemp = str(companyNameTemp).replace("&", "&amp;").replace("<", "&lt;").replace('"', "&quot;").replace("'", "&apos;").replace(">", "&gt;")
            companyName = str(companyTemp)
            botlog.LogSymphonyInfo(str(companyName))
            userID = str(d_org["users"][index_org]["id"])
            botlog.LogSymphonyInfo(str(userID))
    except:
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
            # data_dict = ast.literal_eval(data_raw)
            data_dict = json.loads(str(data_raw))

            dataRender = json.dumps(data_dict, indent=2)
            d_org = json.loads(str(dataRender))
            botlog.LogSymphonyInfo(str(d_org))

            for index_org in range(len(d_org["users"])):
                firstName = str(d_org["users"][index_org]["firstName"])
                lastName = str(d_org["users"][index_org]["lastName"])
                displayName = str(d_org["users"][index_org]["displayName"])
                #companyName = d_org["users"][index_org]["company"]
                companyNameTemp = d_org["users"][index_org]["company"]
                companyTemp = str(companyNameTemp).replace("&", "&amp;").replace("<", "&lt;").replace('"', "&quot;").replace("'", "&apos;").replace(">", "&gt;")
                companyName = str(companyTemp)
                userID = str(d_org["users"][index_org]["id"])
        except:
            botlog.LogSymphonyInfo("I was not able to validate the user access, please try again")

    botlog.LogSymphonyInfo(str(firstName) + " " + str(lastName) + " (" + str(displayName) + ") from Company/Pod name: " + str(companyName) + " with UID: " + str(userID))
    callerCheck = (str(firstName) + " " + str(lastName) + " - " + str(displayName) + " - " + str(companyName) + " - " + str(userID))


    ########### FOR ADMIN OF THE BOT - HELP FILE - SHOWS ALL COMMANDS:

    if callerCheck in _configDef['AuthUser']['AdminList']:
    # if callerCheck in AccessFile:
    # if companyName in _configDef['AuthCompany']['PodList']:

        streamType = ""
        streamType = (messageDetail.ChatRoom.Type)

        if streamType == "IM":
            #try:

            _moreconfigPath = os.path.abspath('modules/command/defaultForBotAdminHelp.json')

            with codecs.open(_moreconfigPath, 'r', 'utf-8-sig') as json_file:
                _moreconfig = json.load(json_file)

            header = "<b class =\"tempo-text-color--blue\">Symphony Zendesk Bot Help</b> For more information, please consult <b>Symphony Team</b> (You are a Bot Admin) <br/>- For Feedback use <b><hash tag=\"SupportBotFeedback\"/></b><br/> - For Bug use <b><hash tag=\"SupportBotBug\"/></b><br/>"
            # ---------

            table_body = "<table style='border-collapse:collapse;border:2px solid black;table-layout:auto;max-width:100%;box-shadow: 5px 5px'><thead><tr style='background-color:#4D94FF;color:#ffffff;font-size:1rem' class=\"tempo-text-color--white tempo-bg-color--black\">" \
                         "<td style='border:1px solid blue;border-bottom: double blue;text-align:center;max-width:15%'>COMMAND</td>" \
                         "<td style='border:1px solid blue;border-bottom: double blue;text-align:center;max-width:15%'>PARAMETER</td>" \
                         "<td style='border:1px solid blue;border-bottom: double blue;text-align:center;max-width:20%'>SAMPLE</td>" \
                         "<td style='border:1px solid blue;border-bottom: double blue;text-align:center;max-width:25%'>DESCRIPTION</td>" \
                         "<td style='border:1px solid blue;border-bottom: double blue;text-align:center;max-width:12.5%'>CATEGORY</td>" \
                         "<td style='border:1px solid blue;border-bottom: double blue;text-align:center;max-width:12.5%'>PERMISSION</td>" \
                         "</tr></thead><tbody>"

            # Seems we need to set this to a colour the first time to work
            perm_bg_color = "green"
            for index in range(len(_configZenAdmin["commands"])):
                numberCheck += 1

                caterory = _configZenAdmin["commands"][index]["category"]

                if caterory == "Info lookup":
                    caterory_bg_color = "cyan"
                if caterory == "Zendesk":
                    caterory_bg_color = "cyan"
                if caterory == "Admin":
                    caterory_bg_color = "purple"
                if caterory == "Miscellaneous":
                    caterory_bg_color = "blue"
                if caterory == "Create/update":
                    caterory_bg_color = "yellow"

                permission = _configZenAdmin["commands"][index]["permission"]

                if permission == "Bot Admin":
                    perm_bg_color = "red"
                if permission == "Zendesk Agent":
                    perm_bg_color = "orange"
                if permission == "All":
                    perm_bg_color = "green"
                if permission == "Zendesk Agent/Zendesk End-user":
                    perm_bg_color = "orange"
                if permission == "Authorised List":
                    perm_bg_color = "orange"

                helptext_a = str(_configZenAdmin["commands"][index]["helptext"]).replace("&", "&amp;").replace('"', "&quot;")
                param_a = str(_configZenAdmin["commands"][index]["param"]).replace("&", "&amp;").replace('"', "&quot;")
                example_a = str(_configZenAdmin["commands"][index]["example"]).replace("&", "&amp;").replace('"', "&quot;")
                desc_a = str(_configZenAdmin["commands"][index]["description"]).replace("&", "&amp;").replace('"', "&quot;")
                cat_a = str(_configZenAdmin["commands"][index]["category"]).replace("&", "&amp;").replace('"', "&quot;")
                perm_a = str(_configZenAdmin["commands"][index]["permission"]).replace("&", "&amp;").replace('"', "&quot;")

                if (numberCheck % 2) == 0:
                    table_body += "<tr style='background-color:#" + backColor + "'>" \
                              "<td style='border:1px solid black;text-align:left'>" + str(helptext_a) + "</td>" \
                              "<td style='border:1px solid black;text-align:left'>" + str(param_a) + "</td>" \
                              "<td style='border:1px solid black;text-align:left'>" + str(example_a) + "</td>" \
                              "<td style='border:1px solid black;text-align:left'>" + str(desc_a) + "</td>" \
                              "<td class=\"tempo-bg-color--" + caterory_bg_color + " tempo-text-color--white\">" + str(cat_a) + "</td>" \
                              "<td class=\"tempo-bg-color--" + perm_bg_color + " tempo-text-color--white\">" + str(perm_a) + "</td>" \
                              "</tr>"
                else:
                    table_body += "<tr>" \
                              "<td style='border:1px solid black;text-align:left'>" + str(helptext_a) + "</td>" \
                              "<td style='border:1px solid black;text-align:left'>" + str(param_a) + "</td>" \
                              "<td style='border:1px solid black;text-align:left'>" + str(example_a) + "</td>" \
                              "<td style='border:1px solid black;text-align:left'>" + str(desc_a) + "</td>" \
                              "<td class=\"tempo-bg-color--" + caterory_bg_color + " tempo-text-color--white\">" + str(cat_a) + "</td>" \
                              "<td class=\"tempo-bg-color--" + perm_bg_color + " tempo-text-color--white\">" + str(perm_a) + "</td>" \
                              "</tr>"

            _moreconfigPath = os.path.abspath('modules/command/defaultForBotAdminHelp.json')
            with codecs.open(_moreconfigPath, 'r', 'utf-8-sig') as json_file:
                _moreconfig = json.load(json_file)

            for index in range(len(_moreconfig["commands"])):

                numberCheck += 1
                caterory = _moreconfig["commands"][index]["category"]

                if caterory == "Info lookup":
                    caterory_bg_color = "cyan"
                if caterory == "Zendesk":
                    caterory_bg_color = "cyan"
                if caterory == "Admin":
                    caterory_bg_color = "purple"
                if caterory == "Miscellaneous":
                    caterory_bg_color = "blue"
                if caterory == "Create/update":
                    caterory_bg_color = "yellow"

                permission = str(_moreconfig["commands"][index]["permission"])

                if permission == "Bot Admin":
                    perm_bg_color = "red"
                if permission == "Zendesk Agent":
                    perm_bg_color = "orange"
                if permission == "All":
                    perm_bg_color = "green"
                if permission == "Zendesk Agent/Zendesk End-user":
                    perm_bg_color = "orange"
                if permission == "Authorised List":
                    perm_bg_color = "orange"

                helptext_b = str(_moreconfig["commands"][index]["helptext"]).replace("&", "&amp;").replace('"', "&quot;")
                param_b = str(_moreconfig["commands"][index]["param"]).replace("&", "&amp;").replace('"', "&quot;")
                example_b = str(_moreconfig["commands"][index]["example"]).replace("&", "&amp;").replace('"', "&quot;")
                desc_b = str(_moreconfig["commands"][index]["description"]).replace("&", "&amp;").replace('"', "&quot;")
                cat_b = str(_moreconfig["commands"][index]["category"]).replace("&", "&amp;").replace('"', "&quot;")
                perm_b = str(_moreconfig["commands"][index]["permission"]).replace("&", "&amp;").replace('"', "&quot;")

                if (numberCheck % 2) == 0:
                    table_body += "<tr style='background-color:#" + backColor + "'>" \
                              "<td style='border:1px solid black;text-align:left'>" + str(helptext_b) + "</td>" \
                              "<td style='border:1px solid black;text-align:left'>" + str(param_b) + "</td>" \
                              "<td style='border:1px solid black;text-align:left'>" + str(example_b) + "</td>" \
                              "<td style='border:1px solid black;text-align:left'>" + str(desc_b) + "</td>" \
                              "<td class=\"tempo-bg-color--" + caterory_bg_color + " tempo-text-color--white\">" + str(cat_b) + "</td>" \
                              "<td class=\"tempo-bg-color--" + perm_bg_color + " tempo-text-color--white\">" + str(perm_b) + "</td>" \
                              "</tr>"
                else:
                    table_body += "<tr>" \
                              "<td style='border:1px solid black;text-align:left'>" + str(helptext_b) + "</td>" \
                              "<td style='border:1px solid black;text-align:left'>" + str(param_b) + "</td>" \
                              "<td style='border:1px solid black;text-align:left'>" + str(example_b) + "</td>" \
                              "<td style='border:1px solid black;text-align:left'>" + str(desc_b) + "</td>" \
                              "<td class=\"tempo-bg-color--" + caterory_bg_color + " tempo-text-color--white\">" + str(cat_b) + "</td>" \
                              "<td class=\"tempo-bg-color--" + perm_bg_color + " tempo-text-color--white\">" + str(perm_b) + "</td>" \
                              "</tr>"
            else:
                pass

            table_body += "</tbody></table>"

            # Some Pod do not allow HTML file type
            AdminHelp = "<html><head><title>SupportBot Help documentation</title></head><body>" + str(table_body) + "</body></html>"
            #print(str(AdminHelp))

            f = open('Temp/help.html', 'w')
            f.write(str(AdminHelp))
            #f.write("Test")
            f.close()
            upload_raw = os.path.abspath("Temp/help.html")
            f = open(upload_raw, 'rb')
            fdata = f.read()
            #print(fdata.title())

            # ctype, encoding = mimetypes.guess_type(upload_raw)
            # att = ("SupportBot help.html", fdata, ctype)
            # att_list = [att]

            ## Convert html to PDF:
            ## https://www.geeksforgeeks.org/python-convert-html-pdf/

            ## Already Saved HTML page
            import pdfkit
            pdfkit.from_file('Temp/help.html', 'Temp/Help.pdf')

            f.close()

            upload_raw1 = os.path.abspath("Temp/Help.pdf")
            f1 = open(upload_raw1, 'rb')
            fdata1 = f1.read()
            #print(fdata1.title())

            ctype, encoding = mimetypes.guess_type(upload_raw1)
            att1 = ("SupportBot help.pdf", fdata1, ctype)

            ## To upload both html and pdf file, of the pod allows it and not block these extensions
            # att_list = [att, att1]
            att_list = [att1]

            ## Convert by website URL
            #import pdfkit
            #pdfkit.from_url('https://www.google.co.in/','shaurya.pdf')

            ## Store text in PDF
            #import pdfkit
            #pdfkit.from_string('Shaurya GFG','GfG.pdf')

            ## You can pass a list with multiple URLs or files:
            #pdfkit.from_url(['google.com', 'geeksforgeeks.org', 'facebook.com'], 'shaurya.pdf')
            #pdfkit.from_file(['file1.html', 'file2.html'], 'out.pdf')

            ## Save content in a variable
            # Use False instead of output path to save pdf to a variable
            #pdf = pdfkit.from_url('http://google.com', False)


            message = "Bot Help file"
            #
            # ##########################
            #
            botlog.LogSymphonyInfo(messageDetail.MessageRaw)
            messaging.SendSymphonyMessageV2_data(messageDetail.StreamId, message, None, att_list)

            ###################
            #
            # att_list = []
            # if messageDetail.Attachments:
            #     for att in messageDetail.Attachments:
            #         att_name = att.name
            #         att_id = att.id
            #         att_size = att.size
            #         att_response = messaging.getAttchment(messageDetail.StreamId, messageDetail.MessageId, att_id)
            #         att_item = (att_name, att_response)
            #         att_list.append(att_item)
            #         print("Att: " + att_list)
            #
            ###################

            #table_body = "<card iconSrc=\"https://thumb.ibb.co/csXBgU/Symphony2018_App_Icon_Mobile.png\" accent=\"tempo-bg-color--blue\"><header>" + header + "</header><body>" + table_body + "</body></card>"
            table_body = "<card iconSrc=\"\" accent=\"tempo-bg-color--blue\"><header>" + header + "</header><body>" + table_body + "</body></card>"
            #print(str(table_body))

            return messaging.SendSymphonyMessageV2_noBotLog(messageDetail.StreamId, table_body)
            f1.close()

            # except:
            #     return messageDetail.ReplyToChat("Please check that all the config files are in the right place. I am sorry, I was working on a different task, can you please retry")
        else:
            return messageDetail.ReplyToChat("For SupportBot /help, please IM me directly")


    ########### FOR AUTHORISED ACCESS USERS OF THE BOT - HELP FILE - SHOWS MOST COMMANDS EXCEPT ADMIN ONES:

    if callerCheck in AccessFile:
        # if companyName in _configDef['AuthCompany']['PodList']:

        streamType = ""
        streamType = (messageDetail.ChatRoom.Type)

        if streamType == "IM":

            #try:

            _moreconfigPath = os.path.abspath('modules/command/defaultforAccessUserHelp.json')

            with codecs.open(_moreconfigPath, 'r', 'utf-8-sig') as json_file:
                _moreconfig = json.load(json_file)

            header = "<b class =\"tempo-text-color--blue\">Symphony Zendesk Bot Help</b> For more information, please consult <b>Symphony Team</b> (You are part of the Authorised users) <br/>- For Feedback use <b><hash tag=\"SupportBotFeedback\"/></b><br/> - For Bug use <b><hash tag=\"SupportBotBug\"/></b><br/>"
            # ---------

            table_body = "<table style='border-collapse:collapse;border:2px solid black;table-layout:auto;max-width:100%;box-shadow: 5px 5px'><thead><tr style='background-color:#4D94FF;color:#ffffff;font-size:1rem' class=\"tempo-text-color--white tempo-bg-color--black\">" \
                         "<td style='border:1px solid blue;border-bottom: double blue;text-align:center;max-width:15%'>COMMAND</td>" \
                         "<td style='border:1px solid blue;border-bottom: double blue;text-align:center;max-width:15%'>PARAMETER</td>" \
                         "<td style='border:1px solid blue;border-bottom: double blue;text-align:center;max-width:20%'>SAMPLE</td>" \
                         "<td style='border:1px solid blue;border-bottom: double blue;text-align:center;max-width:25%'>DESCRIPTION</td>" \
                         "<td style='border:1px solid blue;border-bottom: double blue;text-align:center;max-width:12.5%'>CATEGORY</td>" \
                         "<td style='border:1px solid blue;border-bottom: double blue;text-align:center;max-width:12.5%'>PERMISSION</td>" \
                         "</tr></thead><tbody>"

            # Seems we need to set this to a colour the first time to work
            perm_bg_color = "green"
            for index in range(len(_configZenAccess["commands"])):

                numberCheck += 1
                caterory = _configZenAccess["commands"][index]["category"]

                if caterory == "Info lookup":
                    caterory_bg_color = "cyan"
                if caterory == "Zendesk":
                    caterory_bg_color = "cyan"
                if caterory == "Admin":
                    caterory_bg_color = "purple"
                if caterory == "Miscellaneous":
                    caterory_bg_color = "blue"
                if caterory == "Create/update":
                    caterory_bg_color = "yellow"

                permission = _configZenAccess["commands"][index]["permission"]

                if permission == "Bot Admin":
                    perm_bg_color = "red"
                if permission == "Zendesk Agent":
                    perm_bg_color = "orange"
                if permission == "All":
                    perm_bg_color = "green"
                if permission == "Zendesk Agent/Zendesk End-user":
                    perm_bg_color = "orange"
                if permission == "Authorised List":
                    perm_bg_color = "orange"

                helptext_a = str(_configZenAccess["commands"][index]["helptext"]).replace("&", "&amp;").replace('"', "&quot;")
                param_a = str(_configZenAccess["commands"][index]["param"]).replace("&", "&amp;").replace('"', "&quot;")
                example_a = str(_configZenAccess["commands"][index]["example"]).replace("&", "&amp;").replace('"', "&quot;")
                desc_a = str(_configZenAccess["commands"][index]["description"]).replace("&", "&amp;").replace('"', "&quot;")
                cat_a = str(_configZenAccess["commands"][index]["category"]).replace("&", "&amp;").replace('"', "&quot;")
                perm_a = str(_configZenAccess["commands"][index]["permission"]).replace("&", "&amp;").replace('"', "&quot;")

                if (numberCheck % 2) == 0:
                    table_body += "<tr style='background-color:#" + backColor + "'>" \
                              "<td style='border:1px solid black;text-align:left'>" + str(helptext_a) + "</td>" \
                              "<td style='border:1px solid black;text-align:left'>" + str(param_a) + "</td>" \
                              "<td style='border:1px solid black;text-align:left'>" + str(example_a) + "</td>" \
                              "<td style='border:1px solid black;text-align:left'>" + str(desc_a) + "</td>" \
                              "<td class=\"tempo-bg-color--" + caterory_bg_color + " tempo-text-color--white\">" + str(cat_a) + "</td>" \
                              "<td class=\"tempo-bg-color--" + perm_bg_color + " tempo-text-color--white\">" + str(perm_a) + "</td>" \
                              "</tr>"

                else:
                    table_body += "<tr>" \
                              "<td style='border:1px solid black;text-align:left'>" + str(helptext_a) + "</td>" \
                              "<td style='border:1px solid black;text-align:left'>" + str(param_a) + "</td>" \
                              "<td style='border:1px solid black;text-align:left'>" + str(example_a) + "</td>" \
                              "<td style='border:1px solid black;text-align:left'>" + str(desc_a) + "</td>" \
                              "<td class=\"tempo-bg-color--" + caterory_bg_color + " tempo-text-color--white\">" + str(cat_a) + "</td>" \
                              "<td class=\"tempo-bg-color--" + perm_bg_color + " tempo-text-color--white\">" + str(perm_a) + "</td>" \
                              "</tr>"

            _moreconfigPath = os.path.abspath('modules/command/defaultforAccessUserHelp.json')
            with codecs.open(_moreconfigPath, 'r', 'utf-8-sig') as json_file:
                _moreconfig = json.load(json_file)

            for index in range(len(_moreconfig["commands"])):

                numberCheck += 1
                caterory = _moreconfig["commands"][index]["category"]

                if caterory == "Info lookup":
                    caterory_bg_color = "cyan"
                if caterory == "Zendesk":
                    caterory_bg_color = "cyan"
                if caterory == "Admin":
                    caterory_bg_color = "purple"
                if caterory == "Miscellaneous":
                    caterory_bg_color = "blue"
                if caterory == "Create/update":
                    caterory_bg_color = "yellow"

                permission = str(_moreconfig["commands"][index]["permission"])

                if permission == "Bot Admin":
                    perm_bg_color = "red"
                if permission == "Zendesk Agent":
                    perm_bg_color = "orange"
                if permission == "All":
                    perm_bg_color = "green"
                if permission == "Zendesk Agent/Zendesk End-user":
                    perm_bg_color = "orange"
                if permission == "Authorised List":
                    perm_bg_color = "orange"

                helptext_b = str(_moreconfig["commands"][index]["helptext"]).replace("&", "&amp;").replace('"', "&quot;")
                param_b = str(_moreconfig["commands"][index]["param"]).replace("&", "&amp;").replace('"', "&quot;")
                example_b = str(_moreconfig["commands"][index]["example"]).replace("&", "&amp;").replace('"', "&quot;")
                desc_b = str(_moreconfig["commands"][index]["description"]).replace("&", "&amp;").replace('"', "&quot;")
                cat_b = str(_moreconfig["commands"][index]["category"]).replace("&", "&amp;").replace('"', "&quot;")
                perm_b = str(_moreconfig["commands"][index]["permission"]).replace("&", "&amp;").replace('"', "&quot;")

                if (numberCheck % 2) == 0:
                    table_body += "<tr style='background-color:#" + backColor + "'>" \
                              "<td style='border:1px solid black;text-align:left'>" + str(helptext_b) + "</td>" \
                              "<td style='border:1px solid black;text-align:left'>" + str(param_b) + "</td>" \
                              "<td style='border:1px solid black;text-align:left'>" + str(example_b) + "</td>" \
                              "<td style='border:1px solid black;text-align:left'>" + str(desc_b) + "</td>" \
                              "<td class=\"tempo-bg-color--" + caterory_bg_color + " tempo-text-color--white\">" + str(cat_b) + "</td>" \
                              "<td class=\"tempo-bg-color--" + perm_bg_color + " tempo-text-color--white\">" + str(perm_b) + "</td>" \
                              "</tr>"

                else:
                    table_body += "<tr>" \
                              "<td style='border:1px solid black;text-align:left'>" + str(helptext_b) + "</td>" \
                              "<td style='border:1px solid black;text-align:left'>" + str(param_b) + "</td>" \
                              "<td style='border:1px solid black;text-align:left'>" + str(example_b) + "</td>" \
                              "<td style='border:1px solid black;text-align:left'>" + str(desc_b) + "</td>" \
                              "<td class=\"tempo-bg-color--" + caterory_bg_color + " tempo-text-color--white\">" + str(cat_b) + "</td>" \
                              "<td class=\"tempo-bg-color--" + perm_bg_color + " tempo-text-color--white\">" + str(perm_b) + "</td>" \
                              "</tr>"
            else:
                pass

            table_body += "</tbody></table>"

            # Some Pod do not allow HTML file type
            AdminHelp = "<html><head><title>SupportBot Help documentation</title></head><body>" + str(table_body) + "</body></html>"
            #print(str(AdminHelp))

            f = open('Temp/help.html', 'w')
            f.write(str(AdminHelp))
            #f.write("Test")
            f.close()
            upload_raw = os.path.abspath("Temp/help.html")
            f = open(upload_raw, 'rb')
            fdata = f.read()
            #print(fdata.title())

            # ctype, encoding = mimetypes.guess_type(upload_raw)
            # att = ("SupportBot help.html", fdata, ctype)
            # att_list = [att]

            ## Convert html to PDF:
            ## https://www.geeksforgeeks.org/python-convert-html-pdf/

            ## Already Saved HTML page
            import pdfkit
            pdfkit.from_file('Temp/help.html', 'Temp/Help.pdf')

            f.close()

            upload_raw1 = os.path.abspath("Temp/Help.pdf")
            f1 = open(upload_raw1, 'rb')
            fdata1 = f1.read()
            #print(fdata1.title())

            ctype, encoding = mimetypes.guess_type(upload_raw1)
            att1 = ("SupportBot help.pdf", fdata1, ctype)

            ## To upload both html and pdf file, of the pod allows it and not block these extensions
            # att_list = [att, att1]
            att_list = [att1]

            ## Convert by website URL
            #import pdfkit
            #pdfkit.from_url('https://www.google.co.in/','shaurya.pdf')

            ## Store text in PDF
            #import pdfkit
            #pdfkit.from_string('Shaurya GFG','GfG.pdf')

            ## You can pass a list with multiple URLs or files:
            #pdfkit.from_url(['google.com', 'geeksforgeeks.org', 'facebook.com'], 'shaurya.pdf')
            #pdfkit.from_file(['file1.html', 'file2.html'], 'out.pdf')

            ## Save content in a variable
            # Use False instead of output path to save pdf to a variable
            #pdf = pdfkit.from_url('http://google.com', False)


            message = "Bot Help file"
            #
            # ##########################
            #
            botlog.LogSymphonyInfo(messageDetail.MessageRaw)
            messaging.SendSymphonyMessageV2_data(messageDetail.StreamId, message, None, att_list)

            ###################
            #
            # att_list = []
            # if messageDetail.Attachments:
            #     for att in messageDetail.Attachments:
            #         att_name = att.name
            #         att_id = att.id
            #         att_size = att.size
            #         att_response = messaging.getAttchment(messageDetail.StreamId, messageDetail.MessageId, att_id)
            #         att_item = (att_name, att_response)
            #         att_list.append(att_item)
            #         print("Att: " + att_list)
            #
            ###################

            #table_body = "<card iconSrc=\"https://thumb.ibb.co/csXBgU/Symphony2018_App_Icon_Mobile.png\" accent=\"tempo-bg-color--blue\"><header>" + header + "</header><body>" + table_body + "</body></card>"
            table_body = "<card iconSrc=\"\" accent=\"tempo-bg-color--blue\"><header>" + header + "</header><body>" + table_body + "</body></card>"
            #print(str(table_body))

            return messaging.SendSymphonyMessageV2_noBotLog(messageDetail.StreamId, table_body)
            f1.close()

            # except:
            #     return messageDetail.ReplyToChat("Please check that all the config files are in the right place. I am sorry, I was working on a different task, can you please retry")
        else:
            return messageDetail.ReplyToChat("For SupportBot /help, please IM me directly")

    ########### FOR INTERNAL SYMPHONY POD USERS - HELP FILE - SHOWS LIMITED COMMANDS:

    if companyName in _configDef['AuthCompany']['PodList']:

        streamType = ""
        streamType = (messageDetail.ChatRoom.Type)

        if streamType == "IM":

            #try:

            # _moreconfigPath = os.path.abspath('modules/command/default.json')
            _moreconfigPath = os.path.abspath('modules/command/defaultForInternalHelp.json')

            with codecs.open(_moreconfigPath, 'r', 'utf-8-sig') as json_file:
                _moreconfig = json.load(json_file)

            header = "<b class =\"tempo-text-color--blue\">Symphony Zendesk Bot Help</b> For more information, please consult <b>Symphony Team</b><br/>- For Feedback use <b><hash tag=\"SupportBotFeedback\"/></b><br/> - For Bug use <b><hash tag=\"SupportBotBug\"/></b><br/>"
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
            for index in range(len(_configZenINT["commands"])):

                numberCheck += 1
                caterory = _configZenINT["commands"][index]["category"]

                if caterory == "Info lookup":
                    caterory_bg_color = "cyan"
                if caterory == "Zendesk":
                    caterory_bg_color = "cyan"
                if caterory == "Admin":
                    caterory_bg_color = "purple"
                if caterory == "Miscellaneous":
                    caterory_bg_color = "blue"
                if caterory == "Create/update":
                    caterory_bg_color = "yellow"

                permission = _configZenINT["commands"][index]["permission"]

                if permission == "Bot Admin":
                    perm_bg_color = "red"
                if permission == "Zendesk Agent":
                    perm_bg_color = "orange"
                if permission == "All":
                    perm_bg_color = "green"
                if permission == "Zendesk Agent/Zendesk End-user":
                    perm_bg_color = "orange"

                helptext_a = str(_configZenINT["commands"][index]["helptext"]).replace("&", "&amp;").replace('"', "&quot;")
                param_a = str(_configZenINT["commands"][index]["param"]).replace("&", "&amp;").replace('"', "&quot;")
                example_a = str(_configZenINT["commands"][index]["example"]).replace("&", "&amp;").replace('"', "&quot;")
                desc_a = str(_configZenINT["commands"][index]["description"]).replace("&", "&amp;").replace('"', "&quot;")
                cat_a = str(_configZenINT["commands"][index]["category"]).replace("&", "&amp;").replace('"', "&quot;")
                perm_a = str(_configZenINT["commands"][index]["permission"]).replace("&", "&amp;").replace('"', "&quot;")

                if (numberCheck % 2) == 0:
                    table_body += "<tr style='background-color:#" + backColor + "'>" \
                              "<td style='border:1px solid black;text-align:left'>" + str(helptext_a) + "</td>" \
                              "<td style='border:1px solid black;text-align:left'>" + str(param_a) + "</td>" \
                              "<td style='border:1px solid black;text-align:left'>" + str(example_a) + "</td>" \
                              "<td style='border:1px solid black;text-align:left'>" + str(desc_a) + "</td>" \
                              "<td class=\"tempo-bg-color--" + caterory_bg_color + " tempo-text-color--white\">" + str(cat_a) + "</td>" \
                              "<td class=\"tempo-bg-color--" + perm_bg_color + " tempo-text-color--white\">" + str(perm_a) + "</td>" \
                              "</tr>"
                else:
                    table_body += "<tr>" \
                              "<td style='border:1px solid black;text-align:left'>" + str(helptext_a) + "</td>" \
                              "<td style='border:1px solid black;text-align:left'>" + str(param_a) + "</td>" \
                              "<td style='border:1px solid black;text-align:left'>" + str(example_a) + "</td>" \
                              "<td style='border:1px solid black;text-align:left'>" + str(desc_a) + "</td>" \
                              "<td class=\"tempo-bg-color--" + caterory_bg_color + " tempo-text-color--white\">" + str(cat_a) + "</td>" \
                              "<td class=\"tempo-bg-color--" + perm_bg_color + " tempo-text-color--white\">" + str(perm_a) + "</td>" \
                              "</tr>"

            # _moreconfigPath = os.path.abspath('modules/command/default.json')
            _moreconfigPath = os.path.abspath('modules/command/defaultForInternalHelp.json')
            with codecs.open(_moreconfigPath, 'r', 'utf-8-sig') as json_file:
                _moreconfig = json.load(json_file)

            for index in range(len(_moreconfig["commands"])):

                numberCheck += 1
                caterory = _moreconfig["commands"][index]["category"]

                if caterory == "Info lookup":
                    caterory_bg_color = "cyan"
                if caterory == "Zendesk":
                    caterory_bg_color = "cyan"
                if caterory == "Admin":
                    caterory_bg_color = "purple"
                if caterory == "Miscellaneous":
                    caterory_bg_color = "blue"
                if caterory == "Create/update":
                    caterory_bg_color = "yellow"

                permission = str(_moreconfig["commands"][index]["permission"])

                if permission == "Bot Admin":
                    perm_bg_color = "red"
                if permission == "Zendesk Agent":
                    perm_bg_color = "orange"
                if permission == "All":
                    perm_bg_color = "green"
                if permission == "Zendesk Agent/Zendesk End-user":
                    perm_bg_color = "orange"

                helptext_b = str(_moreconfig["commands"][index]["helptext"]).replace("&", "&amp;").replace('"', "&quot;")
                param_b = str(_moreconfig["commands"][index]["param"]).replace("&", "&amp;").replace('"', "&quot;")
                example_b = str(_moreconfig["commands"][index]["example"]).replace("&", "&amp;").replace('"', "&quot;")
                desc_b = str(_moreconfig["commands"][index]["description"]).replace("&", "&amp;").replace('"', "&quot;")
                cat_b = str(_moreconfig["commands"][index]["category"]).replace("&", "&amp;").replace('"', "&quot;")
                perm_b = str(_moreconfig["commands"][index]["permission"]).replace("&", "&amp;").replace('"', "&quot;")

                if (numberCheck % 2) == 0:
                    table_body += "<tr style='background-color:#" + backColor + "'>" \
                              "<td style='border:1px solid black;text-align:left'>" + str(helptext_b) + "</td>" \
                              "<td style='border:1px solid black;text-align:left'>" + str(param_b) + "</td>" \
                              "<td style='border:1px solid black;text-align:left'>" + str(example_b) + "</td>" \
                              "<td style='border:1px solid black;text-align:left'>" + str(desc_b) + "</td>" \
                              "<td class=\"tempo-bg-color--" + caterory_bg_color + " tempo-text-color--white\">" + str(cat_b) + "</td>" \
                              "<td class=\"tempo-bg-color--" + perm_bg_color + " tempo-text-color--white\">" + str(perm_b) + "</td>" \
                              "</tr>"
                else:
                    table_body += "<tr>" \
                              "<td style='border:1px solid black;text-align:left'>" + str(helptext_b) + "</td>" \
                              "<td style='border:1px solid black;text-align:left'>" + str(param_b) + "</td>" \
                              "<td style='border:1px solid black;text-align:left'>" + str(example_b) + "</td>" \
                              "<td style='border:1px solid black;text-align:left'>" + str(desc_b) + "</td>" \
                              "<td class=\"tempo-bg-color--" + caterory_bg_color + " tempo-text-color--white\">" + str(cat_b) + "</td>" \
                              "<td class=\"tempo-bg-color--" + perm_bg_color + " tempo-text-color--white\">" + str(perm_b) + "</td>" \
                              "</tr>"
            else:
                pass

            table_body += "</tbody></table>"


            # Some Pod do not allow HTML file type
            AdminHelp = "<html><head><title>SupportBot Help documentation</title></head><body>" + str(table_body) + "</body></html>"
            #print(str(AdminHelp))

            f = open('Temp/help.html', 'w')
            f.write(str(AdminHelp))
            #f.write("Test")
            f.close()
            upload_raw = os.path.abspath("Temp/help.html")
            f = open(upload_raw, 'rb')
            fdata = f.read()
            #print(fdata.title())

            # ctype, encoding = mimetypes.guess_type(upload_raw)
            # att = ("SupportBot help.html", fdata, ctype)
            # att_list = [att]

            ## Convert html to PDF:
            ## https://www.geeksforgeeks.org/python-convert-html-pdf/

            ## Already Saved HTML page
            import pdfkit
            pdfkit.from_file('Temp/help.html', 'Temp/Help.pdf')

            f.close()

            upload_raw1 = os.path.abspath("Temp/Help.pdf")
            f1 = open(upload_raw1, 'rb')
            fdata1 = f1.read()
            #print(fdata1.title())

            ctype, encoding = mimetypes.guess_type(upload_raw1)
            att1 = ("SupportBot help.pdf", fdata1, ctype)

            ## To upload both html and pdf file, of the pod allows it and not block these extensions
            # att_list = [att, att1]
            att_list = [att1]

            ## Convert by website URL
            #import pdfkit
            #pdfkit.from_url('https://www.google.co.in/','shaurya.pdf')

            ## Store text in PDF
            #import pdfkit
            #pdfkit.from_string('Shaurya GFG','GfG.pdf')

            ## You can pass a list with multiple URLs or files:
            #pdfkit.from_url(['google.com', 'geeksforgeeks.org', 'facebook.com'], 'shaurya.pdf')
            #pdfkit.from_file(['file1.html', 'file2.html'], 'out.pdf')

            ## Save content in a variable
            # Use False instead of output path to save pdf to a variable
            #pdf = pdfkit.from_url('http://google.com', False)


            message = "Bot Help file"
            #
            # ##########################
            #
            botlog.LogSymphonyInfo(messageDetail.MessageRaw)
            messaging.SendSymphonyMessageV2_data(messageDetail.StreamId, message, None, att_list)
            #
            # ##########################

            ###################
            #
            # att_list = []
            # if messageDetail.Attachments:
            #     for att in messageDetail.Attachments:
            #         att_name = att.name
            #         att_id = att.id
            #         att_size = att.size
            #         att_response = messaging.getAttchment(messageDetail.StreamId, messageDetail.MessageId, att_id)
            #         att_item = (att_name, att_response)
            #         att_list.append(att_item)
            #         print("Att: " + att_list)
            #
            ###################

            #table_body = "<card iconSrc=\"https://thumb.ibb.co/csXBgU/Symphony2018_App_Icon_Mobile.png\" accent=\"tempo-bg-color--blue\"><header>" + header + "</header><body>" + table_body + "</body></card>"
            table_body = "<card iconSrc=\"\" accent=\"tempo-bg-color--blue\"><header>" + header + "</header><body>" + table_body + "</body></card>"


            return messaging.SendSymphonyMessageV2_noBotLog(messageDetail.StreamId, table_body)
            f1.close()

            # except:
            #     return messageDetail.ReplyToChat("Please check that all the config files are in the right place. I am sorry, I was working on a different task, can you please retry")
        else:
            return messageDetail.ReplyToChat("For SupportBot /help, please IM me directly")

    ########### FOR EXTERNAL SYMPHONY AUTHORISED POD USERS - HELP FILE - SHOWS RESTRICTED COMMANDS:

    if companyName in _configDef['AuthExtCompany']['PodList']:

        streamType = ""
        streamType = (messageDetail.ChatRoom.Type)

        if streamType == "IM":

            #try:

            # _moreconfigPath = os.path.abspath('modules/command/default.json')
            _moreconfigPath = os.path.abspath('modules/command/defaultForExternalHelp.json')

            with codecs.open(_moreconfigPath, 'r', 'utf-8-sig') as json_file:
                _moreconfig = json.load(json_file)

            header = "<b class =\"tempo-text-color--blue\">Symphony Zendesk Bot Help</b> For more information, please consult <b>Symphony Team</b><br/>- For Feedback use <b><hash tag=\"SupportBotFeedback\"/></b><br/> - For Bug use <b><hash tag=\"SupportBotBug\"/></b><br/>"
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
            for index in range(len(_configZenEXT["commands"])):

                numberCheck += 1
                caterory = _configZenEXT["commands"][index]["category"]

                if caterory == "Info lookup":
                    caterory_bg_color = "cyan"
                if caterory == "Zendesk":
                    caterory_bg_color = "cyan"
                if caterory == "Admin":
                    caterory_bg_color = "purple"
                if caterory == "Miscellaneous":
                    caterory_bg_color = "blue"
                if caterory == "Create/update":
                    caterory_bg_color = "yellow"

                permission = _configZenEXT["commands"][index]["permission"]

                if permission == "Bot Admin":
                    perm_bg_color = "red"
                if permission == "Zendesk Agent":
                    perm_bg_color = "orange"
                if permission == "All":
                    perm_bg_color = "green"
                if permission == "Zendesk Agent/Zendesk End-user":
                    perm_bg_color = "orange"

                helptext_a = str(_configZenEXT["commands"][index]["helptext"]).replace("&", "&amp;").replace('"', "&quot;")
                param_a = str(_configZenEXT["commands"][index]["param"]).replace("&", "&amp;").replace('"', "&quot;")
                example_a = str(_configZenEXT["commands"][index]["example"]).replace("&", "&amp;").replace('"', "&quot;")
                desc_a = str(_configZenEXT["commands"][index]["description"]).replace("&", "&amp;").replace('"', "&quot;")
                cat_a = str(_configZenEXT["commands"][index]["category"]).replace("&", "&amp;").replace('"', "&quot;")
                perm_a = str(_configZenEXT["commands"][index]["permission"]).replace("&", "&amp;").replace('"', "&quot;")

                if (numberCheck % 2) == 0:
                    table_body += "<tr style='background-color:#" + backColor + "'>" \
                              "<td style='border:1px solid black;text-align:left'>" + str(helptext_a) + "</td>" \
                              "<td style='border:1px solid black;text-align:left'>" + str(param_a) + "</td>" \
                              "<td style='border:1px solid black;text-align:left'>" + str(example_a) + "</td>" \
                              "<td style='border:1px solid black;text-align:left'>" + str(desc_a) + "</td>" \
                              "<td class=\"tempo-bg-color--" + caterory_bg_color + " tempo-text-color--white\">" + str(cat_a) + "</td>" \
                              "<td class=\"tempo-bg-color--" + perm_bg_color + " tempo-text-color--white\">" + str(perm_a) + "</td>" \
                              "</tr>"

                else:
                    table_body += "<tr>" \
                              "<td style='border:1px solid black;text-align:left'>" + str(helptext_a) + "</td>" \
                              "<td style='border:1px solid black;text-align:left'>" + str(param_a) + "</td>" \
                              "<td style='border:1px solid black;text-align:left'>" + str(example_a) + "</td>" \
                              "<td style='border:1px solid black;text-align:left'>" + str(desc_a) + "</td>" \
                              "<td class=\"tempo-bg-color--" + caterory_bg_color + " tempo-text-color--white\">" + str(cat_a) + "</td>" \
                              "<td class=\"tempo-bg-color--" + perm_bg_color + " tempo-text-color--white\">" + str(perm_a) + "</td>" \
                              "</tr>"

            # _moreconfigPath = os.path.abspath('modules/command/default.json')
            _moreconfigPath = os.path.abspath('modules/command/defaultForExternalHelp.json')
            with codecs.open(_moreconfigPath, 'r', 'utf-8-sig') as json_file:
                _moreconfig = json.load(json_file)

            for index in range(len(_moreconfig["commands"])):

                numberCheck += 1
                caterory = _moreconfig["commands"][index]["category"]

                if caterory == "Info lookup":
                    caterory_bg_color = "cyan"
                if caterory == "Zendesk":
                    caterory_bg_color = "cyan"
                if caterory == "Admin":
                    caterory_bg_color = "purple"
                if caterory == "Miscellaneous":
                    caterory_bg_color = "blue"
                if caterory == "Create/update":
                    caterory_bg_color = "yellow"

                permission = str(_moreconfig["commands"][index]["permission"])

                if permission == "Bot Admin":
                    perm_bg_color = "red"
                if permission == "Zendesk Agent":
                    perm_bg_color = "orange"
                if permission == "All":
                    perm_bg_color = "green"
                if permission == "Zendesk Agent/Zendesk End-user":
                    perm_bg_color = "orange"

                helptext_b = str(_moreconfig["commands"][index]["helptext"]).replace("&", "&amp;").replace('"', "&quot;")
                param_b = str(_moreconfig["commands"][index]["param"]).replace("&", "&amp;").replace('"', "&quot;")
                example_b = str(_moreconfig["commands"][index]["example"]).replace("&", "&amp;").replace('"', "&quot;")
                desc_b = str(_moreconfig["commands"][index]["description"]).replace("&", "&amp;").replace('"', "&quot;")
                cat_b = str(_moreconfig["commands"][index]["category"]).replace("&", "&amp;").replace('"', "&quot;")
                perm_b = str(_moreconfig["commands"][index]["permission"]).replace("&", "&amp;").replace('"', "&quot;")

                if (numberCheck % 2) == 0:
                        table_body += "<tr style='background-color:#" + backColor + "'>" \
                              "<td style='border:1px solid black;text-align:left'>" + str(helptext_b) + "</td>" \
                              "<td style='border:1px solid black;text-align:left'>" + str(param_b) + "</td>" \
                              "<td style='border:1px solid black;text-align:left'>" + str(example_b) + "</td>" \
                              "<td style='border:1px solid black;text-align:left'>" + str(desc_b) + "</td>" \
                              "<td class=\"tempo-bg-color--" + caterory_bg_color + " tempo-text-color--white\">" + str(cat_b) + "</td>" \
                              "<td class=\"tempo-bg-color--" + perm_bg_color + " tempo-text-color--white\">" + str(perm_b) + "</td>" \
                              "</tr>"

                else:
                    table_body += "<tr>" \
                              "<td style='border:1px solid black;text-align:left'>" + str(helptext_b) + "</td>" \
                              "<td style='border:1px solid black;text-align:left'>" + str(param_b) + "</td>" \
                              "<td style='border:1px solid black;text-align:left'>" + str(example_b) + "</td>" \
                              "<td style='border:1px solid black;text-align:left'>" + str(desc_b) + "</td>" \
                              "<td class=\"tempo-bg-color--" + caterory_bg_color + " tempo-text-color--white\">" + str(cat_b) + "</td>" \
                              "<td class=\"tempo-bg-color--" + perm_bg_color + " tempo-text-color--white\">" + str(perm_b) + "</td>" \
                              "</tr>"
            else:
                pass

            table_body += "</tbody></table>"


            # Some Pod do not allow HTML file type
            AdminHelp = "<html><head><title>SupportBot Help documentation</title></head><body>" + str(table_body) + "</body></html>"
            #print(str(AdminHelp))

            f = open('Temp/help.html', 'w')
            f.write(str(AdminHelp))
            #f.write("Test")
            f.close()
            upload_raw = os.path.abspath("Temp/help.html")
            f = open(upload_raw, 'rb')
            fdata = f.read()
            #print(fdata.title())

            # ctype, encoding = mimetypes.guess_type(upload_raw)
            # att = ("SupportBot help.html", fdata, ctype)
            # att_list = [att]

            ## Convert html to PDF:
            ## https://www.geeksforgeeks.org/python-convert-html-pdf/

            ## Already Saved HTML page
            import pdfkit
            pdfkit.from_file('Temp/help.html', 'Temp/Help.pdf')

            f.close()

            upload_raw1 = os.path.abspath("Temp/Help.pdf")
            f1 = open(upload_raw1, 'rb')
            fdata1 = f1.read()
            #print(fdata1.title())

            ctype, encoding = mimetypes.guess_type(upload_raw1)
            att1 = ("SupportBot help.pdf", fdata1, ctype)

            ## To upload both html and pdf file, of the pod allows it and not block these extensions
            # att_list = [att, att1]
            att_list = [att1]

            ## Convert by website URL
            #import pdfkit
            #pdfkit.from_url('https://www.google.co.in/','shaurya.pdf')

            ## Store text in PDF
            #import pdfkit
            #pdfkit.from_string('Shaurya GFG','GfG.pdf')

            ## You can pass a list with multiple URLs or files:
            #pdfkit.from_url(['google.com', 'geeksforgeeks.org', 'facebook.com'], 'shaurya.pdf')
            #pdfkit.from_file(['file1.html', 'file2.html'], 'out.pdf')

            ## Save content in a variable
            # Use False instead of output path to save pdf to a variable
            #pdf = pdfkit.from_url('http://google.com', False)


            message = "Bot Help file"
            #
            # ##########################
            #
            botlog.LogSymphonyInfo(messageDetail.MessageRaw)
            messaging.SendSymphonyMessageV2_data(messageDetail.StreamId, message, None, att_list)
            #
            # ##########################

            ###################
            #
            # att_list = []
            # if messageDetail.Attachments:
            #     for att in messageDetail.Attachments:
            #         att_name = att.name
            #         att_id = att.id
            #         att_size = att.size
            #         att_response = messaging.getAttchment(messageDetail.StreamId, messageDetail.MessageId, att_id)
            #         att_item = (att_name, att_response)
            #         att_list.append(att_item)
            #         print("Att: " + att_list)
            #
            ###################

            #table_body = "<card iconSrc=\"https://thumb.ibb.co/csXBgU/Symphony2018_App_Icon_Mobile.png\" accent=\"tempo-bg-color--blue\"><header>" + header + "</header><body>" + table_body + "</body></card>"
            table_body = "<card iconSrc=\"\" accent=\"tempo-bg-color--blue\"><header>" + header + "</header><body>" + table_body + "</body></card>"


            return messaging.SendSymphonyMessageV2_noBotLog(messageDetail.StreamId, table_body)
            f1.close()

            # except:
            #     return messageDetail.ReplyToChat("Please check that all the config files are in the right place. I am sorry, I was working on a different task, can you please retry")
        else:
            return messageDetail.ReplyToChat("For SupportBot /help, please IM me directly")

    else:
        botlog.LogSymphonyInfo("This pod is not authorised to access the bot")


def botStream(messageDetail):
    botlog.LogSymphonyInfo("###########################")
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
            # data_dict = ast.literal_eval(data_raw)
            data_dict = json.loads(str(data_raw))

            dataRender = json.dumps(data_dict, indent=2)
            d_org = json.loads(dataRender)
            botlog.LogSymphonyInfo(str(d_org))

            for index_org in range(len(d_org["users"])):
                firstName = str(d_org["users"][index_org]["firstName"])
                lastName = str(d_org["users"][index_org]["lastName"])
                displayName = str(d_org["users"][index_org]["displayName"])
                #companyName = d_org["users"][index_org]["company"]
                companyNameTemp = d_org["users"][index_org]["company"]
                companyTemp = str(companyNameTemp).replace("&", "&amp;").replace("<", "&lt;").replace('"', "&quot;").replace("'", "&apos;").replace(">", "&gt;")
                companyName = str(companyTemp)
                userID = str(d_org["users"][index_org]["id"])

                botlog.LogSymphonyInfo(str(firstName) + " " + str(lastName) + " from Company/Pod name: " + str(companyName) + " with UID: " + str(userID))
                callerCheck = (firstName + " " + lastName + " - " + displayName + " - " + companyName + " - " + str(userID))

        except:
            #return messageDetail.ReplyToChat("Cannot validate user access")
            return botlog.LogSymphonyInfo("Cannot validate user access")

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

            #return messageDetail.ReplyToChatV2_noBotLog("<card iconSrc =\"https://thumb.ibb.co/csXBgU/Symphony2018_App_Icon_Mobile.png\" accent=\"tempo-bg-color--blue\"><header>Please find the result below. Total number of stream with the Bot <b>" + str(count) + "</b> </header><body>" + reply + "</body></card>")
            return messageDetail.ReplyToChatV2_noBotLog("<card iconSrc =\"\" accent=\"tempo-bg-color--blue\"><header>Please find the result below. Total number of stream with the Bot <b>" + str(count) + "</b> </header><body>" + reply + "</body></card>")

        else:
            #return messageDetail.ReplyToChat("You aren't authorised to use this command.")
            return botlog.LogSymphonyInfo("You aren't authorised to use this command.")
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
                # data_dict = ast.literal_eval(data_raw)
                data_dict = json.loads(str(data_raw))

                dataRender = json.dumps(data_dict, indent=2)
                d_org = json.loads(dataRender)
                botlog.LogSymphonyInfo(str(d_org))

                for index_org in range(len(d_org["users"])):
                    firstName = str(d_org["users"][index_org]["firstName"])
                    lastName = str(d_org["users"][index_org]["lastName"])
                    displayName = str(d_org["users"][index_org]["displayName"])
                    #companyName = d_org["users"][index_org]["company"]
                    companyNameTemp = d_org["users"][index_org]["company"]
                    companyTemp = str(companyNameTemp).replace("&", "&amp;").replace("<", "&lt;").replace('"', "&quot;").replace("'", "&apos;").replace(">", "&gt;")
                    companyName = str(companyTemp)
                    userID = str(d_org["users"][index_org]["id"])

                    botlog.LogSymphonyInfo(str(firstName) + " " + str(lastName) + " from Company/Pod name: " + str(
                        companyName) + " with UID: " + str(userID))
                    callerCheck = (firstName + " " + lastName + " - " + displayName + " - " + companyName + " - " + str(
                        userID))

            except:
                #return messageDetail.ReplyToChat("Cannot validate user access")
                return botlog.LogSymphonyInfo("Cannot validate user access")

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

                #return messageDetail.ReplyToChatV2_noBotLog("<card iconSrc =\"https://thumb.ibb.co/csXBgU/Symphony2018_App_Icon_Mobile.png\" accent=\"tempo-bg-color--blue\"><header>Please find the result below. Total number of stream with the Bot <b>" + str(count) + "</b> </header><body>" + reply + "</body></card>")
                return messageDetail.ReplyToChatV2_noBotLog("<card iconSrc =\"\" accent=\"tempo-bg-color--blue\"><header>Please find the result below. Total number of stream with the Bot <b>" + str(count) + "</b> </header><body>" + reply + "</body></card>")

            else:
                #return messageDetail.ReplyToChat("You aren't authorised to use this command.")
                return botlog.LogSymphonyInfo("You aren't authorised to use this command.")
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
            # data_dict = ast.literal_eval(data_raw)
            data_dict = json.loads(str(data_raw))

            dataRender = json.dumps(data_dict, indent=2)
            d_org = json.loads(dataRender)
            botlog.LogSymphonyInfo(str(d_org))

            for index_org in range(len(d_org["users"])):
                firstName = str(d_org["users"][index_org]["firstName"])
                lastName = str(d_org["users"][index_org]["lastName"])
                displayName = str(d_org["users"][index_org]["displayName"])
                #companyName = d_org["users"][index_org]["company"]
                companyNameTemp = d_org["users"][index_org]["company"]
                companyTemp = str(companyNameTemp).replace("&", "&amp;").replace("<", "&lt;").replace('"', "&quot;").replace("'", "&apos;").replace(">", "&gt;")
                companyName = str(companyTemp)
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
#             #data_dict = ast.literal_eval(data_raw)
#             data_dict = json.loads(str(data_raw))
#
#             dataRender = json.dumps(data_dict, indent=2)
#             d_org = json.loads(dataRender)
#
#             for index_org in range(len(d_org["users"])):
#                 firstName = d_org["users"][index_org]["firstName"]
#                 lastName = d_org["users"][index_org]["lastName"]
#                 displayName = d_org["users"][index_org]["displayName"]
#                 #companyName = d_org["users"][index_org]["company"]
#                 companyNameTemp = d_org["users"][index_org]["company"]
#                 companyTemp = str(companyNameTemp).replace("&", "&amp;").replace("<", "&lt;").replace('"', "&quot;").replace("'", "&apos;").replace(">", "&gt;")
#                 companyName = str(companyTemp)
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
    #data_dict = ast.literal_eval(data_raw)
    data_dict = json.loads(str(data_raw))

    dataRender = json.dumps(data_dict, indent=2)
    d_org = json.loads(str(dataRender))
    botlog.LogSymphonyInfo(str(d_org))

    for index_org in range(len(d_org["users"])):
        firstName = str(d_org["users"][index_org]["firstName"])
        lastName = str(d_org["users"][index_org]["lastName"])
        displayName = str(d_org["users"][index_org]["displayName"])
        #companyName = d_org["users"][index_org]["company"]
        companyNameTemp = d_org["users"][index_org]["company"]
        companyTemp = str(companyNameTemp).replace("&", "&amp;").replace("<", "&lt;").replace('"', "&quot;").replace("'", "&apos;").replace(">", "&gt;")
        companyName = str(companyTemp)
        userID = str(d_org["users"][index_org]["id"])

    if companyName in _configDef['AuthCompany']['PodList'] or companyName in _configDef['AuthExtCompany']['PodList']:

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



########


def SendSymphonyEchoV2(messageDetail):

    try:
        commandCallerUID = messageDetail.FromUserId

        connComp.request("GET", "/pod/v3/users?uid=" + commandCallerUID, headers=headersCompany)

        resComp = connComp.getresponse()
        dataComp = resComp.read()
        data_raw = str(dataComp.decode('utf-8'))
        # data_dict = ast.literal_eval(data_raw)
        data_dict = json.loads(str(data_raw))

        dataRender = json.dumps(data_dict, indent=2)
        d_org = json.loads(dataRender)

        for index_org in range(len(d_org["users"])):
            firstName = str(d_org["users"][index_org]["firstName"])
            lastName = str(d_org["users"][index_org]["lastName"])
            displayName = str(d_org["users"][index_org]["displayName"])
            #companyName = d_org["users"][index_org]["company"]
            companyNameTemp = d_org["users"][index_org]["company"]
            companyTemp = str(companyNameTemp).replace("&", "&amp;").replace("<", "&lt;").replace('"', "&quot;").replace("'", "&apos;").replace(">", "&gt;")
            companyName = str(companyTemp)
            userID = str(d_org["users"][index_org]["id"])

        botlog.LogSymphonyInfo(str(firstName) + " " + str(lastName) + " (" + str(displayName) + ") from Company/Pod name: " + str(companyName) + " with UID: " + str(userID))
        callerCheck = (str(firstName) + " " + str(lastName) + " - " + str(displayName) + " - " + str(companyName) + " - " + str(userID))

        # if callerCheck in AccessFile:
        if companyName in _configDef['AuthCompany']['PodList']:
            try:
                msg = messageDetail.Command.MessageText.strip()
                messaging.SendSymphonyMessageV2(messageDetail.StreamId, msg)
            except:
                botlog.LogSymphonyInfo("Echo did not work")
    except:
        botlog.LogSymphonyInfo("Inside second try for Echo")
        try:
            msg = messageDetail.Command.MessageText.strip()
            messaging.SendSymphonyMessageV2(messageDetail.StreamId, msg)
        except:
            botlog.LogSymphonyInfo("Echo did not work entirely")

def GetGoogleTranslation(messageDetail):

    try:
        commandCallerUID = messageDetail.FromUserId

        connComp.request("GET", "/pod/v3/users?uid=" + commandCallerUID, headers=headersCompany)

        resComp = connComp.getresponse()
        dataComp = resComp.read()
        data_raw = str(dataComp.decode('utf-8'))
        # data_dict = ast.literal_eval(data_raw)
        data_dict = json.loads(str(data_raw))

        dataRender = json.dumps(data_dict, indent=2)
        d_org = json.loads(dataRender)

        for index_org in range(len(d_org["users"])):
            firstName = d_org["users"][index_org]["firstName"]
            lastName = d_org["users"][index_org]["lastName"]
            displayName = d_org["users"][index_org]["displayName"]
            #companyName = d_org["users"][index_org]["company"]
            companyNameTemp = d_org["users"][index_org]["company"]
            companyTemp = str(companyNameTemp).replace("&", "&amp;").replace("<", "&lt;").replace('"', "&quot;").replace("'", "&apos;").replace(">", "&gt;")
            companyName = str(companyTemp)
            userID = str(d_org["users"][index_org]["id"])
            #emailAddress = str(d_org["users"][index_org]["emailAddress"])

        botlog.LogSymphonyInfo(firstName + " " + lastName + " (" + displayName + ") from Company/Pod name: " + str(companyName) + " with UID: " + str(userID))
        callerCheck = (firstName + " " + lastName + " - " + displayName + " - " + companyName + " - " + str(userID))

        # if callerCheck in AccessFile:
        if companyName in _configDef['AuthCompany']['PodList']:

            botlog.LogSymphonyInfo("Bot Call - Google translate")

            try:

                transText = messageDetail.Command.MessageText

                if transText:

                    botlog.LogSymphonyInfo('Attempting to translate: ' + transText)

                    payload = {"client": "gtx", "sl": "auto", "tl": "en", "dt": "t", "q": transText}
                    transEP = "https://translate.googleapis.com/translate_a/single"

                    response = requests.get(transEP, params=payload).json()
                    translation = response[0][0][0]
                    lang = response[2]
                    msg = 'I think you said: ' + translation + ' (' + lang + ')'
                else:
                    msg = 'Please include a word or sentence to be translated.'

                messaging.SendSymphonyMessage(messageDetail.StreamId, msg)
            except:
                botlog.LogSymphonyInfo("Translate did not work")
    except:
        botlog.LogSymphonyInfo("Translate did not work")

    # except:
    #     try:
    #         botlog.LogSymphonyInfo("Inside second Translate")
    #         transText = messageDetail.Command.MessageText
    #
    #         if transText:
    #
    #             botlog.LogSymphonyInfo('Attempting to translate: ' + transText)
    #
    #             payload = {"client": "gtx", "sl": "auto", "tl": "en", "dt": "t", "q": transText}
    #             transEP = "https://translate.googleapis.com/translate_a/single"
    #
    #             response = requests.get(transEP, params=payload).json()
    #             translation = response[0][0][0]
    #             lang = response[2]
    #             msg = 'I think you said: ' + translation + ' (' + lang + ')'
    #         else:
    #             msg = 'Please include a word or sentence to be translated.'
    #
    #         messaging.SendSymphonyMessage(messageDetail.StreamId, msg)
    #     except:
    #         botlog.LogSymphonyInfo("Google Translate did not work entirely")


# https://www.alphavantage.co/documentation/
def GetAlphaVantageStockQuote(messageDetail):

    try:

        commandCallerUID = messageDetail.FromUserId

        connComp.request("GET", "/pod/v3/users?uid=" + commandCallerUID, headers=headersCompany)

        resComp = connComp.getresponse()
        dataComp = resComp.read()
        data_raw = str(dataComp.decode('utf-8'))
        # data_dict = ast.literal_eval(data_raw)
        data_dict = json.loads(str(data_raw))

        dataRender = json.dumps(data_dict, indent=2)
        d_org = json.loads(dataRender)

        for index_org in range(len(d_org["users"])):
            firstName = d_org["users"][index_org]["firstName"]
            lastName = d_org["users"][index_org]["lastName"]
            displayName = d_org["users"][index_org]["displayName"]
            #companyName = d_org["users"][index_org]["company"]
            companyNameTemp = d_org["users"][index_org]["company"]
            companyTemp = str(companyNameTemp).replace("&", "&amp;").replace("<", "&lt;").replace('"', "&quot;").replace("'", "&apos;").replace(">", "&gt;")
            companyName = str(companyTemp)
            userID = str(d_org["users"][index_org]["id"])
            #emailAddress = str(d_org["users"][index_org]["emailAddress"])

        botlog.LogSymphonyInfo(firstName + " " + lastName + " (" + displayName + ") from Company/Pod name: " + str(companyName) + " with UID: " + str(userID))
        callerCheck = (firstName + " " + lastName + " - " + displayName + " - " + companyName + " - " + str(userID))

        if callerCheck in AccessFile:

            botlog.LogSymphonyInfo("Bot call - Alpha Vantage Stock Quote")

            quoteText = messageDetail.Command.MessageText

            try:
                avAPIKey = botconfig.GetCommandSetting('alphavantage')['apikey']

                quoteSymbol = quoteText.split()[0]

                payload = {"function": "TIME_SERIES_DAILY", "apikey": avAPIKey, "symbol": quoteSymbol}
                avEP = 'https://www.alphavantage.co/query'
                response = requests.get(avEP, params=payload).json()

                tsDate = sorted(list(response['Time Series (Daily)'].keys()), reverse=True)[0]
                tsOpen = response['Time Series (Daily)'][tsDate]['1. open']
                tsClose = response['Time Series (Daily)'][tsDate]['4. close']

                msg = 'Quote for: ' + quoteText + '<br/>Date: ' + tsDate + '<br/>Open: ' + tsOpen
                msg += '<br/>Close: ' + tsClose + ''

                messaging.SendSymphonyMessage(messageDetail.StreamId, msg)

            except Exception as ex:
                errorStr = "Symphony REST Exception (system): {}".format(ex)
                botlog.LogSystemError(errorStr)
                msg = "Sorry, I could not return a quote."
                messaging.SendSymphonyMessage(messageDetail.StreamId, msg)
    except:
        botlog.LogSymphonyInfo("AlphaQupte did not work entirely")


def GetGiphyImage(messageDetail):

    try:

        commandCallerUID = messageDetail.FromUserId

        connComp.request("GET", "/pod/v3/users?uid=" + commandCallerUID, headers=headersCompany)

        resComp = connComp.getresponse()
        dataComp = resComp.read()
        data_raw = str(dataComp.decode('utf-8'))
        # data_dict = ast.literal_eval(data_raw)
        data_dict = json.loads(str(data_raw))

        dataRender = json.dumps(data_dict, indent=2)
        d_org = json.loads(dataRender)

        for index_org in range(len(d_org["users"])):
            firstName = d_org["users"][index_org]["firstName"]
            lastName = d_org["users"][index_org]["lastName"]
            displayName = d_org["users"][index_org]["displayName"]
            #companyName = d_org["users"][index_org]["company"]
            companyNameTemp = d_org["users"][index_org]["company"]
            companyTemp = str(companyNameTemp).replace("&", "&amp;").replace("<", "&lt;").replace('"', "&quot;").replace("'", "&apos;").replace(">", "&gt;")
            companyName = str(companyTemp)
            userID = str(d_org["users"][index_org]["id"])
            #emailAddress = str(d_org["users"][index_org]["emailAddress"])

        botlog.LogSymphonyInfo(firstName + " " + lastName + " (" + displayName + ") from Company/Pod name: " + str(companyName) + " with UID: " + str(userID))
        callerCheck = (firstName + " " + lastName + " - " + displayName + " - " + companyName + " - " + str(userID))

        # if callerCheck in AccessFile:
        if companyName in _configDef['AuthCompany']['PodList']:

            botlog.LogSymphonyInfo("Bot Call - Giphy")
            try:
                giphyAPIKey = botconfig.GetCommandSetting('giphy')['apikey']

                giphyText = messageDetail.Command.MessageText

                paramList = giphyText.split()

                isRandom = len(paramList) == 0 or paramList[0] == 'random'

                if isRandom:
                    ep = "http://api.giphy.com/v1/gifs/random"
                    payload = {"apikey": giphyAPIKey}
                else:
                    ep = "http://api.giphy.com/v1/gifs/translate"
                    payload = {"apikey": giphyAPIKey, "s": giphyText}

                response = requests.get(ep, params=payload).json()

                if isRandom:
                    #msg = "<img src='" + response['data']['image_original_url'] + "'/>"
                    gifimagelink = (response['data']['image_original_url'])
                    #msg = "<card iconSrc=\"https://thumb.ibb.co/csXBgU/Symphony2018_App_Icon_Mobile.png\" accent=\"tempo-bg-color--blue\"><header>(Click to view the GIF)</header><body><img src=\"" + gifimagelink + "\"/><br/><a href=\"" + gifimagelink + "\"/></body></card>"
                    msg = "<card iconSrc=\"\" accent=\"tempo-bg-color--blue\"><header>(Click to view the GIF)</header><body><img src=\"" + gifimagelink + "\"/><br/><a href=\"" + gifimagelink + "\"/></body></card>"


                else:
                    gifimagelink = (response['data']['images']['original']['url'])
                    #print(*paramList)

                    #joins all the elements of the array
                    header = ' '.join(paramList)

                    #msg = "<card iconSrc=\"https://thumb.ibb.co/csXBgU/Symphony2018_App_Icon_Mobile.png\" accent=\"tempo-bg-color--blue\"><header> You searched Giphy for: \"<b>"+ header +"</b>\" (click to view GIF)</header><body><img src=\"" + gifimagelink + "\"/><br/><a href=\"" + gifimagelink + "\"/></body></card>"
                    msg = "<card iconSrc=\"\" accent=\"tempo-bg-color--blue\"><header> You searched Giphy for: \"<b>"+ header +"</b>\" (click to view GIF)</header><body><img src=\"" + gifimagelink + "\"/><br/><a href=\"" + gifimagelink + "\"/></body></card>"

                messaging.SendSymphonyMessageV2(messageDetail.StreamId, msg)

            except Exception as ex:
                errorStr = "Symphony REST Exception (system): {}".format(ex)
                botlog.LogSystemError(errorStr)
                msg = "Sorry, I could not return a GIF right now."
                messaging.SendSymphonyMessage(messageDetail.StreamId, msg)
    except:
        try:
            botlog.LogSymphonyInfo("Inside secong Giphy")
            try:
                giphyAPIKey = botconfig.GetCommandSetting('giphy')['apikey']

                giphyText = messageDetail.Command.MessageText

                paramList = giphyText.split()

                isRandom = len(paramList) == 0 or paramList[0] == 'random'

                if isRandom:
                    ep = "http://api.giphy.com/v1/gifs/random"
                    payload = {"apikey": giphyAPIKey}
                else:
                    ep = "http://api.giphy.com/v1/gifs/translate"
                    payload = {"apikey": giphyAPIKey, "s": giphyText}

                response = requests.get(ep, params=payload).json()

                if isRandom:
                    #msg = "<img src='" + response['data']['image_original_url'] + "'/>"
                    gifimagelink = (response['data']['image_original_url'])
                    #msg = "<card iconSrc=\"https://thumb.ibb.co/csXBgU/Symphony2018_App_Icon_Mobile.png\" accent=\"tempo-bg-color--blue\"><header>(Click to view the GIF)</header><body><img src=\"" + gifimagelink + "\"/><br/><a href=\"" + gifimagelink + "\"/></body></card>"
                    msg = "<card iconSrc=\"\" accent=\"tempo-bg-color--blue\"><header>(Click to view the GIF)</header><body><img src=\"" + gifimagelink + "\"/><br/><a href=\"" + gifimagelink + "\"/></body></card>"

                else:
                    gifimagelink = (response['data']['images']['original']['url'])
                    #print(*paramList)

                    #joins all the elements of the array
                    header = ' '.join(paramList)

                    #msg = "<card iconSrc=\"https://thumb.ibb.co/csXBgU/Symphony2018_App_Icon_Mobile.png\" accent=\"tempo-bg-color--blue\"><header> You searched Giphy for: \"<b>"+ header +"</b>\" (click to view GIF)</header><body><img src=\"" + gifimagelink + "\"/><br/><a href=\"" + gifimagelink + "\"/></body></card>"
                    msg = "<card iconSrc=\"\" accent=\"tempo-bg-color--blue\"><header> You searched Giphy for: \"<b>"+ header +"</b>\" (click to view GIF)</header><body><img src=\"" + gifimagelink + "\"/><br/><a href=\"" + gifimagelink + "\"/></body></card>"


                messaging.SendSymphonyMessageV2(messageDetail.StreamId, msg)

            except Exception as ex:
                errorStr = "Symphony REST Exception (system): {}".format(ex)
                botlog.LogSystemError(errorStr)
                msg = "Sorry, I could not return a GIF right now."
                messaging.SendSymphonyMessage(messageDetail.StreamId, msg)
        except:
            botlog.LogSymphonyInfo("Giphy did not work entirely")

def QoD (messageDetail):

    try:

        commandCallerUID = messageDetail.FromUserId

        connComp.request("GET", "/pod/v3/users?uid=" + commandCallerUID, headers=headersCompany)

        resComp = connComp.getresponse()
        dataComp = resComp.read()
        data_raw = str(dataComp.decode('utf-8'))
        # data_dict = ast.literal_eval(data_raw)
        data_dict = json.loads(str(data_raw))

        dataRender = json.dumps(data_dict, indent=2)
        d_org = json.loads(dataRender)

        for index_org in range(len(d_org["users"])):
            firstName = d_org["users"][index_org]["firstName"]
            lastName = d_org["users"][index_org]["lastName"]
            displayName = d_org["users"][index_org]["displayName"]
            #companyName = d_org["users"][index_org]["company"]
            companyNameTemp = d_org["users"][index_org]["company"]
            companyTemp = str(companyNameTemp).replace("&", "&amp;").replace("<", "&lt;").replace('"', "&quot;").replace("'", "&apos;").replace(">", "&gt;")
            companyName = str(companyTemp)
            userID = str(d_org["users"][index_org]["id"])
            #emailAddress = str(d_org["users"][index_org]["emailAddress"])

        botlog.LogSymphonyInfo(firstName + " " + lastName + " (" + displayName + ") from Company/Pod name: " + str(companyName) + " with UID: " + str(userID))
        callerCheck = (firstName + " " + lastName + " - " + displayName + " - " + companyName + " - " + str(userID))

        # if callerCheck in AccessFile:
        if companyName in _configDef['AuthCompany']['PodList']:

            botlog.LogSymphonyInfo("Bot Call: Quote of the Day")

            try:

                qodtext = messageDetail.Command.MessageText

                qodcheck = qodtext.split()

                isRandom = len(qodcheck) == 0 or qodcheck[0] == ""

                messageDetail.ReplyToChat("Please ponder on the following Quote:")

                if isRandom:

                    conn = http.client.HTTPConnection("quotes.rest")
                    headers = {
                        'cache-control': "no-cache",
                    }
                    conn.request("GET", "/qod", headers=headers)
                    res = conn.getresponse()
                    data = res.read()
                    parsed = json.loads(data)
                    parsedData = (json.dumps(parsed, indent=4))
                    #print("parsedData: " + parsedData)
                    qodraw = (data.decode("utf-8")).replace("\n", "")
                    #print("qodraw: " + str(qodraw))

                    qodrawsplit = qodraw.split("\":")
                    checklen = len(qodrawsplit)

                    if checklen == 4:
                        return messageDetail.ReplyToChat("Quote of the Day will be live again tomorrow :)")
                    else:

                        qodrawsplitdata = str(qodrawsplit[5][2:][:-23])
                        qodrawsplitdata = qodrawsplitdata.replace("\",", "")
                        qodrawsplitAuhor = str(qodrawsplit[7][2:][:-21])
                        qodrawsplitAuhor = qodrawsplitAuhor.replace("\",", "")

                        msg = "<card accent=\"tempo-bg-color--blue\"><header>Quote of the Day by " + str(qodrawsplitAuhor) + "</header><body>" + str(qodrawsplitdata).replace("\\r\\n"," ").replace("\\r\\"," ") + "</body></card>"

                    return messageDetail.ReplyToChatV2(str(msg))

                else:
                    return messageDetail.ReplyToChat("Please just type /qod to get the Quote of the Day")
            except:
                botlog.LogSymphonyInfo("Quote of the Day did not work")
    except:
        try:
            botlog.LogSymphonyInfo("inside second Quote of the Day")
            try:

                qodtext = messageDetail.Command.MessageText

                qodcheck = qodtext.split()

                isRandom = len(qodcheck) == 0 or qodcheck[0] == ""

                if isRandom:

                    conn = http.client.HTTPConnection("quotes.rest")
                    headers = {
                        'cache-control': "no-cache",
                    }
                    conn.request("GET", "/qod", headers=headers)
                    res = conn.getresponse()
                    data = res.read()
                    parsed = json.loads(data)
                    parsedData = (json.dumps(parsed, indent=4))
                    #print("parsedData: " + parsedData)
                    qodraw = (data.decode("utf-8")).replace("\n", "")
                    #print("qodraw: " + str(qodraw))

                    qodrawsplit = qodraw.split("\":")
                    checklen = len(qodrawsplit)

                    if checklen == 4:
                        return messageDetail.ReplyToChat("Quote of the Day will be live again tomorrow :)")
                    else:

                        qodrawsplitdata = str(qodrawsplit[5][2:][:-23])
                        qodrawsplitdata = qodrawsplitdata.replace("\",", "")
                        qodrawsplitAuhor = str(qodrawsplit[7][2:][:-21])
                        qodrawsplitAuhor = qodrawsplitAuhor.replace("\",", "")

                        msg = "<card accent=\"tempo-bg-color--blue\"><header>Quote of the Day by " + str(qodrawsplitAuhor) + "</header><body>" + str(qodrawsplitdata).replace("\\r\\n"," ").replace("\\r\\"," ") + "</body></card>"

                    return messageDetail.ReplyToChatV2(str(msg))

                else:
                    return messageDetail.ReplyToChat("Please just type /qod to get the Quote of the Day")
            except:
                botlog.LogSymphonyInfo("Quote of the Day did not work")
        except:
            botlog.LogSymphonyInfo("Quote of the Day did not work entirely")


##########################

def QoDTask ():

    try:
        conn = http.client.HTTPConnection("quotes.rest")
        headers = {
            'cache-control': "no-cache",
        }
        conn.request("GET", "/qod", headers=headers)
        res = conn.getresponse()
        data = res.read()
        parsed = json.loads(data)
        parsedData = (json.dumps(parsed, indent=4))
        #print("parsedData: " + parsedData)
        qodraw = (data.decode("utf-8")).replace("\n", "")
        #print("qodraw: " + str(qodraw))

        qodrawsplit = qodraw.split("\":")
        checklen = len(qodrawsplit)

        if checklen == 4:
            msg = "Quote of the Day will be live again tomorrow :)"
        else:
            qodrawsplitdata = str(qodrawsplit[5][2:][:-23])
            qodrawsplitdata = qodrawsplitdata.replace("\",", "")
            qodrawsplitAuhor = str(qodrawsplit[7][2:][:-21])
            qodrawsplitAuhor = qodrawsplitAuhor.replace("\",", "")

            msg = "<card accent=\"tempo-bg-color--blue\"><header>Quote of the Day by " + str(qodrawsplitAuhor) + "</header><body>" + str(qodrawsplitdata).replace("\\r\\n"," ").replace("\\r\\"," ") + "</body></card>"
        #messaging.SendSymphonyMessageV2(_configDef['quoteOfTheDay']['stream1'], msg)
        # return messaging.SendSymphonyMessageV2(_configDef['quoteOfTheDay']['stream2'], msg)
        return messaging.SendSymphonyMessageV2(_configDef['quoteOfTheDay']['stream1'], msg)

    except:
        conn = http.client.HTTPConnection("quotes.rest")
        headers = {
            'cache-control': "no-cache",
        }
        conn.request("GET", "/qod", headers=headers)
        res = conn.getresponse()
        data = res.read()
        parsed = json.loads(data)
        parsedData = (json.dumps(parsed, indent=4))
        #print("parsedData: " + parsedData)
        qodraw = (data.decode("utf-8")).replace("\n", "")
        #print("qodraw: " + str(qodraw))

        qodrawsplit = qodraw.split("\":")
        checklen = len(qodrawsplit)

        if checklen == 4:
            msg = "Quote of the Day will be live again tomorrow :)"
        else:
            qodrawsplitdata = str(qodrawsplit[5][2:][:-23])
            qodrawsplitdata = qodrawsplitdata.replace("\",", "")
            qodrawsplitAuhor = str(qodrawsplit[7][2:][:-21])
            qodrawsplitAuhor = qodrawsplitAuhor.replace("\",", "")

            msg = "<card accent=\"tempo-bg-color--blue\"><header>Quote of the Day by " + str(qodrawsplitAuhor) + "</header><body>" + str(qodrawsplitdata).replace("\\r\\n"," ").replace("\\r\\"," ") + "</body></card>"
        messaging.SendSymphonyMessageV2(_configDef['quoteOfTheDay']['stream1'], msg)
        return messaging.SendSymphonyMessageV2(_configDef['quoteOfTheDay']['stream2'], msg)

##########################
## OLD WEATHER API ##

# def weather(messageDetail):
#
#     try:
#
#         commandCallerUID = messageDetail.FromUserId
#
#         connComp.request("GET", "/pod/v3/users?uid=" + commandCallerUID, headers=headersCompany)
#
#         resComp = connComp.getresponse()
#         dataComp = resComp.read()
#         data_raw = str(dataComp.decode('utf-8'))
#         #data_dict = ast.literal_eval(data_raw)
#         data_dict = json.loads(str(data_raw))
#
#         dataRender = json.dumps(data_dict, indent=2)
#         d_org = json.loads(dataRender)
#
#         for index_org in range(len(d_org["users"])):
#             firstName = d_org["users"][index_org]["firstName"]
#             lastName = d_org["users"][index_org]["lastName"]
#             displayName = d_org["users"][index_org]["displayName"]
#             #companyName = d_org["users"][index_org]["company"]
#             companyNameTemp = d_org["users"][index_org]["company"]
#             companyTemp = str(companyNameTemp).replace("&", "&amp;").replace("<", "&lt;").replace('"', "&quot;").replace("'", "&apos;").replace(">", "&gt;")
#             companyName = str(companyTemp)
#             userID = str(d_org["users"][index_org]["id"])
#
#         botlog.LogSymphonyInfo(firstName + " " + lastName + " (" + displayName + ") from Company/Pod name: " + str(companyName) + " with UID: " + str(userID))
#         callerCheck = (firstName + " " + lastName + " - " + displayName + " - " + companyName + " - " + str(userID))
#
#     except:
#         botlog.LogSymphonyInfo("Inside second user check")
#         commandCallerUID = messageDetail.FromUserId
#
#         connComp.request("GET", "/pod/v3/users?uid=" + commandCallerUID, headers=headersCompany)
#
#         resComp = connComp.getresponse()
#         dataComp = resComp.read()
#         data_raw = str(dataComp.decode('utf-8'))
#         #data_dict = ast.literal_eval(data_raw)
#         data_dict = json.loads(str(data_raw))
#
#         dataRender = json.dumps(data_dict, indent=2)
#         d_org = json.loads(dataRender)
#
#         for index_org in range(len(d_org["users"])):
#             firstName = d_org["users"][index_org]["firstName"]
#             lastName = d_org["users"][index_org]["lastName"]
#             displayName = d_org["users"][index_org]["displayName"]
#             #companyName = d_org["users"][index_org]["company"]
#             companyNameTemp = d_org["users"][index_org]["company"]
#             companyTemp = str(companyNameTemp).replace("&", "&amp;").replace("<", "&lt;").replace('"', "&quot;").replace("'", "&apos;").replace(">", "&gt;")
#             companyName = str(companyTemp)
#             userID = str(d_org["users"][index_org]["id"])
#
#         botlog.LogSymphonyInfo(firstName + " " + lastName + " (" + displayName + ") from Company/Pod name: " + str(companyName) + " with UID: " + str(userID))
#         callerCheck = (firstName + " " + lastName + " - " + displayName + " - " + companyName + " - " + str(userID))
#
#     # try:
#         # if callerCheck in AccessFile:
#     if companyName in _configDef['AuthCompany']['PodList']:
#         return messageDetail.ReplyToChat("Sorry, the developer is working on a new endpoint, please try this again in few days..")
#             # botlog.LogSymphonyInfo("Bot Call: Weather")
#             #
#             # # try:
#             #
#             # message = (messageDetail.Command.MessageText)
#             # weatherCatcher = message.split()
#             # location = ""
#             # days = ""
#             # rawtwo = 2
#             # two = str(rawtwo)
#             # rawthree = 3
#             # three = str(rawthree)
#             # rawfour = 4
#             # four = str(rawfour)
#             # rawfive = 5
#             # five = str(rawfive)
#             # rawsix = 6
#             # six = str(rawsix)
#             # rawseven = 7
#             # seven = str(rawseven)
#             #
#             # catchLength = len(weatherCatcher)
#             # #print("Lenght is: " + (str(catchLength)))
#             #
#             # try:
#             #     emptyLocation = catchLength == 0 or weatherCatcher[0] == ""
#             #     if emptyLocation:
#             #         return messageDetail.ReplyToChat("Please enter a location, if it is more than one word, e.g New York, please use underscore as in New_York")
#             #     else:
#             #         location = weatherCatcher[0]
#             #         #print("Location: " + location)
#             # except:
#             #     messageDetail.ReplyToChat("Loading the weather forecast")
#             #
#             # try:
#             #     emptyDays = weatherCatcher[1] == ""
#             #     if emptyDays:
#             #         days = 0
#             #     else:
#             #         days = weatherCatcher[1]
#             #         messageDetail.ReplyToChatV2("Forecasting weather for <b>" + days + "</b> days in <b>" + str(location) + "</b>")
#             #         #print("Days: " + days)
#             # except:
#             #     messageDetail.ReplyToChatV2("Forecasting weather for today in <b>" + str(location) + "</b>")
#             #
#             #
#             # conn = http.client.HTTPSConnection("api.apixu.com")
#             # headers = {
#             #     'cache-control': "no-cache",
#             # }
#             # conn.request("GET", "/v1/forecast.json?key=" + _configDef['weather']['API_Key'] + "&q=" + str(location) + "&days=" + days + "", headers=headers)
#             # res = conn.getresponse()
#             # data = res.read()
#             # d_raw = remove_emoji(data)
#             # data_new = d_raw.replace("","").replace("Å","ō")
#             # # print(data_new)
#             # # request_raw = data.decode('utf-8')
#             # data = json.dumps(data_new, indent=2)
#             # # data = json.dumps(request_raw, indent=2)
#             # data_dict = ast.literal_eval(data)
#             # d = json.loads(data_dict)
#             # # d = data
#             # print(str(d))
#             #
#             # # Checking for location validation
#             # notmatchingLocation = "{'error': {'code': 1006, 'message': 'No matching location found.'}}"
#             # #tempWeather = str(data.decode("utf-8")).replace("\"", "")
#             # tempWeather = str(d).replace("\'", "")
#             # #print("tempWeather: " + str(tempWeather))
#             #
#             # if str(d).startswith(notmatchingLocation):
#             #     return messageDetail.ReplyToChat("The location entered is not valid, please try again.")
#             # else:
#             #
#             #     # try:
#             #     # # Main weather info - to display regardless of days selected
#             #     weatherRaw = tempWeather.split(":")
#             #     LocationName = str(d["location"]["name"])
#             #     Region = str(d["location"]["region"])
#             #     Country = str(d["location"]["country"])
#             #     LastUpdated = str(d["current"]["last_updated"])
#             #     TempC = str(d["current"]["temp_c"])
#             #     TempF = str(d["current"]["temp_f"])
#             #     Condition = str(d["current"]["condition"]["text"])
#             #     CurrentURL = str(d["current"]["condition"]["icon"])
#             #
#             #     day1date = str(d["forecast"]["forecastday"][0]["date"])
#             #     day1maxtemp = str(d["forecast"]["forecastday"][0]["day"]["maxtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][0]["day"]["maxtemp_f"]) + " F"
#             #     day1mintemp = str(d["forecast"]["forecastday"][0]["day"]["mintemp_c"]) + " C / " + str(d["forecast"]["forecastday"][0]["day"]["mintemp_f"]) + " F"
#             #     day1avgtemp = str(d["forecast"]["forecastday"][0]["day"]["avgtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][0]["day"]["avgtemp_f"]) + " F"
#             #     day1maxwind = str(d["forecast"]["forecastday"][0]["day"]["maxwind_mph"]) + " mph / " + str(d["forecast"]["forecastday"][0]["day"]["maxwind_kph"]) + " kph"
#             #     day1totalprecip = str(d["forecast"]["forecastday"][0]["day"]["totalprecip_mm"]) + "mm / " + str(d["forecast"]["forecastday"][0]["day"]["totalprecip_in"]) + "in"
#             #     day1avghumidity = str(d["forecast"]["forecastday"][0]["day"]["avghumidity"])
#             #     day1condition = str(d["forecast"]["forecastday"][0]["day"]["condition"]["text"])
#             #     day1icon = str(d["forecast"]["forecastday"][0]["day"]["condition"]["icon"])
#             #     day1sunrise = str(d["forecast"]["forecastday"][0]["astro"]["sunrise"])
#             #     day1sunset = str(d["forecast"]["forecastday"][0]["astro"]["sunset"])
#             #     day1moonrise = str(d["forecast"]["forecastday"][0]["astro"]["moonrise"])
#             #     day1moonset = str(d["forecast"]["forecastday"][0]["astro"]["moonset"])
#             #     # except:
#             #     #     return messageDetail.ReplyToChat("Sorry, I am not able to get the weather, please try again later")
#             #
#             #     table_body = "<table style='table-layout:auto;width:100%'>" \
#             #                  "<thead>" \
#             #                  "<tr class=\"tempo-text-color--white tempo-bg-color--black\">" \
#             #                  "<td>Date</td>" \
#             #                  "<td>Max Temp</td>" \
#             #                  "<td>Min Temp</td>" \
#             #                  "<td>Avg Temp</td>" \
#             #                  "<td>Max Wind</td>" \
#             #                  "<td>Tot Precipitation</td>" \
#             #                  "<td>Avg Humidity</td>" \
#             #                  "<td>Condition</td>" \
#             #                  "<td></td>" \
#             #                  "<td>Sunrise</td>" \
#             #                  "<td>Sunset</td>" \
#             #                  "<td>Moonrise</td>" \
#             #                  "<td>Moonset</td>" \
#             #                  "</tr>" \
#             #                  "</thead><tbody>"
#             #
#             #     table_body += "<tr>" \
#             #                   "<td>" + day1date + "</td>" \
#             #                   "<td>" + day1maxtemp + "</td>" \
#             #                   "<td>" + day1mintemp + "</td>" \
#             #                   "<td>" + day1avgtemp + "</td>" \
#             #                   "<td>" + day1maxwind + "</td>" \
#             #                   "<td>" + day1totalprecip + "</td>" \
#             #                   "<td>" + day1avghumidity + "</td>" \
#             #                   "<td>" + day1condition + "</td>" \
#             #                   "<td><img src=\"" + day1icon + "\"/></td>" \
#             #                   "<td>" + day1sunrise + "</td>" \
#             #                   "<td>" + day1sunset + "</td>" \
#             #                   "<td>" + day1moonrise + "</td>" \
#             #                   "<td>" + day1moonset + "</td>" \
#             #                   "</tr>"
#             #
#             #     if days == two:
#             #
#             #         try:
#             #             #print("2 days")
#             #             day2date = str(d["forecast"]["forecastday"][1]["date"])
#             #             day2maxtemp = str(d["forecast"]["forecastday"][1]["day"]["maxtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][1]["day"]["maxtemp_f"]) + " F"
#             #             day2mintemp = str(d["forecast"]["forecastday"][1]["day"]["mintemp_c"]) + " C / " + str(d["forecast"]["forecastday"][1]["day"]["mintemp_f"]) + " F"
#             #             day2avgtemp = str(d["forecast"]["forecastday"][1]["day"]["avgtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][1]["day"]["avgtemp_f"]) + " F"
#             #             day2maxwind = str(d["forecast"]["forecastday"][1]["day"]["maxwind_mph"]) + " mph / " + str(d["forecast"]["forecastday"][1]["day"]["maxwind_kph"]) + " kph"
#             #             day2totalprecip = str(d["forecast"]["forecastday"][1]["day"]["totalprecip_mm"]) + "mm / " + str(d["forecast"]["forecastday"][1]["day"]["totalprecip_in"]) + "in"
#             #             day2avghumidity = str(d["forecast"]["forecastday"][1]["day"]["avghumidity"])
#             #             day2condition = str(d["forecast"]["forecastday"][1]["day"]["condition"]["text"])
#             #             day2icon = str(d["forecast"]["forecastday"][1]["day"]["condition"]["icon"])
#             #             day2sunrise = str(d["forecast"]["forecastday"][1]["astro"]["sunrise"])
#             #             day2sunset = str(d["forecast"]["forecastday"][1]["astro"]["sunset"])
#             #             day2moonrise = str(d["forecast"]["forecastday"][1]["astro"]["moonrise"])
#             #             day2moonset = str(d["forecast"]["forecastday"][1]["astro"]["moonset"])
#             #         except:
#             #             return messageDetail.ReplyToChat("Sorry, I am not able to get the weather, please try again later")
#             #
#             #         table_body += "<tr><td>" + day2date + "</td><td>" + day2maxtemp + "</td><td>" + day2mintemp + "</td><td>" + day2avgtemp + "</td><td>" + day2maxwind + "</td><td>" + day2totalprecip + "</td><td>" + day2avghumidity + "</td><td>" + day2condition + "</td><td><img src=\"" + day2icon + "\"/></td><td>" + day2sunrise + "</td><td>" + day2sunset + "</td><td>" + day2moonrise + "</td><td>" + day2moonset + "</td></tr>"
#             #
#             #     if days == three:
#             #
#             #         try:
#             #             #print("2 days")
#             #             day2date = str(d["forecast"]["forecastday"][1]["date"])
#             #             day2maxtemp = str(d["forecast"]["forecastday"][1]["day"]["maxtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][1]["day"]["maxtemp_f"]) + " F"
#             #             day2mintemp = str(d["forecast"]["forecastday"][1]["day"]["mintemp_c"]) + " C / " + str(d["forecast"]["forecastday"][1]["day"]["mintemp_f"]) + " F"
#             #             day2avgtemp = str(d["forecast"]["forecastday"][1]["day"]["avgtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][1]["day"]["avgtemp_f"]) + " F"
#             #             day2maxwind = str(d["forecast"]["forecastday"][1]["day"]["maxwind_mph"]) + " mph / " + str(d["forecast"]["forecastday"][1]["day"]["maxwind_kph"]) + " kph"
#             #             day2totalprecip = str(d["forecast"]["forecastday"][1]["day"]["totalprecip_mm"]) + "mm / " + str(d["forecast"]["forecastday"][1]["day"]["totalprecip_in"]) + "in"
#             #             day2avghumidity = str(d["forecast"]["forecastday"][1]["day"]["avghumidity"])
#             #             day2condition = str(d["forecast"]["forecastday"][1]["day"]["condition"]["text"])
#             #             day2icon = str(d["forecast"]["forecastday"][1]["day"]["condition"]["icon"])
#             #             day2sunrise = str(d["forecast"]["forecastday"][1]["astro"]["sunrise"])
#             #             day2sunset = str(d["forecast"]["forecastday"][1]["astro"]["sunset"])
#             #             day2moonrise = str(d["forecast"]["forecastday"][1]["astro"]["moonrise"])
#             #             day2moonset = str(d["forecast"]["forecastday"][1]["astro"]["moonset"])
#             #         except:
#             #             return messageDetail.ReplyToChat("Sorry, I am not able to get the weather, please try again later")
#             #
#             #         table_body += "<tr><td>" + day2date + "</td><td>" + day2maxtemp + "</td><td>" + day2mintemp + "</td><td>" + day2avgtemp + "</td><td>" + day2maxwind + "</td><td>" + day2totalprecip + "</td><td>" + day2avghumidity + "</td><td>" + day2condition + "</td><td><img src=\"" + day2icon + "\"/></td><td>" + day2sunrise + "</td><td>" + day2sunset + "</td><td>" + day2moonrise + "</td><td>" + day2moonset + "</td></tr>"
#             #
#             #         try:
#             #             #print("3 days")
#             #             day3date = str(d["forecast"]["forecastday"][2]["date"])
#             #             day3maxtemp = str(d["forecast"]["forecastday"][2]["day"]["maxtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][2]["day"]["maxtemp_f"]) + " F"
#             #             day3mintemp = str(d["forecast"]["forecastday"][2]["day"]["mintemp_c"]) + " C / " + str(d["forecast"]["forecastday"][2]["day"]["mintemp_f"]) + " F"
#             #             day3avgtemp = str(d["forecast"]["forecastday"][2]["day"]["avgtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][2]["day"]["avgtemp_f"]) + " F"
#             #             day3maxwind = str(d["forecast"]["forecastday"][2]["day"]["maxwind_mph"]) + " mph / " + str(d["forecast"]["forecastday"][2]["day"]["maxwind_kph"]) + " kph"
#             #             day3totalprecip = str(d["forecast"]["forecastday"][2]["day"]["totalprecip_mm"]) + "mm / " + str(d["forecast"]["forecastday"][2]["day"]["totalprecip_in"]) + "in"
#             #             day3avghumidity = str(d["forecast"]["forecastday"][2]["day"]["avghumidity"])
#             #             day3condition = str(d["forecast"]["forecastday"][2]["day"]["condition"]["text"])
#             #             day3icon = str(d["forecast"]["forecastday"][2]["day"]["condition"]["icon"])
#             #             day3sunrise = str(d["forecast"]["forecastday"][2]["astro"]["sunrise"])
#             #             day3sunset = str(d["forecast"]["forecastday"][2]["astro"]["sunset"])
#             #             day3moonrise = str(d["forecast"]["forecastday"][2]["astro"]["moonrise"])
#             #             day3moonset = str(d["forecast"]["forecastday"][2]["astro"]["moonset"])
#             #         except:
#             #             return messageDetail.ReplyToChat("Sorry, I am not able to get the weather, please try again later")
#             #
#             #         table_body += "<tr><td>" + day3date + "</td><td>" + day3maxtemp + "</td><td>" + day3mintemp + "</td><td>" + day3avgtemp + "</td><td>" + day3maxwind + "</td><td>" + day3totalprecip + "</td><td>" + day3avghumidity + "</td><td>" + day3condition + "</td><td><img src=\"" + day3icon + "\"/></td><td>" + day3sunrise + "</td><td>" + day3sunset + "</td><td>" + day3moonrise + "</td><td>" + day3moonset + "</td></tr>"
#             #
#             #
#             #     if days == four:
#             #
#             #         try:
#             #             #print("2 days")
#             #             day2date = str(d["forecast"]["forecastday"][1]["date"])
#             #             day2maxtemp = str(d["forecast"]["forecastday"][1]["day"]["maxtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][1]["day"]["maxtemp_f"]) + " F"
#             #             day2mintemp = str(d["forecast"]["forecastday"][1]["day"]["mintemp_c"]) + " C / " + str(d["forecast"]["forecastday"][1]["day"]["mintemp_f"]) + " F"
#             #             day2avgtemp = str(d["forecast"]["forecastday"][1]["day"]["avgtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][1]["day"]["avgtemp_f"]) + " F"
#             #             day2maxwind = str(d["forecast"]["forecastday"][1]["day"]["maxwind_mph"]) + " mph / " + str(d["forecast"]["forecastday"][1]["day"]["maxwind_kph"]) + " kph"
#             #             day2totalprecip = str(d["forecast"]["forecastday"][1]["day"]["totalprecip_mm"]) + "mm / " + str(d["forecast"]["forecastday"][1]["day"]["totalprecip_in"]) + "in"
#             #             day2avghumidity = str(d["forecast"]["forecastday"][1]["day"]["avghumidity"])
#             #             day2condition = str(d["forecast"]["forecastday"][1]["day"]["condition"]["text"])
#             #             day2icon = str(d["forecast"]["forecastday"][1]["day"]["condition"]["icon"])
#             #             day2sunrise = str(d["forecast"]["forecastday"][1]["astro"]["sunrise"])
#             #             day2sunset = str(d["forecast"]["forecastday"][1]["astro"]["sunset"])
#             #             day2moonrise = str(d["forecast"]["forecastday"][1]["astro"]["moonrise"])
#             #             day2moonset = str(d["forecast"]["forecastday"][1]["astro"]["moonset"])
#             #         except:
#             #             return messageDetail.ReplyToChat("Sorry, I am not able to get the weather, please try again later")
#             #
#             #         table_body += "<tr><td>" + day2date + "</td><td>" + day2maxtemp + "</td><td>" + day2mintemp + "</td><td>" + day2avgtemp + "</td><td>" + day2maxwind + "</td><td>" + day2totalprecip + "</td><td>" + day2avghumidity + "</td><td>" + day2condition + "</td><td><img src=\"" + day2icon + "\"/></td><td>" + day2sunrise + "</td><td>" + day2sunset + "</td><td>" + day2moonrise + "</td><td>" + day2moonset + "</td></tr>"
#             #
#             #         try:
#             #             #print("3 days")
#             #             day3date = str(d["forecast"]["forecastday"][2]["date"])
#             #             day3maxtemp = str(d["forecast"]["forecastday"][2]["day"]["maxtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][2]["day"]["maxtemp_f"]) + " F"
#             #             day3mintemp = str(d["forecast"]["forecastday"][2]["day"]["mintemp_c"]) + " C / " + str(d["forecast"]["forecastday"][2]["day"]["mintemp_f"]) + " F"
#             #             day3avgtemp = str(d["forecast"]["forecastday"][2]["day"]["avgtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][2]["day"]["avgtemp_f"]) + " F"
#             #             day3maxwind = str(d["forecast"]["forecastday"][2]["day"]["maxwind_mph"]) + " mph / " + str(d["forecast"]["forecastday"][2]["day"]["maxwind_kph"]) + " kph"
#             #             day3totalprecip = str(d["forecast"]["forecastday"][2]["day"]["totalprecip_mm"]) + "mm / " + str(d["forecast"]["forecastday"][2]["day"]["totalprecip_in"]) + "in"
#             #             day3avghumidity = str(d["forecast"]["forecastday"][2]["day"]["avghumidity"])
#             #             day3condition = str(d["forecast"]["forecastday"][2]["day"]["condition"]["text"])
#             #             day3icon = str(d["forecast"]["forecastday"][2]["day"]["condition"]["icon"])
#             #             day3sunrise = str(d["forecast"]["forecastday"][2]["astro"]["sunrise"])
#             #             day3sunset = str(d["forecast"]["forecastday"][2]["astro"]["sunset"])
#             #             day3moonrise = str(d["forecast"]["forecastday"][2]["astro"]["moonrise"])
#             #             day3moonset = str(d["forecast"]["forecastday"][2]["astro"]["moonset"])
#             #         except:
#             #             return messageDetail.ReplyToChat("Sorry, I am not able to get the weather, please try again later")
#             #
#             #         table_body += "<tr><td>" + day3date + "</td><td>" + day3maxtemp + "</td><td>" + day3mintemp + "</td><td>" + day3avgtemp + "</td><td>" + day3maxwind + "</td><td>" + day3totalprecip + "</td><td>" + day3avghumidity + "</td><td>" + day3condition + "</td><td><img src=\"" + day3icon + "\"/></td><td>" + day3sunrise + "</td><td>" + day3sunset + "</td><td>" + day3moonrise + "</td><td>" + day3moonset + "</td></tr>"
#             #
#             #         try:
#             #             #print("4 days")
#             #             day4date = str(d["forecast"]["forecastday"][3]["date"])
#             #             day4maxtemp = str(d["forecast"]["forecastday"][3]["day"]["maxtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][3]["day"]["maxtemp_f"]) + " F"
#             #             day4mintemp = str(d["forecast"]["forecastday"][3]["day"]["mintemp_c"]) + " C / " + str(d["forecast"]["forecastday"][3]["day"]["mintemp_f"]) + " F"
#             #             day4avgtemp = str(d["forecast"]["forecastday"][3]["day"]["avgtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][3]["day"]["avgtemp_f"]) + " F"
#             #             day4maxwind = str(d["forecast"]["forecastday"][3]["day"]["maxwind_mph"]) + " mph / " + str(d["forecast"]["forecastday"][3]["day"]["maxwind_kph"]) + " kph"
#             #             day4totalprecip = str(d["forecast"]["forecastday"][3]["day"]["totalprecip_mm"]) + "mm / " + str(d["forecast"]["forecastday"][3]["day"]["totalprecip_in"]) + "in"
#             #             day4avghumidity = str(d["forecast"]["forecastday"][3]["day"]["avghumidity"])
#             #             day4condition = str(d["forecast"]["forecastday"][3]["day"]["condition"]["text"])
#             #             day4icon = str(d["forecast"]["forecastday"][3]["day"]["condition"]["icon"])
#             #             day4sunrise = str(d["forecast"]["forecastday"][3]["astro"]["sunrise"])
#             #             day4sunset = str(d["forecast"]["forecastday"][3]["astro"]["sunset"])
#             #             day4moonrise = str(d["forecast"]["forecastday"][3]["astro"]["moonrise"])
#             #             day4moonset = str(d["forecast"]["forecastday"][3]["astro"]["moonset"])
#             #         except:
#             #             return messageDetail.ReplyToChat("Sorry, I am not able to get the weather, please try again later")
#             #
#             #         table_body += "<tr><td>" + day4date + "</td><td>" + day4maxtemp + "</td><td>" + day4mintemp + "</td><td>" + day4avgtemp + "</td><td>" + day4maxwind + "</td><td>" + day4totalprecip + "</td><td>" + day4avghumidity + "</td><td>" + day4condition + "</td><td><img src=\"" + day4icon + "\"/></td><td>" + day4sunrise + "</td><td>" + day4sunset + "</td><td>" + day4moonrise + "</td><td>" + day4moonset + "</td></tr>"
#             #
#             #     if days == five:
#             #         try:
#             #             #print("2 days")
#             #             day2date = str(d["forecast"]["forecastday"][1]["date"])
#             #             day2maxtemp = str(d["forecast"]["forecastday"][1]["day"]["maxtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][1]["day"]["maxtemp_f"]) + " F"
#             #             day2mintemp = str(d["forecast"]["forecastday"][1]["day"]["mintemp_c"]) + " C / " + str(d["forecast"]["forecastday"][1]["day"]["mintemp_f"]) + " F"
#             #             day2avgtemp = str(d["forecast"]["forecastday"][1]["day"]["avgtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][1]["day"]["avgtemp_f"]) + " F"
#             #             day2maxwind = str(d["forecast"]["forecastday"][1]["day"]["maxwind_mph"]) + " mph / " + str(d["forecast"]["forecastday"][1]["day"]["maxwind_kph"]) + " kph"
#             #             day2totalprecip = str(d["forecast"]["forecastday"][1]["day"]["totalprecip_mm"]) + "mm / " + str(d["forecast"]["forecastday"][1]["day"]["totalprecip_in"]) + "in"
#             #             day2avghumidity = str(d["forecast"]["forecastday"][1]["day"]["avghumidity"])
#             #             day2condition = str(d["forecast"]["forecastday"][1]["day"]["condition"]["text"])
#             #             day2icon = str(d["forecast"]["forecastday"][1]["day"]["condition"]["icon"])
#             #             day2sunrise = str(d["forecast"]["forecastday"][1]["astro"]["sunrise"])
#             #             day2sunset = str(d["forecast"]["forecastday"][1]["astro"]["sunset"])
#             #             day2moonrise = str(d["forecast"]["forecastday"][1]["astro"]["moonrise"])
#             #             day2moonset = str(d["forecast"]["forecastday"][1]["astro"]["moonset"])
#             #         except:
#             #             return messageDetail.ReplyToChat("Sorry, I am not able to get the weather, please try again later")
#             #
#             #         table_body += "<tr><td>" + day2date + "</td><td>" + day2maxtemp + "</td><td>" + day2mintemp + "</td><td>" + day2avgtemp + "</td><td>" + day2maxwind + "</td><td>" + day2totalprecip + "</td><td>" + day2avghumidity + "</td><td>" + day2condition + "</td><td><img src=\"" + day2icon + "\"/></td><td>" + day2sunrise + "</td><td>" + day2sunset + "</td><td>" + day2moonrise + "</td><td>" + day2moonset + "</td></tr>"
#             #
#             #         try:
#             #             #print("3 days")
#             #             day3date = str(d["forecast"]["forecastday"][2]["date"])
#             #             day3maxtemp = str(d["forecast"]["forecastday"][2]["day"]["maxtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][2]["day"]["maxtemp_f"]) + " F"
#             #             day3mintemp = str(d["forecast"]["forecastday"][2]["day"]["mintemp_c"]) + " C / " + str(d["forecast"]["forecastday"][2]["day"]["mintemp_f"]) + " F"
#             #             day3avgtemp = str(d["forecast"]["forecastday"][2]["day"]["avgtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][2]["day"]["avgtemp_f"]) + " F"
#             #             day3maxwind = str(d["forecast"]["forecastday"][2]["day"]["maxwind_mph"]) + " mph / " + str(d["forecast"]["forecastday"][2]["day"]["maxwind_kph"]) + " kph"
#             #             day3totalprecip = str(d["forecast"]["forecastday"][2]["day"]["totalprecip_mm"]) + "mm / " + str(d["forecast"]["forecastday"][2]["day"]["totalprecip_in"]) + "in"
#             #             day3avghumidity = str(d["forecast"]["forecastday"][2]["day"]["avghumidity"])
#             #             day3condition = str(d["forecast"]["forecastday"][2]["day"]["condition"]["text"])
#             #             day3icon = str(d["forecast"]["forecastday"][2]["day"]["condition"]["icon"])
#             #             day3sunrise = str(d["forecast"]["forecastday"][2]["astro"]["sunrise"])
#             #             day3sunset = str(d["forecast"]["forecastday"][2]["astro"]["sunset"])
#             #             day3moonrise = str(d["forecast"]["forecastday"][2]["astro"]["moonrise"])
#             #             day3moonset = str(d["forecast"]["forecastday"][2]["astro"]["moonset"])
#             #         except:
#             #             return messageDetail.ReplyToChat("Sorry, I am not able to get the weather, please try again later")
#             #
#             #         table_body += "<tr><td>" + day3date + "</td><td>" + day3maxtemp + "</td><td>" + day3mintemp + "</td><td>" + day3avgtemp + "</td><td>" + day3maxwind + "</td><td>" + day3totalprecip + "</td><td>" + day3avghumidity + "</td><td>" + day3condition + "</td><td><img src=\"" + day3icon + "\"/></td><td>" + day3sunrise + "</td><td>" + day3sunset + "</td><td>" + day3moonrise + "</td><td>" + day3moonset + "</td></tr>"
#             #
#             #         try:
#             #             #print("4 days")
#             #             day4date = str(d["forecast"]["forecastday"][3]["date"])
#             #             day4maxtemp = str(d["forecast"]["forecastday"][3]["day"]["maxtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][3]["day"]["maxtemp_f"]) + " F"
#             #             day4mintemp = str(d["forecast"]["forecastday"][3]["day"]["mintemp_c"]) + " C / " + str(d["forecast"]["forecastday"][3]["day"]["mintemp_f"]) + " F"
#             #             day4avgtemp = str(d["forecast"]["forecastday"][3]["day"]["avgtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][3]["day"]["avgtemp_f"]) + " F"
#             #             day4maxwind = str(d["forecast"]["forecastday"][3]["day"]["maxwind_mph"]) + " mph / " + str(d["forecast"]["forecastday"][3]["day"]["maxwind_kph"]) + " kph"
#             #             day4totalprecip = str(d["forecast"]["forecastday"][3]["day"]["totalprecip_mm"]) + "mm / " + str(d["forecast"]["forecastday"][3]["day"]["totalprecip_in"]) + "in"
#             #             day4avghumidity = str(d["forecast"]["forecastday"][3]["day"]["avghumidity"])
#             #             day4condition = str(d["forecast"]["forecastday"][3]["day"]["condition"]["text"])
#             #             day4icon = str(d["forecast"]["forecastday"][3]["day"]["condition"]["icon"])
#             #             day4sunrise = str(d["forecast"]["forecastday"][3]["astro"]["sunrise"])
#             #             day4sunset = str(d["forecast"]["forecastday"][3]["astro"]["sunset"])
#             #             day4moonrise = str(d["forecast"]["forecastday"][3]["astro"]["moonrise"])
#             #             day4moonset = str(d["forecast"]["forecastday"][3]["astro"]["moonset"])
#             #         except:
#             #             return messageDetail.ReplyToChat("Sorry, I am not able to get the weather, please try again later")
#             #
#             #         table_body += "<tr><td>" + day4date + "</td><td>" + day4maxtemp + "</td><td>" + day4mintemp + "</td><td>" + day4avgtemp + "</td><td>" + day4maxwind + "</td><td>" + day4totalprecip + "</td><td>" + day4avghumidity + "</td><td>" + day4condition + "</td><td><img src=\"" + day4icon + "\"/></td><td>" + day4sunrise + "</td><td>" + day4sunset + "</td><td>" + day4moonrise + "</td><td>" + day4moonset + "</td></tr>"
#             #
#             #         try:
#             #             #print("5 days")
#             #             day5date = str(d["forecast"]["forecastday"][4]["date"])
#             #             day5maxtemp = str(d["forecast"]["forecastday"][4]["day"]["maxtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][4]["day"]["maxtemp_f"]) + " F"
#             #             day5mintemp = str(d["forecast"]["forecastday"][4]["day"]["mintemp_c"]) + " C / " + str(d["forecast"]["forecastday"][4]["day"]["mintemp_f"]) + " F"
#             #             day5avgtemp = str(d["forecast"]["forecastday"][4]["day"]["avgtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][4]["day"]["avgtemp_f"]) + " F"
#             #             day5maxwind = str(d["forecast"]["forecastday"][4]["day"]["maxwind_mph"]) + " mph / " + str(d["forecast"]["forecastday"][4]["day"]["maxwind_kph"]) + " kph"
#             #             day5totalprecip = str(d["forecast"]["forecastday"][4]["day"]["totalprecip_mm"]) + "mm / " + str(d["forecast"]["forecastday"][4]["day"]["totalprecip_in"]) + "in"
#             #             day5avghumidity = str(d["forecast"]["forecastday"][4]["day"]["avghumidity"])
#             #             day5condition = str(d["forecast"]["forecastday"][4]["day"]["condition"]["text"])
#             #             day5icon = str(d["forecast"]["forecastday"][4]["day"]["condition"]["icon"])
#             #             day5sunrise = str(d["forecast"]["forecastday"][4]["astro"]["sunrise"])
#             #             day5sunset = str(d["forecast"]["forecastday"][4]["astro"]["sunset"])
#             #             day5moonrise = str(d["forecast"]["forecastday"][4]["astro"]["moonrise"])
#             #             day5moonset = str(d["forecast"]["forecastday"][4]["astro"]["moonset"])
#             #         except:
#             #             return messageDetail.ReplyToChat("Sorry, I am not able to get the weather, please try again later")
#             #
#             #         table_body += "<tr><td>" + day5date + "</td><td>" + day5maxtemp + "</td><td>" + day5mintemp + "</td><td>" + day5avgtemp + "</td><td>" + day5maxwind + "</td><td>" + day5totalprecip + "</td><td>" + day5avghumidity + "</td><td>" + day5condition + "</td><td><img src=\"" + day5icon + "\"/></td><td>" + day5sunrise + "</td><td>" + day5sunset + "</td><td>" + day5moonrise + "</td><td>" + day5moonset + "</td></tr>"
#             #
#             #     if days == six:
#             #
#             #         try:
#             #             #print("2 days")
#             #             day2date = str(d["forecast"]["forecastday"][1]["date"])
#             #             day2maxtemp = str(d["forecast"]["forecastday"][1]["day"]["maxtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][1]["day"]["maxtemp_f"]) + " F"
#             #             day2mintemp = str(d["forecast"]["forecastday"][1]["day"]["mintemp_c"]) + " C / " + str(d["forecast"]["forecastday"][1]["day"]["mintemp_f"]) + " F"
#             #             day2avgtemp = str(d["forecast"]["forecastday"][1]["day"]["avgtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][1]["day"]["avgtemp_f"]) + " F"
#             #             day2maxwind = str(d["forecast"]["forecastday"][1]["day"]["maxwind_mph"]) + " mph / " + str(d["forecast"]["forecastday"][1]["day"]["maxwind_kph"]) + " kph"
#             #             day2totalprecip = str(d["forecast"]["forecastday"][1]["day"]["totalprecip_mm"]) + "mm / " + str(d["forecast"]["forecastday"][1]["day"]["totalprecip_in"]) + "in"
#             #             day2avghumidity = str(d["forecast"]["forecastday"][1]["day"]["avghumidity"])
#             #             day2condition = str(d["forecast"]["forecastday"][1]["day"]["condition"]["text"])
#             #             day2icon = str(d["forecast"]["forecastday"][1]["day"]["condition"]["icon"])
#             #             day2sunrise = str(d["forecast"]["forecastday"][1]["astro"]["sunrise"])
#             #             day2sunset = str(d["forecast"]["forecastday"][1]["astro"]["sunset"])
#             #             day2moonrise = str(d["forecast"]["forecastday"][1]["astro"]["moonrise"])
#             #             day2moonset = str(d["forecast"]["forecastday"][1]["astro"]["moonset"])
#             #         except:
#             #             return messageDetail.ReplyToChat("Sorry, I am not able to get the weather, please try again later")
#             #
#             #         table_body += "<tr><td>" + day2date + "</td><td>" + day2maxtemp + "</td><td>" + day2mintemp + "</td><td>" + day2avgtemp + "</td><td>" + day2maxwind + "</td><td>" + day2totalprecip + "</td><td>" + day2avghumidity + "</td><td>" + day2condition + "</td><td><img src=\"" + day2icon + "\"/></td><td>" + day2sunrise + "</td><td>" + day2sunset + "</td><td>" + day2moonrise + "</td><td>" + day2moonset + "</td></tr>"
#             #
#             #         try:
#             #             #print("3 days")
#             #             day3date = str(d["forecast"]["forecastday"][2]["date"])
#             #             day3maxtemp = str(d["forecast"]["forecastday"][2]["day"]["maxtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][2]["day"]["maxtemp_f"]) + " F"
#             #             day3mintemp = str(d["forecast"]["forecastday"][2]["day"]["mintemp_c"]) + " C / " + str(d["forecast"]["forecastday"][2]["day"]["mintemp_f"]) + " F"
#             #             day3avgtemp = str(d["forecast"]["forecastday"][2]["day"]["avgtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][2]["day"]["avgtemp_f"]) + " F"
#             #             day3maxwind = str(d["forecast"]["forecastday"][2]["day"]["maxwind_mph"]) + " mph / " + str(d["forecast"]["forecastday"][2]["day"]["maxwind_kph"]) + " kph"
#             #             day3totalprecip = str(d["forecast"]["forecastday"][2]["day"]["totalprecip_mm"]) + "mm / " + str(d["forecast"]["forecastday"][2]["day"]["totalprecip_in"]) + "in"
#             #             day3avghumidity = str(d["forecast"]["forecastday"][2]["day"]["avghumidity"])
#             #             day3condition = str(d["forecast"]["forecastday"][2]["day"]["condition"]["text"])
#             #             day3icon = str(d["forecast"]["forecastday"][2]["day"]["condition"]["icon"])
#             #             day3sunrise = str(d["forecast"]["forecastday"][2]["astro"]["sunrise"])
#             #             day3sunset = str(d["forecast"]["forecastday"][2]["astro"]["sunset"])
#             #             day3moonrise = str(d["forecast"]["forecastday"][2]["astro"]["moonrise"])
#             #             day3moonset = str(d["forecast"]["forecastday"][2]["astro"]["moonset"])
#             #         except:
#             #             return messageDetail.ReplyToChat("Sorry, I am not able to get the weather, please try again later")
#             #
#             #         table_body += "<tr><td>" + day3date + "</td><td>" + day3maxtemp + "</td><td>" + day3mintemp + "</td><td>" + day3avgtemp + "</td><td>" + day3maxwind + "</td><td>" + day3totalprecip + "</td><td>" + day3avghumidity + "</td><td>" + day3condition + "</td><td><img src=\"" + day3icon + "\"/></td><td>" + day3sunrise + "</td><td>" + day3sunset + "</td><td>" + day3moonrise + "</td><td>" + day3moonset + "</td></tr>"
#             #
#             #         try:
#             #             #print("4 days")
#             #             day4date = str(d["forecast"]["forecastday"][3]["date"])
#             #             day4maxtemp = str(d["forecast"]["forecastday"][3]["day"]["maxtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][3]["day"]["maxtemp_f"]) + " F"
#             #             day4mintemp = str(d["forecast"]["forecastday"][3]["day"]["mintemp_c"]) + " C / " + str(d["forecast"]["forecastday"][3]["day"]["mintemp_f"]) + " F"
#             #             day4avgtemp = str(d["forecast"]["forecastday"][3]["day"]["avgtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][3]["day"]["avgtemp_f"]) + " F"
#             #             day4maxwind = str(d["forecast"]["forecastday"][3]["day"]["maxwind_mph"]) + " mph / " + str(d["forecast"]["forecastday"][3]["day"]["maxwind_kph"]) + " kph"
#             #             day4totalprecip = str(d["forecast"]["forecastday"][3]["day"]["totalprecip_mm"]) + "mm / " + str(d["forecast"]["forecastday"][3]["day"]["totalprecip_in"]) + "in"
#             #             day4avghumidity = str(d["forecast"]["forecastday"][3]["day"]["avghumidity"])
#             #             day4condition = str(d["forecast"]["forecastday"][3]["day"]["condition"]["text"])
#             #             day4icon = str(d["forecast"]["forecastday"][3]["day"]["condition"]["icon"])
#             #             day4sunrise = str(d["forecast"]["forecastday"][3]["astro"]["sunrise"])
#             #             day4sunset = str(d["forecast"]["forecastday"][3]["astro"]["sunset"])
#             #             day4moonrise = str(d["forecast"]["forecastday"][3]["astro"]["moonrise"])
#             #             day4moonset = str(d["forecast"]["forecastday"][3]["astro"]["moonset"])
#             #         except:
#             #             return messageDetail.ReplyToChat("Sorry, I am not able to get the weather, please try again later")
#             #
#             #         table_body += "<tr><td>" + day4date + "</td><td>" + day4maxtemp + "</td><td>" + day4mintemp + "</td><td>" + day4avgtemp + "</td><td>" + day4maxwind + "</td><td>" + day4totalprecip + "</td><td>" + day4avghumidity + "</td><td>" + day4condition + "</td><td><img src=\"" + day4icon + "\"/></td><td>" + day4sunrise + "</td><td>" + day4sunset + "</td><td>" + day4moonrise + "</td><td>" + day4moonset + "</td></tr>"
#             #
#             #         try:
#             #             #print("5 days")
#             #             day5date = str(d["forecast"]["forecastday"][4]["date"])
#             #             day5maxtemp = str(d["forecast"]["forecastday"][4]["day"]["maxtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][4]["day"]["maxtemp_f"]) + " F"
#             #             day5mintemp = str(d["forecast"]["forecastday"][4]["day"]["mintemp_c"]) + " C / " + str(d["forecast"]["forecastday"][4]["day"]["mintemp_f"]) + " F"
#             #             day5avgtemp = str(d["forecast"]["forecastday"][4]["day"]["avgtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][4]["day"]["avgtemp_f"]) + " F"
#             #             day5maxwind = str(d["forecast"]["forecastday"][4]["day"]["maxwind_mph"]) + " mph / " + str(d["forecast"]["forecastday"][4]["day"]["maxwind_kph"]) + " kph"
#             #             day5totalprecip = str(d["forecast"]["forecastday"][4]["day"]["totalprecip_mm"]) + "mm / " + str(d["forecast"]["forecastday"][4]["day"]["totalprecip_in"]) + "in"
#             #             day5avghumidity = str(d["forecast"]["forecastday"][4]["day"]["avghumidity"])
#             #             day5condition = str(d["forecast"]["forecastday"][4]["day"]["condition"]["text"])
#             #             day5icon = str(d["forecast"]["forecastday"][4]["day"]["condition"]["icon"])
#             #             day5sunrise = str(d["forecast"]["forecastday"][4]["astro"]["sunrise"])
#             #             day5sunset = str(d["forecast"]["forecastday"][4]["astro"]["sunset"])
#             #             day5moonrise = str(d["forecast"]["forecastday"][4]["astro"]["moonrise"])
#             #             day5moonset = str(d["forecast"]["forecastday"][4]["astro"]["moonset"])
#             #         except:
#             #             return messageDetail.ReplyToChat("Sorry, I am not able to get the weather, please try again later")
#             #
#             #         table_body += "<tr><td>" + day5date + "</td><td>" + day5maxtemp + "</td><td>" + day5mintemp + "</td><td>" + day5avgtemp + "</td><td>" + day5maxwind + "</td><td>" + day5totalprecip + "</td><td>" + day5avghumidity + "</td><td>" + day5condition + "</td><td><img src=\"" + day5icon + "\"/></td><td>" + day5sunrise + "</td><td>" + day5sunset + "</td><td>" + day5moonrise + "</td><td>" + day5moonset + "</td></tr>"
#             #
#             #         try:
#             #             #print("6 days")
#             #             day6date = str(d["forecast"]["forecastday"][5]["date"])
#             #             day6maxtemp = str(d["forecast"]["forecastday"][5]["day"]["maxtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][5]["day"]["maxtemp_f"]) + " F"
#             #             day6mintemp = str(d["forecast"]["forecastday"][5]["day"]["mintemp_c"]) + " C / " + str(d["forecast"]["forecastday"][5]["day"]["mintemp_f"]) + " F"
#             #             day6avgtemp = str(d["forecast"]["forecastday"][5]["day"]["avgtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][5]["day"]["avgtemp_f"]) + " F"
#             #             day6maxwind = str(d["forecast"]["forecastday"][5]["day"]["maxwind_mph"]) + " mph / " + str(d["forecast"]["forecastday"][5]["day"]["maxwind_kph"]) + " kph"
#             #             day6totalprecip = str(d["forecast"]["forecastday"][5]["day"]["totalprecip_mm"]) + "mm / " + str(d["forecast"]["forecastday"][5]["day"]["totalprecip_in"]) + "in"
#             #             day6avghumidity = str(d["forecast"]["forecastday"][5]["day"]["avghumidity"])
#             #             day6condition = str(d["forecast"]["forecastday"][5]["day"]["condition"]["text"])
#             #             day6icon = str(d["forecast"]["forecastday"][5]["day"]["condition"]["icon"])
#             #             day6sunrise = str(d["forecast"]["forecastday"][5]["astro"]["sunrise"])
#             #             day6sunset = str(d["forecast"]["forecastday"][5]["astro"]["sunset"])
#             #             day6moonrise = str(d["forecast"]["forecastday"][5]["astro"]["moonrise"])
#             #             day6moonset = str(d["forecast"]["forecastday"][5]["astro"]["moonset"])
#             #         except:
#             #             return messageDetail.ReplyToChat("Sorry, I am not able to get the weather, please try again later")
#             #
#             #         table_body += "<tr><td>" + day6date + "</td><td>" + day6maxtemp + "</td><td>" + day6mintemp + "</td><td>" + day6avgtemp + "</td><td>" + day6maxwind + "</td><td>" + day6totalprecip + "</td><td>" + day6avghumidity + "</td><td>" + day6condition + "</td><td><img src=\"" + day6icon + "\"/></td><td>" + day6sunrise + "</td><td>" + day6sunset + "</td><td>" + day6moonrise + "</td><td>" + day6moonset + "</td></tr>"
#             #
#             #
#             #     if days == seven:
#             #
#             #         try:
#             #             #print("2 days")
#             #             day2date = str(d["forecast"]["forecastday"][1]["date"])
#             #             day2maxtemp = str(d["forecast"]["forecastday"][1]["day"]["maxtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][1]["day"]["maxtemp_f"]) + " F"
#             #             day2mintemp = str(d["forecast"]["forecastday"][1]["day"]["mintemp_c"]) + " C / " + str(d["forecast"]["forecastday"][1]["day"]["mintemp_f"]) + " F"
#             #             day2avgtemp = str(d["forecast"]["forecastday"][1]["day"]["avgtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][1]["day"]["avgtemp_f"]) + " F"
#             #             day2maxwind = str(d["forecast"]["forecastday"][1]["day"]["maxwind_mph"]) + " mph / " + str(d["forecast"]["forecastday"][1]["day"]["maxwind_kph"]) + " kph"
#             #             day2totalprecip = str(d["forecast"]["forecastday"][1]["day"]["totalprecip_mm"]) + "mm / " + str(d["forecast"]["forecastday"][1]["day"]["totalprecip_in"]) + "in"
#             #             day2avghumidity = str(d["forecast"]["forecastday"][1]["day"]["avghumidity"])
#             #             day2condition = str(d["forecast"]["forecastday"][1]["day"]["condition"]["text"])
#             #             day2icon = str(d["forecast"]["forecastday"][1]["day"]["condition"]["icon"])
#             #             day2sunrise = str(d["forecast"]["forecastday"][1]["astro"]["sunrise"])
#             #             day2sunset = str(d["forecast"]["forecastday"][1]["astro"]["sunset"])
#             #             day2moonrise = str(d["forecast"]["forecastday"][1]["astro"]["moonrise"])
#             #             day2moonset = str(d["forecast"]["forecastday"][1]["astro"]["moonset"])
#             #         except:
#             #             return messageDetail.ReplyToChat("Sorry, I am not able to get the weather, please try again later")
#             #
#             #         table_body += "<tr><td>" + day2date + "</td><td>" + day2maxtemp + "</td><td>" + day2mintemp + "</td><td>" + day2avgtemp + "</td><td>" + day2maxwind + "</td><td>" + day2totalprecip + "</td><td>" + day2avghumidity + "</td><td>" + day2condition + "</td><td><img src=\"" + day2icon + "\"/></td><td>" + day2sunrise + "</td><td>" + day2sunset + "</td><td>" + day2moonrise + "</td><td>" + day2moonset + "</td></tr>"
#             #
#             #         try:
#             #             #print("3 days")
#             #             day3date = str(d["forecast"]["forecastday"][2]["date"])
#             #             day3maxtemp = str(d["forecast"]["forecastday"][2]["day"]["maxtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][2]["day"]["maxtemp_f"]) + " F"
#             #             day3mintemp = str(d["forecast"]["forecastday"][2]["day"]["mintemp_c"]) + " C / " + str(d["forecast"]["forecastday"][2]["day"]["mintemp_f"]) + " F"
#             #             day3avgtemp = str(d["forecast"]["forecastday"][2]["day"]["avgtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][2]["day"]["avgtemp_f"]) + " F"
#             #             day3maxwind = str(d["forecast"]["forecastday"][2]["day"]["maxwind_mph"]) + " mph / " + str(d["forecast"]["forecastday"][2]["day"]["maxwind_kph"]) + " kph"
#             #             day3totalprecip = str(d["forecast"]["forecastday"][2]["day"]["totalprecip_mm"]) + "mm / " + str(d["forecast"]["forecastday"][2]["day"]["totalprecip_in"]) + "in"
#             #             day3avghumidity = str(d["forecast"]["forecastday"][2]["day"]["avghumidity"])
#             #             day3condition = str(d["forecast"]["forecastday"][2]["day"]["condition"]["text"])
#             #             day3icon = str(d["forecast"]["forecastday"][2]["day"]["condition"]["icon"])
#             #             day3sunrise = str(d["forecast"]["forecastday"][2]["astro"]["sunrise"])
#             #             day3sunset = str(d["forecast"]["forecastday"][2]["astro"]["sunset"])
#             #             day3moonrise = str(d["forecast"]["forecastday"][2]["astro"]["moonrise"])
#             #             day3moonset = str(d["forecast"]["forecastday"][2]["astro"]["moonset"])
#             #         except:
#             #             return messageDetail.ReplyToChat("Sorry, I am not able to get the weather, please try again later")
#             #
#             #         table_body += "<tr><td>" + day3date + "</td><td>" + day3maxtemp + "</td><td>" + day3mintemp + "</td><td>" + day3avgtemp + "</td><td>" + day3maxwind + "</td><td>" + day3totalprecip + "</td><td>" + day3avghumidity + "</td><td>" + day3condition + "</td><td><img src=\"" + day3icon + "\"/></td><td>" + day3sunrise + "</td><td>" + day3sunset + "</td><td>" + day3moonrise + "</td><td>" + day3moonset + "</td></tr>"
#             #
#             #         try:
#             #             #print("4 days")
#             #             day4date = str(d["forecast"]["forecastday"][3]["date"])
#             #             day4maxtemp = str(d["forecast"]["forecastday"][3]["day"]["maxtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][3]["day"]["maxtemp_f"]) + " F"
#             #             day4mintemp = str(d["forecast"]["forecastday"][3]["day"]["mintemp_c"]) + " C / " + str(d["forecast"]["forecastday"][3]["day"]["mintemp_f"]) + " F"
#             #             day4avgtemp = str(d["forecast"]["forecastday"][3]["day"]["avgtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][3]["day"]["avgtemp_f"]) + " F"
#             #             day4maxwind = str(d["forecast"]["forecastday"][3]["day"]["maxwind_mph"]) + " mph / " + str(d["forecast"]["forecastday"][3]["day"]["maxwind_kph"]) + " kph"
#             #             day4totalprecip = str(d["forecast"]["forecastday"][3]["day"]["totalprecip_mm"]) + "mm / " + str(d["forecast"]["forecastday"][3]["day"]["totalprecip_in"]) + "in"
#             #             day4avghumidity = str(d["forecast"]["forecastday"][3]["day"]["avghumidity"])
#             #             day4condition = str(d["forecast"]["forecastday"][3]["day"]["condition"]["text"])
#             #             day4icon = str(d["forecast"]["forecastday"][3]["day"]["condition"]["icon"])
#             #             day4sunrise = str(d["forecast"]["forecastday"][3]["astro"]["sunrise"])
#             #             day4sunset = str(d["forecast"]["forecastday"][3]["astro"]["sunset"])
#             #             day4moonrise = str(d["forecast"]["forecastday"][3]["astro"]["moonrise"])
#             #             day4moonset = str(d["forecast"]["forecastday"][3]["astro"]["moonset"])
#             #         except:
#             #             return messageDetail.ReplyToChat("Sorry, I am not able to get the weather, please try again later")
#             #
#             #         table_body += "<tr><td>" + day4date + "</td><td>" + day4maxtemp + "</td><td>" + day4mintemp + "</td><td>" + day4avgtemp + "</td><td>" + day4maxwind + "</td><td>" + day4totalprecip + "</td><td>" + day4avghumidity + "</td><td>" + day4condition + "</td><td><img src=\"" + day4icon + "\"/></td><td>" + day4sunrise + "</td><td>" + day4sunset + "</td><td>" + day4moonrise + "</td><td>" + day4moonset + "</td></tr>"
#             #
#             #         try:
#             #             #print("5 days")
#             #             day5date = str(d["forecast"]["forecastday"][4]["date"])
#             #             day5maxtemp = str(d["forecast"]["forecastday"][4]["day"]["maxtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][4]["day"]["maxtemp_f"]) + " F"
#             #             day5mintemp = str(d["forecast"]["forecastday"][4]["day"]["mintemp_c"]) + " C / " + str(d["forecast"]["forecastday"][4]["day"]["mintemp_f"]) + " F"
#             #             day5avgtemp = str(d["forecast"]["forecastday"][4]["day"]["avgtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][4]["day"]["avgtemp_f"]) + " F"
#             #             day5maxwind = str(d["forecast"]["forecastday"][4]["day"]["maxwind_mph"]) + " mph / " + str(d["forecast"]["forecastday"][4]["day"]["maxwind_kph"]) + " kph"
#             #             day5totalprecip = str(d["forecast"]["forecastday"][4]["day"]["totalprecip_mm"]) + "mm / " + str(d["forecast"]["forecastday"][4]["day"]["totalprecip_in"]) + "in"
#             #             day5avghumidity = str(d["forecast"]["forecastday"][4]["day"]["avghumidity"])
#             #             day5condition = str(d["forecast"]["forecastday"][4]["day"]["condition"]["text"])
#             #             day5icon = str(d["forecast"]["forecastday"][4]["day"]["condition"]["icon"])
#             #             day5sunrise = str(d["forecast"]["forecastday"][4]["astro"]["sunrise"])
#             #             day5sunset = str(d["forecast"]["forecastday"][4]["astro"]["sunset"])
#             #             day5moonrise = str(d["forecast"]["forecastday"][4]["astro"]["moonrise"])
#             #             day5moonset = str(d["forecast"]["forecastday"][4]["astro"]["moonset"])
#             #         except:
#             #             return messageDetail.ReplyToChat("Sorry, I am not able to get the weather, please try again later")
#             #
#             #         table_body += "<tr><td>" + day5date + "</td><td>" + day5maxtemp + "</td><td>" + day5mintemp + "</td><td>" + day5avgtemp + "</td><td>" + day5maxwind + "</td><td>" + day5totalprecip + "</td><td>" + day5avghumidity + "</td><td>" + day5condition + "</td><td><img src=\"" + day5icon + "\"/></td><td>" + day5sunrise + "</td><td>" + day5sunset + "</td><td>" + day5moonrise + "</td><td>" + day5moonset + "</td></tr>"
#             #
#             #         try:
#             #             #print("6 days")
#             #             day6date = str(d["forecast"]["forecastday"][5]["date"])
#             #             day6maxtemp = str(d["forecast"]["forecastday"][5]["day"]["maxtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][5]["day"]["maxtemp_f"]) + " F"
#             #             day6mintemp = str(d["forecast"]["forecastday"][5]["day"]["mintemp_c"]) + " C / " + str(d["forecast"]["forecastday"][5]["day"]["mintemp_f"]) + " F"
#             #             day6avgtemp = str(d["forecast"]["forecastday"][5]["day"]["avgtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][5]["day"]["avgtemp_f"]) + " F"
#             #             day6maxwind = str(d["forecast"]["forecastday"][5]["day"]["maxwind_mph"]) + " mph / " + str(d["forecast"]["forecastday"][5]["day"]["maxwind_kph"]) + " kph"
#             #             day6totalprecip = str(d["forecast"]["forecastday"][5]["day"]["totalprecip_mm"]) + "mm / " + str(d["forecast"]["forecastday"][5]["day"]["totalprecip_in"]) + "in"
#             #             day6avghumidity = str(d["forecast"]["forecastday"][5]["day"]["avghumidity"])
#             #             day6condition = str(d["forecast"]["forecastday"][5]["day"]["condition"]["text"])
#             #             day6icon = str(d["forecast"]["forecastday"][5]["day"]["condition"]["icon"])
#             #             day6sunrise = str(d["forecast"]["forecastday"][5]["astro"]["sunrise"])
#             #             day6sunset = str(d["forecast"]["forecastday"][5]["astro"]["sunset"])
#             #             day6moonrise = str(d["forecast"]["forecastday"][5]["astro"]["moonrise"])
#             #             day6moonset = str(d["forecast"]["forecastday"][5]["astro"]["moonset"])
#             #         except:
#             #             return messageDetail.ReplyToChat("Sorry, I am not able to get the weather, please try again later")
#             #
#             #         table_body += "<tr><td>" + day6date + "</td><td>" + day6maxtemp + "</td><td>" + day6mintemp + "</td><td>" + day6avgtemp + "</td><td>" + day6maxwind + "</td><td>" + day6totalprecip + "</td><td>" + day6avghumidity + "</td><td>" + day6condition + "</td><td><img src=\"" + day6icon + "\"/></td><td>" + day6sunrise + "</td><td>" + day6sunset + "</td><td>" + day6moonrise + "</td><td>" + day6moonset + "</td></tr>"
#             #
#             #         try:
#             #             #print("7 days")
#             #             day7date = str(d["forecast"]["forecastday"][6]["date"])
#             #             day7maxtemp = str(d["forecast"]["forecastday"][6]["day"]["maxtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][6]["day"]["maxtemp_f"]) + " F"
#             #             day7mintemp = str(d["forecast"]["forecastday"][6]["day"]["mintemp_c"]) + " C / " + str(d["forecast"]["forecastday"][6]["day"]["mintemp_f"]) + " F"
#             #             day7avgtemp = str(d["forecast"]["forecastday"][6]["day"]["avgtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][6]["day"]["avgtemp_f"]) + " F"
#             #             day7maxwind = str(d["forecast"]["forecastday"][6]["day"]["maxwind_mph"]) + " mph / " + str(d["forecast"]["forecastday"][6]["day"]["maxwind_kph"]) + " kph"
#             #             day7totalprecip = str(d["forecast"]["forecastday"][6]["day"]["totalprecip_mm"]) + "mm / " + str(d["forecast"]["forecastday"][6]["day"]["totalprecip_in"]) + "in"
#             #             day7avghumidity = str(d["forecast"]["forecastday"][6]["day"]["avghumidity"])
#             #             day7condition = str(d["forecast"]["forecastday"][6]["day"]["condition"]["text"])
#             #             day7icon = str(d["forecast"]["forecastday"][6]["day"]["condition"]["icon"])
#             #             day7sunrise = str(d["forecast"]["forecastday"][6]["astro"]["sunrise"])
#             #             day7sunset = str(d["forecast"]["forecastday"][6]["astro"]["sunset"])
#             #             day7moonrise = str(d["forecast"]["forecastday"][6]["astro"]["moonrise"])
#             #             day7moonset = str(d["forecast"]["forecastday"][6]["astro"]["moonset"])
#             #         except:
#             #             return messageDetail.ReplyToChat("Sorry, I am not able to get the weather, please try again later")
#             #
#             #         table_body += "<tr><td>" + day7date + "</td><td>" + day7maxtemp + "</td><td>" + day7mintemp + "</td><td>" + day7avgtemp + "</td><td>" + day7maxwind + "</td><td>" + day7totalprecip + "</td><td>" + day7avghumidity + "</td><td>" + day7condition + "</td><td><img src=\"" + day7icon + "\"/></td><td>" + day7sunrise + "</td><td>" + day7sunset + "</td><td>" + day7moonrise + "</td><td>" + day7moonset + "</td></tr>"
#             #
#             #     table_body += "</tbody></table>"
#             #
#             #     #return messageDetail.ReplyToChatV2_noBotLog("<card iconSrc=\"https://thumb.ibb.co/csXBgU/Symphony2018_App_Icon_Mobile.png\" accent=\"tempo-bg-color--blue\"><header>The current condition in " + LocationName + ", " + Region + ", " + Country + " as of " + LastUpdated + " is " + Condition + ", <img src=\"" + CurrentURL + "\"/> (" + TempC + " C / " + TempF + " F)<br/></header><body>" + table_body + "</body></card>")
#             #     return messageDetail.ReplyToChatV2_noBotLog("<card iconSrc=\"\" accent=\"tempo-bg-color--blue\"><header>The current condition in " + LocationName + ", " + Region + ", " + Country + " as of " + LastUpdated + " is " + Condition + ", <img src=\"" + CurrentURL + "\"/> (" + TempC + " C / " + TempF + " F)<br/></header><body>" + table_body + "</body></card>")
#
#     # except:
#     #     try:
#     #         botlog.LogSymphonyInfo("Inside Second call Weather")
#     #         # if callerCheck in AccessFile:
#     #         if companyName in _configDef['AuthCompany']['PodList']:
#     #
#     #             botlog.LogSymphonyInfo("Bot Call: Weather")
#     #
#     #             message = (messageDetail.Command.MessageText)
#     #             weatherCatcher = message.split()
#     #             location = ""
#     #             days = ""
#     #             rawtwo = 2
#     #             two = str(rawtwo)
#     #             rawthree = 3
#     #             three = str(rawthree)
#     #             rawfour = 4
#     #             four = str(rawfour)
#     #             rawfive = 5
#     #             five = str(rawfive)
#     #             rawsix = 6
#     #             six = str(rawsix)
#     #             rawseven = 7
#     #             seven = str(rawseven)
#     #
#     #             catchLength = len(weatherCatcher)
#     #             #print("Lenght is: " + (str(catchLength)))
#     #
#     #             try:
#     #                 emptyLocation = catchLength == 0 or weatherCatcher[0] == ""
#     #                 if emptyLocation:
#     #                     return messageDetail.ReplyToChat("Please enter a location, if it is more than one word, e.g New York, please use underscore as in New_York")
#     #                 else:
#     #                     location = weatherCatcher[0]
#     #                     #print("Location: " + location)
#     #             except:
#     #                 messageDetail.ReplyToChat("Loading the weather forecast")
#     #
#     #             try:
#     #                 emptyDays = weatherCatcher[1] == ""
#     #                 if emptyDays:
#     #                     days = 0
#     #                 else:
#     #                     days = weatherCatcher[1]
#     #                     messageDetail.ReplyToChatV2("Forecasting weather for <b>" + days + "</b> days in <b>" + location + "</b>")
#     #                     #print("Days: " + days)
#     #             except:
#     #                 messageDetail.ReplyToChatV2("Forecasting weather for today in <b>" + location + "</b>")
#     #
#     #
#     #             conn = http.client.HTTPSConnection("api.apixu.com")
#     #             headers = {
#     #                 'cache-control': "no-cache",
#     #             }
#     #             conn.request("GET", "/v1/forecast.json?key=" + _configDef['weather']['API_Key'] + "&q=" + location + "&days=" + days + "", headers=headers)
#     #             res = conn.getresponse()
#     #             data = res.read()
#     #             d_raw = remove_emoji(data)
#     #             data_new = d_raw.replace("","").replace("Å","ō")
#     #             # print(data_new)
#     #             # request_raw = data.decode('utf-8')
#     #             data = json.dumps(data_new, indent=2)
#     #             # data = json.dumps(request_raw, indent=2)
#     #             data_dict = ast.literal_eval(data)
#     #             d = json.loads(data_dict)
#     #             # d = data
#     #             # print(str(d))
#     #
#     #             # Checking for location validation
#     #             notmatchingLocation = "{'error': {'code': 1006, 'message': 'No matching location found.'}}"
#     #             #tempWeather = str(data.decode("utf-8")).replace("\"", "")
#     #             tempWeather = str(d).replace("\'", "")
#     #             #print("tempWeather: " + str(tempWeather))
#     #
#     #             if str(d).startswith(notmatchingLocation):
#     #                 return messageDetail.ReplyToChat("The location entered is not valid, please try again.")
#     #             else:
#     #
#     #                 # try:
#     #                 # # Main weather info - to display regardless of days selected
#     #                 weatherRaw = tempWeather.split(":")
#     #                 LocationName = str(d["location"]["name"])
#     #                 Region = str(d["location"]["region"])
#     #                 Country = str(d["location"]["country"])
#     #                 LastUpdated = str(d["current"]["last_updated"])
#     #                 TempC = str(d["current"]["temp_c"])
#     #                 TempF = str(d["current"]["temp_f"])
#     #                 Condition = str(d["current"]["condition"]["text"])
#     #                 CurrentURL = str(d["current"]["condition"]["icon"])
#     #
#     #                 day1date = str(d["forecast"]["forecastday"][0]["date"])
#     #                 day1maxtemp = str(d["forecast"]["forecastday"][0]["day"]["maxtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][0]["day"]["maxtemp_f"]) + " F"
#     #                 day1mintemp = str(d["forecast"]["forecastday"][0]["day"]["mintemp_c"]) + " C / " + str(d["forecast"]["forecastday"][0]["day"]["mintemp_f"]) + " F"
#     #                 day1avgtemp = str(d["forecast"]["forecastday"][0]["day"]["avgtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][0]["day"]["avgtemp_f"]) + " F"
#     #                 day1maxwind = str(d["forecast"]["forecastday"][0]["day"]["maxwind_mph"]) + " mph / " + str(d["forecast"]["forecastday"][0]["day"]["maxwind_kph"]) + " kph"
#     #                 day1totalprecip = str(d["forecast"]["forecastday"][0]["day"]["totalprecip_mm"]) + "mm / " + str(d["forecast"]["forecastday"][0]["day"]["totalprecip_in"]) + "in"
#     #                 day1avghumidity = str(d["forecast"]["forecastday"][0]["day"]["avghumidity"])
#     #                 day1condition = str(d["forecast"]["forecastday"][0]["day"]["condition"]["text"])
#     #                 day1icon = str(d["forecast"]["forecastday"][0]["day"]["condition"]["icon"])
#     #                 day1sunrise = str(d["forecast"]["forecastday"][0]["astro"]["sunrise"])
#     #                 day1sunset = str(d["forecast"]["forecastday"][0]["astro"]["sunset"])
#     #                 day1moonrise = str(d["forecast"]["forecastday"][0]["astro"]["moonrise"])
#     #                 day1moonset = str(d["forecast"]["forecastday"][0]["astro"]["moonset"])
#     #                 # except:
#     #                 #     return messageDetail.ReplyToChat("Sorry, I am not able to get the weather, please try again later")
#     #
#     #                 table_body = "<table style='table-layout:auto;width:100%'>" \
#     #                              "<thead>" \
#     #                              "<tr class=\"tempo-text-color--white tempo-bg-color--black\">" \
#     #                              "<td>Date</td>" \
#     #                              "<td>Max Temp</td>" \
#     #                              "<td>Min Temp</td>" \
#     #                              "<td>Avg Temp</td>" \
#     #                              "<td>Max Wind</td>" \
#     #                              "<td>Tot Precipitation</td>" \
#     #                              "<td>Avg Humidity</td>" \
#     #                              "<td>Condition</td>" \
#     #                              "<td></td>" \
#     #                              "<td>Sunrise</td>" \
#     #                              "<td>Sunset</td>" \
#     #                              "<td>Moonrise</td>" \
#     #                              "<td>Moonset</td>" \
#     #                              "</tr>" \
#     #                              "</thead><tbody>"
#     #
#     #                 table_body += "<tr>" \
#     #                               "<td>" + day1date + "</td>" \
#     #                               "<td>" + day1maxtemp + "</td>" \
#     #                               "<td>" + day1mintemp + "</td>" \
#     #                               "<td>" + day1avgtemp + "</td>" \
#     #                               "<td>" + day1maxwind + "</td>" \
#     #                               "<td>" + day1totalprecip + "</td>" \
#     #                               "<td>" + day1avghumidity + "</td>" \
#     #                               "<td>" + day1condition + "</td>" \
#     #                               "<td><img src=\"" + day1icon + "\"/></td>" \
#     #                               "<td>" + day1sunrise + "</td>" \
#     #                               "<td>" + day1sunset + "</td>" \
#     #                               "<td>" + day1moonrise + "</td>" \
#     #                               "<td>" + day1moonset + "</td>" \
#     #                               "</tr>"
#     #
#     #                 if days == two:
#     #
#     #                     try:
#     #                         #print("2 days")
#     #                         day2date = str(d["forecast"]["forecastday"][1]["date"])
#     #                         day2maxtemp = str(d["forecast"]["forecastday"][1]["day"]["maxtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][1]["day"]["maxtemp_f"]) + " F"
#     #                         day2mintemp = str(d["forecast"]["forecastday"][1]["day"]["mintemp_c"]) + " C / " + str(d["forecast"]["forecastday"][1]["day"]["mintemp_f"]) + " F"
#     #                         day2avgtemp = str(d["forecast"]["forecastday"][1]["day"]["avgtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][1]["day"]["avgtemp_f"]) + " F"
#     #                         day2maxwind = str(d["forecast"]["forecastday"][1]["day"]["maxwind_mph"]) + " mph / " + str(d["forecast"]["forecastday"][1]["day"]["maxwind_kph"]) + " kph"
#     #                         day2totalprecip = str(d["forecast"]["forecastday"][1]["day"]["totalprecip_mm"]) + "mm / " + str(d["forecast"]["forecastday"][1]["day"]["totalprecip_in"]) + "in"
#     #                         day2avghumidity = str(d["forecast"]["forecastday"][1]["day"]["avghumidity"])
#     #                         day2condition = str(d["forecast"]["forecastday"][1]["day"]["condition"]["text"])
#     #                         day2icon = str(d["forecast"]["forecastday"][1]["day"]["condition"]["icon"])
#     #                         day2sunrise = str(d["forecast"]["forecastday"][1]["astro"]["sunrise"])
#     #                         day2sunset = str(d["forecast"]["forecastday"][1]["astro"]["sunset"])
#     #                         day2moonrise = str(d["forecast"]["forecastday"][1]["astro"]["moonrise"])
#     #                         day2moonset = str(d["forecast"]["forecastday"][1]["astro"]["moonset"])
#     #                     except:
#     #                         return messageDetail.ReplyToChat("Sorry, I am not able to get the weather, please try again later")
#     #
#     #                     table_body += "<tr><td>" + day2date + "</td><td>" + day2maxtemp + "</td><td>" + day2mintemp + "</td><td>" + day2avgtemp + "</td><td>" + day2maxwind + "</td><td>" + day2totalprecip + "</td><td>" + day2avghumidity + "</td><td>" + day2condition + "</td><td><img src=\"" + day2icon + "\"/></td><td>" + day2sunrise + "</td><td>" + day2sunset + "</td><td>" + day2moonrise + "</td><td>" + day2moonset + "</td></tr>"
#     #
#     #                 if days == three:
#     #
#     #                     try:
#     #                         #print("2 days")
#     #                         day2date = str(d["forecast"]["forecastday"][1]["date"])
#     #                         day2maxtemp = str(d["forecast"]["forecastday"][1]["day"]["maxtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][1]["day"]["maxtemp_f"]) + " F"
#     #                         day2mintemp = str(d["forecast"]["forecastday"][1]["day"]["mintemp_c"]) + " C / " + str(d["forecast"]["forecastday"][1]["day"]["mintemp_f"]) + " F"
#     #                         day2avgtemp = str(d["forecast"]["forecastday"][1]["day"]["avgtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][1]["day"]["avgtemp_f"]) + " F"
#     #                         day2maxwind = str(d["forecast"]["forecastday"][1]["day"]["maxwind_mph"]) + " mph / " + str(d["forecast"]["forecastday"][1]["day"]["maxwind_kph"]) + " kph"
#     #                         day2totalprecip = str(d["forecast"]["forecastday"][1]["day"]["totalprecip_mm"]) + "mm / " + str(d["forecast"]["forecastday"][1]["day"]["totalprecip_in"]) + "in"
#     #                         day2avghumidity = str(d["forecast"]["forecastday"][1]["day"]["avghumidity"])
#     #                         day2condition = str(d["forecast"]["forecastday"][1]["day"]["condition"]["text"])
#     #                         day2icon = str(d["forecast"]["forecastday"][1]["day"]["condition"]["icon"])
#     #                         day2sunrise = str(d["forecast"]["forecastday"][1]["astro"]["sunrise"])
#     #                         day2sunset = str(d["forecast"]["forecastday"][1]["astro"]["sunset"])
#     #                         day2moonrise = str(d["forecast"]["forecastday"][1]["astro"]["moonrise"])
#     #                         day2moonset = str(d["forecast"]["forecastday"][1]["astro"]["moonset"])
#     #                     except:
#     #                         return messageDetail.ReplyToChat("Sorry, I am not able to get the weather, please try again later")
#     #
#     #                     table_body += "<tr><td>" + day2date + "</td><td>" + day2maxtemp + "</td><td>" + day2mintemp + "</td><td>" + day2avgtemp + "</td><td>" + day2maxwind + "</td><td>" + day2totalprecip + "</td><td>" + day2avghumidity + "</td><td>" + day2condition + "</td><td><img src=\"" + day2icon + "\"/></td><td>" + day2sunrise + "</td><td>" + day2sunset + "</td><td>" + day2moonrise + "</td><td>" + day2moonset + "</td></tr>"
#     #
#     #                     try:
#     #                         #print("3 days")
#     #                         day3date = str(d["forecast"]["forecastday"][2]["date"])
#     #                         day3maxtemp = str(d["forecast"]["forecastday"][2]["day"]["maxtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][2]["day"]["maxtemp_f"]) + " F"
#     #                         day3mintemp = str(d["forecast"]["forecastday"][2]["day"]["mintemp_c"]) + " C / " + str(d["forecast"]["forecastday"][2]["day"]["mintemp_f"]) + " F"
#     #                         day3avgtemp = str(d["forecast"]["forecastday"][2]["day"]["avgtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][2]["day"]["avgtemp_f"]) + " F"
#     #                         day3maxwind = str(d["forecast"]["forecastday"][2]["day"]["maxwind_mph"]) + " mph / " + str(d["forecast"]["forecastday"][2]["day"]["maxwind_kph"]) + " kph"
#     #                         day3totalprecip = str(d["forecast"]["forecastday"][2]["day"]["totalprecip_mm"]) + "mm / " + str(d["forecast"]["forecastday"][2]["day"]["totalprecip_in"]) + "in"
#     #                         day3avghumidity = str(d["forecast"]["forecastday"][2]["day"]["avghumidity"])
#     #                         day3condition = str(d["forecast"]["forecastday"][2]["day"]["condition"]["text"])
#     #                         day3icon = str(d["forecast"]["forecastday"][2]["day"]["condition"]["icon"])
#     #                         day3sunrise = str(d["forecast"]["forecastday"][2]["astro"]["sunrise"])
#     #                         day3sunset = str(d["forecast"]["forecastday"][2]["astro"]["sunset"])
#     #                         day3moonrise = str(d["forecast"]["forecastday"][2]["astro"]["moonrise"])
#     #                         day3moonset = str(d["forecast"]["forecastday"][2]["astro"]["moonset"])
#     #                     except:
#     #                         return messageDetail.ReplyToChat("Sorry, I am not able to get the weather, please try again later")
#     #
#     #                     table_body += "<tr><td>" + day3date + "</td><td>" + day3maxtemp + "</td><td>" + day3mintemp + "</td><td>" + day3avgtemp + "</td><td>" + day3maxwind + "</td><td>" + day3totalprecip + "</td><td>" + day3avghumidity + "</td><td>" + day3condition + "</td><td><img src=\"" + day3icon + "\"/></td><td>" + day3sunrise + "</td><td>" + day3sunset + "</td><td>" + day3moonrise + "</td><td>" + day3moonset + "</td></tr>"
#     #
#     #
#     #                 if days == four:
#     #
#     #                     try:
#     #                         #print("2 days")
#     #                         day2date = str(d["forecast"]["forecastday"][1]["date"])
#     #                         day2maxtemp = str(d["forecast"]["forecastday"][1]["day"]["maxtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][1]["day"]["maxtemp_f"]) + " F"
#     #                         day2mintemp = str(d["forecast"]["forecastday"][1]["day"]["mintemp_c"]) + " C / " + str(d["forecast"]["forecastday"][1]["day"]["mintemp_f"]) + " F"
#     #                         day2avgtemp = str(d["forecast"]["forecastday"][1]["day"]["avgtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][1]["day"]["avgtemp_f"]) + " F"
#     #                         day2maxwind = str(d["forecast"]["forecastday"][1]["day"]["maxwind_mph"]) + " mph / " + str(d["forecast"]["forecastday"][1]["day"]["maxwind_kph"]) + " kph"
#     #                         day2totalprecip = str(d["forecast"]["forecastday"][1]["day"]["totalprecip_mm"]) + "mm / " + str(d["forecast"]["forecastday"][1]["day"]["totalprecip_in"]) + "in"
#     #                         day2avghumidity = str(d["forecast"]["forecastday"][1]["day"]["avghumidity"])
#     #                         day2condition = str(d["forecast"]["forecastday"][1]["day"]["condition"]["text"])
#     #                         day2icon = str(d["forecast"]["forecastday"][1]["day"]["condition"]["icon"])
#     #                         day2sunrise = str(d["forecast"]["forecastday"][1]["astro"]["sunrise"])
#     #                         day2sunset = str(d["forecast"]["forecastday"][1]["astro"]["sunset"])
#     #                         day2moonrise = str(d["forecast"]["forecastday"][1]["astro"]["moonrise"])
#     #                         day2moonset = str(d["forecast"]["forecastday"][1]["astro"]["moonset"])
#     #                     except:
#     #                         return messageDetail.ReplyToChat("Sorry, I am not able to get the weather, please try again later")
#     #
#     #                     table_body += "<tr><td>" + day2date + "</td><td>" + day2maxtemp + "</td><td>" + day2mintemp + "</td><td>" + day2avgtemp + "</td><td>" + day2maxwind + "</td><td>" + day2totalprecip + "</td><td>" + day2avghumidity + "</td><td>" + day2condition + "</td><td><img src=\"" + day2icon + "\"/></td><td>" + day2sunrise + "</td><td>" + day2sunset + "</td><td>" + day2moonrise + "</td><td>" + day2moonset + "</td></tr>"
#     #
#     #                     try:
#     #                         #print("3 days")
#     #                         day3date = str(d["forecast"]["forecastday"][2]["date"])
#     #                         day3maxtemp = str(d["forecast"]["forecastday"][2]["day"]["maxtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][2]["day"]["maxtemp_f"]) + " F"
#     #                         day3mintemp = str(d["forecast"]["forecastday"][2]["day"]["mintemp_c"]) + " C / " + str(d["forecast"]["forecastday"][2]["day"]["mintemp_f"]) + " F"
#     #                         day3avgtemp = str(d["forecast"]["forecastday"][2]["day"]["avgtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][2]["day"]["avgtemp_f"]) + " F"
#     #                         day3maxwind = str(d["forecast"]["forecastday"][2]["day"]["maxwind_mph"]) + " mph / " + str(d["forecast"]["forecastday"][2]["day"]["maxwind_kph"]) + " kph"
#     #                         day3totalprecip = str(d["forecast"]["forecastday"][2]["day"]["totalprecip_mm"]) + "mm / " + str(d["forecast"]["forecastday"][2]["day"]["totalprecip_in"]) + "in"
#     #                         day3avghumidity = str(d["forecast"]["forecastday"][2]["day"]["avghumidity"])
#     #                         day3condition = str(d["forecast"]["forecastday"][2]["day"]["condition"]["text"])
#     #                         day3icon = str(d["forecast"]["forecastday"][2]["day"]["condition"]["icon"])
#     #                         day3sunrise = str(d["forecast"]["forecastday"][2]["astro"]["sunrise"])
#     #                         day3sunset = str(d["forecast"]["forecastday"][2]["astro"]["sunset"])
#     #                         day3moonrise = str(d["forecast"]["forecastday"][2]["astro"]["moonrise"])
#     #                         day3moonset = str(d["forecast"]["forecastday"][2]["astro"]["moonset"])
#     #                     except:
#     #                         return messageDetail.ReplyToChat("Sorry, I am not able to get the weather, please try again later")
#     #
#     #                     table_body += "<tr><td>" + day3date + "</td><td>" + day3maxtemp + "</td><td>" + day3mintemp + "</td><td>" + day3avgtemp + "</td><td>" + day3maxwind + "</td><td>" + day3totalprecip + "</td><td>" + day3avghumidity + "</td><td>" + day3condition + "</td><td><img src=\"" + day3icon + "\"/></td><td>" + day3sunrise + "</td><td>" + day3sunset + "</td><td>" + day3moonrise + "</td><td>" + day3moonset + "</td></tr>"
#     #
#     #                     try:
#     #                         #print("4 days")
#     #                         day4date = str(d["forecast"]["forecastday"][3]["date"])
#     #                         day4maxtemp = str(d["forecast"]["forecastday"][3]["day"]["maxtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][3]["day"]["maxtemp_f"]) + " F"
#     #                         day4mintemp = str(d["forecast"]["forecastday"][3]["day"]["mintemp_c"]) + " C / " + str(d["forecast"]["forecastday"][3]["day"]["mintemp_f"]) + " F"
#     #                         day4avgtemp = str(d["forecast"]["forecastday"][3]["day"]["avgtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][3]["day"]["avgtemp_f"]) + " F"
#     #                         day4maxwind = str(d["forecast"]["forecastday"][3]["day"]["maxwind_mph"]) + " mph / " + str(d["forecast"]["forecastday"][3]["day"]["maxwind_kph"]) + " kph"
#     #                         day4totalprecip = str(d["forecast"]["forecastday"][3]["day"]["totalprecip_mm"]) + "mm / " + str(d["forecast"]["forecastday"][3]["day"]["totalprecip_in"]) + "in"
#     #                         day4avghumidity = str(d["forecast"]["forecastday"][3]["day"]["avghumidity"])
#     #                         day4condition = str(d["forecast"]["forecastday"][3]["day"]["condition"]["text"])
#     #                         day4icon = str(d["forecast"]["forecastday"][3]["day"]["condition"]["icon"])
#     #                         day4sunrise = str(d["forecast"]["forecastday"][3]["astro"]["sunrise"])
#     #                         day4sunset = str(d["forecast"]["forecastday"][3]["astro"]["sunset"])
#     #                         day4moonrise = str(d["forecast"]["forecastday"][3]["astro"]["moonrise"])
#     #                         day4moonset = str(d["forecast"]["forecastday"][3]["astro"]["moonset"])
#     #                     except:
#     #                         return messageDetail.ReplyToChat("Sorry, I am not able to get the weather, please try again later")
#     #
#     #                     table_body += "<tr><td>" + day4date + "</td><td>" + day4maxtemp + "</td><td>" + day4mintemp + "</td><td>" + day4avgtemp + "</td><td>" + day4maxwind + "</td><td>" + day4totalprecip + "</td><td>" + day4avghumidity + "</td><td>" + day4condition + "</td><td><img src=\"" + day4icon + "\"/></td><td>" + day4sunrise + "</td><td>" + day4sunset + "</td><td>" + day4moonrise + "</td><td>" + day4moonset + "</td></tr>"
#     #
#     #                 if days == five:
#     #                     try:
#     #                         #print("2 days")
#     #                         day2date = str(d["forecast"]["forecastday"][1]["date"])
#     #                         day2maxtemp = str(d["forecast"]["forecastday"][1]["day"]["maxtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][1]["day"]["maxtemp_f"]) + " F"
#     #                         day2mintemp = str(d["forecast"]["forecastday"][1]["day"]["mintemp_c"]) + " C / " + str(d["forecast"]["forecastday"][1]["day"]["mintemp_f"]) + " F"
#     #                         day2avgtemp = str(d["forecast"]["forecastday"][1]["day"]["avgtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][1]["day"]["avgtemp_f"]) + " F"
#     #                         day2maxwind = str(d["forecast"]["forecastday"][1]["day"]["maxwind_mph"]) + " mph / " + str(d["forecast"]["forecastday"][1]["day"]["maxwind_kph"]) + " kph"
#     #                         day2totalprecip = str(d["forecast"]["forecastday"][1]["day"]["totalprecip_mm"]) + "mm / " + str(d["forecast"]["forecastday"][1]["day"]["totalprecip_in"]) + "in"
#     #                         day2avghumidity = str(d["forecast"]["forecastday"][1]["day"]["avghumidity"])
#     #                         day2condition = str(d["forecast"]["forecastday"][1]["day"]["condition"]["text"])
#     #                         day2icon = str(d["forecast"]["forecastday"][1]["day"]["condition"]["icon"])
#     #                         day2sunrise = str(d["forecast"]["forecastday"][1]["astro"]["sunrise"])
#     #                         day2sunset = str(d["forecast"]["forecastday"][1]["astro"]["sunset"])
#     #                         day2moonrise = str(d["forecast"]["forecastday"][1]["astro"]["moonrise"])
#     #                         day2moonset = str(d["forecast"]["forecastday"][1]["astro"]["moonset"])
#     #                     except:
#     #                         return messageDetail.ReplyToChat("Sorry, I am not able to get the weather, please try again later")
#     #
#     #                     table_body += "<tr><td>" + day2date + "</td><td>" + day2maxtemp + "</td><td>" + day2mintemp + "</td><td>" + day2avgtemp + "</td><td>" + day2maxwind + "</td><td>" + day2totalprecip + "</td><td>" + day2avghumidity + "</td><td>" + day2condition + "</td><td><img src=\"" + day2icon + "\"/></td><td>" + day2sunrise + "</td><td>" + day2sunset + "</td><td>" + day2moonrise + "</td><td>" + day2moonset + "</td></tr>"
#     #
#     #                     try:
#     #                         #print("3 days")
#     #                         day3date = str(d["forecast"]["forecastday"][2]["date"])
#     #                         day3maxtemp = str(d["forecast"]["forecastday"][2]["day"]["maxtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][2]["day"]["maxtemp_f"]) + " F"
#     #                         day3mintemp = str(d["forecast"]["forecastday"][2]["day"]["mintemp_c"]) + " C / " + str(d["forecast"]["forecastday"][2]["day"]["mintemp_f"]) + " F"
#     #                         day3avgtemp = str(d["forecast"]["forecastday"][2]["day"]["avgtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][2]["day"]["avgtemp_f"]) + " F"
#     #                         day3maxwind = str(d["forecast"]["forecastday"][2]["day"]["maxwind_mph"]) + " mph / " + str(d["forecast"]["forecastday"][2]["day"]["maxwind_kph"]) + " kph"
#     #                         day3totalprecip = str(d["forecast"]["forecastday"][2]["day"]["totalprecip_mm"]) + "mm / " + str(d["forecast"]["forecastday"][2]["day"]["totalprecip_in"]) + "in"
#     #                         day3avghumidity = str(d["forecast"]["forecastday"][2]["day"]["avghumidity"])
#     #                         day3condition = str(d["forecast"]["forecastday"][2]["day"]["condition"]["text"])
#     #                         day3icon = str(d["forecast"]["forecastday"][2]["day"]["condition"]["icon"])
#     #                         day3sunrise = str(d["forecast"]["forecastday"][2]["astro"]["sunrise"])
#     #                         day3sunset = str(d["forecast"]["forecastday"][2]["astro"]["sunset"])
#     #                         day3moonrise = str(d["forecast"]["forecastday"][2]["astro"]["moonrise"])
#     #                         day3moonset = str(d["forecast"]["forecastday"][2]["astro"]["moonset"])
#     #                     except:
#     #                         return messageDetail.ReplyToChat("Sorry, I am not able to get the weather, please try again later")
#     #
#     #                     table_body += "<tr><td>" + day3date + "</td><td>" + day3maxtemp + "</td><td>" + day3mintemp + "</td><td>" + day3avgtemp + "</td><td>" + day3maxwind + "</td><td>" + day3totalprecip + "</td><td>" + day3avghumidity + "</td><td>" + day3condition + "</td><td><img src=\"" + day3icon + "\"/></td><td>" + day3sunrise + "</td><td>" + day3sunset + "</td><td>" + day3moonrise + "</td><td>" + day3moonset + "</td></tr>"
#     #
#     #                     try:
#     #                         #print("4 days")
#     #                         day4date = str(d["forecast"]["forecastday"][3]["date"])
#     #                         day4maxtemp = str(d["forecast"]["forecastday"][3]["day"]["maxtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][3]["day"]["maxtemp_f"]) + " F"
#     #                         day4mintemp = str(d["forecast"]["forecastday"][3]["day"]["mintemp_c"]) + " C / " + str(d["forecast"]["forecastday"][3]["day"]["mintemp_f"]) + " F"
#     #                         day4avgtemp = str(d["forecast"]["forecastday"][3]["day"]["avgtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][3]["day"]["avgtemp_f"]) + " F"
#     #                         day4maxwind = str(d["forecast"]["forecastday"][3]["day"]["maxwind_mph"]) + " mph / " + str(d["forecast"]["forecastday"][3]["day"]["maxwind_kph"]) + " kph"
#     #                         day4totalprecip = str(d["forecast"]["forecastday"][3]["day"]["totalprecip_mm"]) + "mm / " + str(d["forecast"]["forecastday"][3]["day"]["totalprecip_in"]) + "in"
#     #                         day4avghumidity = str(d["forecast"]["forecastday"][3]["day"]["avghumidity"])
#     #                         day4condition = str(d["forecast"]["forecastday"][3]["day"]["condition"]["text"])
#     #                         day4icon = str(d["forecast"]["forecastday"][3]["day"]["condition"]["icon"])
#     #                         day4sunrise = str(d["forecast"]["forecastday"][3]["astro"]["sunrise"])
#     #                         day4sunset = str(d["forecast"]["forecastday"][3]["astro"]["sunset"])
#     #                         day4moonrise = str(d["forecast"]["forecastday"][3]["astro"]["moonrise"])
#     #                         day4moonset = str(d["forecast"]["forecastday"][3]["astro"]["moonset"])
#     #                     except:
#     #                         return messageDetail.ReplyToChat("Sorry, I am not able to get the weather, please try again later")
#     #
#     #                     table_body += "<tr><td>" + day4date + "</td><td>" + day4maxtemp + "</td><td>" + day4mintemp + "</td><td>" + day4avgtemp + "</td><td>" + day4maxwind + "</td><td>" + day4totalprecip + "</td><td>" + day4avghumidity + "</td><td>" + day4condition + "</td><td><img src=\"" + day4icon + "\"/></td><td>" + day4sunrise + "</td><td>" + day4sunset + "</td><td>" + day4moonrise + "</td><td>" + day4moonset + "</td></tr>"
#     #
#     #                     try:
#     #                         #print("5 days")
#     #                         day5date = str(d["forecast"]["forecastday"][4]["date"])
#     #                         day5maxtemp = str(d["forecast"]["forecastday"][4]["day"]["maxtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][4]["day"]["maxtemp_f"]) + " F"
#     #                         day5mintemp = str(d["forecast"]["forecastday"][4]["day"]["mintemp_c"]) + " C / " + str(d["forecast"]["forecastday"][4]["day"]["mintemp_f"]) + " F"
#     #                         day5avgtemp = str(d["forecast"]["forecastday"][4]["day"]["avgtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][4]["day"]["avgtemp_f"]) + " F"
#     #                         day5maxwind = str(d["forecast"]["forecastday"][4]["day"]["maxwind_mph"]) + " mph / " + str(d["forecast"]["forecastday"][4]["day"]["maxwind_kph"]) + " kph"
#     #                         day5totalprecip = str(d["forecast"]["forecastday"][4]["day"]["totalprecip_mm"]) + "mm / " + str(d["forecast"]["forecastday"][4]["day"]["totalprecip_in"]) + "in"
#     #                         day5avghumidity = str(d["forecast"]["forecastday"][4]["day"]["avghumidity"])
#     #                         day5condition = str(d["forecast"]["forecastday"][4]["day"]["condition"]["text"])
#     #                         day5icon = str(d["forecast"]["forecastday"][4]["day"]["condition"]["icon"])
#     #                         day5sunrise = str(d["forecast"]["forecastday"][4]["astro"]["sunrise"])
#     #                         day5sunset = str(d["forecast"]["forecastday"][4]["astro"]["sunset"])
#     #                         day5moonrise = str(d["forecast"]["forecastday"][4]["astro"]["moonrise"])
#     #                         day5moonset = str(d["forecast"]["forecastday"][4]["astro"]["moonset"])
#     #                     except:
#     #                         return messageDetail.ReplyToChat("Sorry, I am not able to get the weather, please try again later")
#     #
#     #                     table_body += "<tr><td>" + day5date + "</td><td>" + day5maxtemp + "</td><td>" + day5mintemp + "</td><td>" + day5avgtemp + "</td><td>" + day5maxwind + "</td><td>" + day5totalprecip + "</td><td>" + day5avghumidity + "</td><td>" + day5condition + "</td><td><img src=\"" + day5icon + "\"/></td><td>" + day5sunrise + "</td><td>" + day5sunset + "</td><td>" + day5moonrise + "</td><td>" + day5moonset + "</td></tr>"
#     #
#     #                 if days == six:
#     #
#     #                     try:
#     #                         #print("2 days")
#     #                         day2date = str(d["forecast"]["forecastday"][1]["date"])
#     #                         day2maxtemp = str(d["forecast"]["forecastday"][1]["day"]["maxtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][1]["day"]["maxtemp_f"]) + " F"
#     #                         day2mintemp = str(d["forecast"]["forecastday"][1]["day"]["mintemp_c"]) + " C / " + str(d["forecast"]["forecastday"][1]["day"]["mintemp_f"]) + " F"
#     #                         day2avgtemp = str(d["forecast"]["forecastday"][1]["day"]["avgtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][1]["day"]["avgtemp_f"]) + " F"
#     #                         day2maxwind = str(d["forecast"]["forecastday"][1]["day"]["maxwind_mph"]) + " mph / " + str(d["forecast"]["forecastday"][1]["day"]["maxwind_kph"]) + " kph"
#     #                         day2totalprecip = str(d["forecast"]["forecastday"][1]["day"]["totalprecip_mm"]) + "mm / " + str(d["forecast"]["forecastday"][1]["day"]["totalprecip_in"]) + "in"
#     #                         day2avghumidity = str(d["forecast"]["forecastday"][1]["day"]["avghumidity"])
#     #                         day2condition = str(d["forecast"]["forecastday"][1]["day"]["condition"]["text"])
#     #                         day2icon = str(d["forecast"]["forecastday"][1]["day"]["condition"]["icon"])
#     #                         day2sunrise = str(d["forecast"]["forecastday"][1]["astro"]["sunrise"])
#     #                         day2sunset = str(d["forecast"]["forecastday"][1]["astro"]["sunset"])
#     #                         day2moonrise = str(d["forecast"]["forecastday"][1]["astro"]["moonrise"])
#     #                         day2moonset = str(d["forecast"]["forecastday"][1]["astro"]["moonset"])
#     #                     except:
#     #                         return messageDetail.ReplyToChat("Sorry, I am not able to get the weather, please try again later")
#     #
#     #                     table_body += "<tr><td>" + day2date + "</td><td>" + day2maxtemp + "</td><td>" + day2mintemp + "</td><td>" + day2avgtemp + "</td><td>" + day2maxwind + "</td><td>" + day2totalprecip + "</td><td>" + day2avghumidity + "</td><td>" + day2condition + "</td><td><img src=\"" + day2icon + "\"/></td><td>" + day2sunrise + "</td><td>" + day2sunset + "</td><td>" + day2moonrise + "</td><td>" + day2moonset + "</td></tr>"
#     #
#     #                     try:
#     #                         #print("3 days")
#     #                         day3date = str(d["forecast"]["forecastday"][2]["date"])
#     #                         day3maxtemp = str(d["forecast"]["forecastday"][2]["day"]["maxtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][2]["day"]["maxtemp_f"]) + " F"
#     #                         day3mintemp = str(d["forecast"]["forecastday"][2]["day"]["mintemp_c"]) + " C / " + str(d["forecast"]["forecastday"][2]["day"]["mintemp_f"]) + " F"
#     #                         day3avgtemp = str(d["forecast"]["forecastday"][2]["day"]["avgtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][2]["day"]["avgtemp_f"]) + " F"
#     #                         day3maxwind = str(d["forecast"]["forecastday"][2]["day"]["maxwind_mph"]) + " mph / " + str(d["forecast"]["forecastday"][2]["day"]["maxwind_kph"]) + " kph"
#     #                         day3totalprecip = str(d["forecast"]["forecastday"][2]["day"]["totalprecip_mm"]) + "mm / " + str(d["forecast"]["forecastday"][2]["day"]["totalprecip_in"]) + "in"
#     #                         day3avghumidity = str(d["forecast"]["forecastday"][2]["day"]["avghumidity"])
#     #                         day3condition = str(d["forecast"]["forecastday"][2]["day"]["condition"]["text"])
#     #                         day3icon = str(d["forecast"]["forecastday"][2]["day"]["condition"]["icon"])
#     #                         day3sunrise = str(d["forecast"]["forecastday"][2]["astro"]["sunrise"])
#     #                         day3sunset = str(d["forecast"]["forecastday"][2]["astro"]["sunset"])
#     #                         day3moonrise = str(d["forecast"]["forecastday"][2]["astro"]["moonrise"])
#     #                         day3moonset = str(d["forecast"]["forecastday"][2]["astro"]["moonset"])
#     #                     except:
#     #                         return messageDetail.ReplyToChat("Sorry, I am not able to get the weather, please try again later")
#     #
#     #                     table_body += "<tr><td>" + day3date + "</td><td>" + day3maxtemp + "</td><td>" + day3mintemp + "</td><td>" + day3avgtemp + "</td><td>" + day3maxwind + "</td><td>" + day3totalprecip + "</td><td>" + day3avghumidity + "</td><td>" + day3condition + "</td><td><img src=\"" + day3icon + "\"/></td><td>" + day3sunrise + "</td><td>" + day3sunset + "</td><td>" + day3moonrise + "</td><td>" + day3moonset + "</td></tr>"
#     #
#     #                     try:
#     #                         #print("4 days")
#     #                         day4date = str(d["forecast"]["forecastday"][3]["date"])
#     #                         day4maxtemp = str(d["forecast"]["forecastday"][3]["day"]["maxtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][3]["day"]["maxtemp_f"]) + " F"
#     #                         day4mintemp = str(d["forecast"]["forecastday"][3]["day"]["mintemp_c"]) + " C / " + str(d["forecast"]["forecastday"][3]["day"]["mintemp_f"]) + " F"
#     #                         day4avgtemp = str(d["forecast"]["forecastday"][3]["day"]["avgtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][3]["day"]["avgtemp_f"]) + " F"
#     #                         day4maxwind = str(d["forecast"]["forecastday"][3]["day"]["maxwind_mph"]) + " mph / " + str(d["forecast"]["forecastday"][3]["day"]["maxwind_kph"]) + " kph"
#     #                         day4totalprecip = str(d["forecast"]["forecastday"][3]["day"]["totalprecip_mm"]) + "mm / " + str(d["forecast"]["forecastday"][3]["day"]["totalprecip_in"]) + "in"
#     #                         day4avghumidity = str(d["forecast"]["forecastday"][3]["day"]["avghumidity"])
#     #                         day4condition = str(d["forecast"]["forecastday"][3]["day"]["condition"]["text"])
#     #                         day4icon = str(d["forecast"]["forecastday"][3]["day"]["condition"]["icon"])
#     #                         day4sunrise = str(d["forecast"]["forecastday"][3]["astro"]["sunrise"])
#     #                         day4sunset = str(d["forecast"]["forecastday"][3]["astro"]["sunset"])
#     #                         day4moonrise = str(d["forecast"]["forecastday"][3]["astro"]["moonrise"])
#     #                         day4moonset = str(d["forecast"]["forecastday"][3]["astro"]["moonset"])
#     #                     except:
#     #                         return messageDetail.ReplyToChat("Sorry, I am not able to get the weather, please try again later")
#     #
#     #                     table_body += "<tr><td>" + day4date + "</td><td>" + day4maxtemp + "</td><td>" + day4mintemp + "</td><td>" + day4avgtemp + "</td><td>" + day4maxwind + "</td><td>" + day4totalprecip + "</td><td>" + day4avghumidity + "</td><td>" + day4condition + "</td><td><img src=\"" + day4icon + "\"/></td><td>" + day4sunrise + "</td><td>" + day4sunset + "</td><td>" + day4moonrise + "</td><td>" + day4moonset + "</td></tr>"
#     #
#     #                     try:
#     #                         #print("5 days")
#     #                         day5date = str(d["forecast"]["forecastday"][4]["date"])
#     #                         day5maxtemp = str(d["forecast"]["forecastday"][4]["day"]["maxtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][4]["day"]["maxtemp_f"]) + " F"
#     #                         day5mintemp = str(d["forecast"]["forecastday"][4]["day"]["mintemp_c"]) + " C / " + str(d["forecast"]["forecastday"][4]["day"]["mintemp_f"]) + " F"
#     #                         day5avgtemp = str(d["forecast"]["forecastday"][4]["day"]["avgtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][4]["day"]["avgtemp_f"]) + " F"
#     #                         day5maxwind = str(d["forecast"]["forecastday"][4]["day"]["maxwind_mph"]) + " mph / " + str(d["forecast"]["forecastday"][4]["day"]["maxwind_kph"]) + " kph"
#     #                         day5totalprecip = str(d["forecast"]["forecastday"][4]["day"]["totalprecip_mm"]) + "mm / " + str(d["forecast"]["forecastday"][4]["day"]["totalprecip_in"]) + "in"
#     #                         day5avghumidity = str(d["forecast"]["forecastday"][4]["day"]["avghumidity"])
#     #                         day5condition = str(d["forecast"]["forecastday"][4]["day"]["condition"]["text"])
#     #                         day5icon = str(d["forecast"]["forecastday"][4]["day"]["condition"]["icon"])
#     #                         day5sunrise = str(d["forecast"]["forecastday"][4]["astro"]["sunrise"])
#     #                         day5sunset = str(d["forecast"]["forecastday"][4]["astro"]["sunset"])
#     #                         day5moonrise = str(d["forecast"]["forecastday"][4]["astro"]["moonrise"])
#     #                         day5moonset = str(d["forecast"]["forecastday"][4]["astro"]["moonset"])
#     #                     except:
#     #                         return messageDetail.ReplyToChat("Sorry, I am not able to get the weather, please try again later")
#     #
#     #                     table_body += "<tr><td>" + day5date + "</td><td>" + day5maxtemp + "</td><td>" + day5mintemp + "</td><td>" + day5avgtemp + "</td><td>" + day5maxwind + "</td><td>" + day5totalprecip + "</td><td>" + day5avghumidity + "</td><td>" + day5condition + "</td><td><img src=\"" + day5icon + "\"/></td><td>" + day5sunrise + "</td><td>" + day5sunset + "</td><td>" + day5moonrise + "</td><td>" + day5moonset + "</td></tr>"
#     #
#     #                     try:
#     #                         #print("6 days")
#     #                         day6date = str(d["forecast"]["forecastday"][5]["date"])
#     #                         day6maxtemp = str(d["forecast"]["forecastday"][5]["day"]["maxtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][5]["day"]["maxtemp_f"]) + " F"
#     #                         day6mintemp = str(d["forecast"]["forecastday"][5]["day"]["mintemp_c"]) + " C / " + str(d["forecast"]["forecastday"][5]["day"]["mintemp_f"]) + " F"
#     #                         day6avgtemp = str(d["forecast"]["forecastday"][5]["day"]["avgtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][5]["day"]["avgtemp_f"]) + " F"
#     #                         day6maxwind = str(d["forecast"]["forecastday"][5]["day"]["maxwind_mph"]) + " mph / " + str(d["forecast"]["forecastday"][5]["day"]["maxwind_kph"]) + " kph"
#     #                         day6totalprecip = str(d["forecast"]["forecastday"][5]["day"]["totalprecip_mm"]) + "mm / " + str(d["forecast"]["forecastday"][5]["day"]["totalprecip_in"]) + "in"
#     #                         day6avghumidity = str(d["forecast"]["forecastday"][5]["day"]["avghumidity"])
#     #                         day6condition = str(d["forecast"]["forecastday"][5]["day"]["condition"]["text"])
#     #                         day6icon = str(d["forecast"]["forecastday"][5]["day"]["condition"]["icon"])
#     #                         day6sunrise = str(d["forecast"]["forecastday"][5]["astro"]["sunrise"])
#     #                         day6sunset = str(d["forecast"]["forecastday"][5]["astro"]["sunset"])
#     #                         day6moonrise = str(d["forecast"]["forecastday"][5]["astro"]["moonrise"])
#     #                         day6moonset = str(d["forecast"]["forecastday"][5]["astro"]["moonset"])
#     #                     except:
#     #                         return messageDetail.ReplyToChat("Sorry, I am not able to get the weather, please try again later")
#     #
#     #                     table_body += "<tr><td>" + day6date + "</td><td>" + day6maxtemp + "</td><td>" + day6mintemp + "</td><td>" + day6avgtemp + "</td><td>" + day6maxwind + "</td><td>" + day6totalprecip + "</td><td>" + day6avghumidity + "</td><td>" + day6condition + "</td><td><img src=\"" + day6icon + "\"/></td><td>" + day6sunrise + "</td><td>" + day6sunset + "</td><td>" + day6moonrise + "</td><td>" + day6moonset + "</td></tr>"
#     #
#     #
#     #                 if days == seven:
#     #
#     #                     try:
#     #                         #print("2 days")
#     #                         day2date = str(d["forecast"]["forecastday"][1]["date"])
#     #                         day2maxtemp = str(d["forecast"]["forecastday"][1]["day"]["maxtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][1]["day"]["maxtemp_f"]) + " F"
#     #                         day2mintemp = str(d["forecast"]["forecastday"][1]["day"]["mintemp_c"]) + " C / " + str(d["forecast"]["forecastday"][1]["day"]["mintemp_f"]) + " F"
#     #                         day2avgtemp = str(d["forecast"]["forecastday"][1]["day"]["avgtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][1]["day"]["avgtemp_f"]) + " F"
#     #                         day2maxwind = str(d["forecast"]["forecastday"][1]["day"]["maxwind_mph"]) + " mph / " + str(d["forecast"]["forecastday"][1]["day"]["maxwind_kph"]) + " kph"
#     #                         day2totalprecip = str(d["forecast"]["forecastday"][1]["day"]["totalprecip_mm"]) + "mm / " + str(d["forecast"]["forecastday"][1]["day"]["totalprecip_in"]) + "in"
#     #                         day2avghumidity = str(d["forecast"]["forecastday"][1]["day"]["avghumidity"])
#     #                         day2condition = str(d["forecast"]["forecastday"][1]["day"]["condition"]["text"])
#     #                         day2icon = str(d["forecast"]["forecastday"][1]["day"]["condition"]["icon"])
#     #                         day2sunrise = str(d["forecast"]["forecastday"][1]["astro"]["sunrise"])
#     #                         day2sunset = str(d["forecast"]["forecastday"][1]["astro"]["sunset"])
#     #                         day2moonrise = str(d["forecast"]["forecastday"][1]["astro"]["moonrise"])
#     #                         day2moonset = str(d["forecast"]["forecastday"][1]["astro"]["moonset"])
#     #                     except:
#     #                         return messageDetail.ReplyToChat("Sorry, I am not able to get the weather, please try again later")
#     #
#     #                     table_body += "<tr><td>" + day2date + "</td><td>" + day2maxtemp + "</td><td>" + day2mintemp + "</td><td>" + day2avgtemp + "</td><td>" + day2maxwind + "</td><td>" + day2totalprecip + "</td><td>" + day2avghumidity + "</td><td>" + day2condition + "</td><td><img src=\"" + day2icon + "\"/></td><td>" + day2sunrise + "</td><td>" + day2sunset + "</td><td>" + day2moonrise + "</td><td>" + day2moonset + "</td></tr>"
#     #
#     #                     try:
#     #                         #print("3 days")
#     #                         day3date = str(d["forecast"]["forecastday"][2]["date"])
#     #                         day3maxtemp = str(d["forecast"]["forecastday"][2]["day"]["maxtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][2]["day"]["maxtemp_f"]) + " F"
#     #                         day3mintemp = str(d["forecast"]["forecastday"][2]["day"]["mintemp_c"]) + " C / " + str(d["forecast"]["forecastday"][2]["day"]["mintemp_f"]) + " F"
#     #                         day3avgtemp = str(d["forecast"]["forecastday"][2]["day"]["avgtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][2]["day"]["avgtemp_f"]) + " F"
#     #                         day3maxwind = str(d["forecast"]["forecastday"][2]["day"]["maxwind_mph"]) + " mph / " + str(d["forecast"]["forecastday"][2]["day"]["maxwind_kph"]) + " kph"
#     #                         day3totalprecip = str(d["forecast"]["forecastday"][2]["day"]["totalprecip_mm"]) + "mm / " + str(d["forecast"]["forecastday"][2]["day"]["totalprecip_in"]) + "in"
#     #                         day3avghumidity = str(d["forecast"]["forecastday"][2]["day"]["avghumidity"])
#     #                         day3condition = str(d["forecast"]["forecastday"][2]["day"]["condition"]["text"])
#     #                         day3icon = str(d["forecast"]["forecastday"][2]["day"]["condition"]["icon"])
#     #                         day3sunrise = str(d["forecast"]["forecastday"][2]["astro"]["sunrise"])
#     #                         day3sunset = str(d["forecast"]["forecastday"][2]["astro"]["sunset"])
#     #                         day3moonrise = str(d["forecast"]["forecastday"][2]["astro"]["moonrise"])
#     #                         day3moonset = str(d["forecast"]["forecastday"][2]["astro"]["moonset"])
#     #                     except:
#     #                         return messageDetail.ReplyToChat("Sorry, I am not able to get the weather, please try again later")
#     #
#     #                     table_body += "<tr><td>" + day3date + "</td><td>" + day3maxtemp + "</td><td>" + day3mintemp + "</td><td>" + day3avgtemp + "</td><td>" + day3maxwind + "</td><td>" + day3totalprecip + "</td><td>" + day3avghumidity + "</td><td>" + day3condition + "</td><td><img src=\"" + day3icon + "\"/></td><td>" + day3sunrise + "</td><td>" + day3sunset + "</td><td>" + day3moonrise + "</td><td>" + day3moonset + "</td></tr>"
#     #
#     #                     try:
#     #                         #print("4 days")
#     #                         day4date = str(d["forecast"]["forecastday"][3]["date"])
#     #                         day4maxtemp = str(d["forecast"]["forecastday"][3]["day"]["maxtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][3]["day"]["maxtemp_f"]) + " F"
#     #                         day4mintemp = str(d["forecast"]["forecastday"][3]["day"]["mintemp_c"]) + " C / " + str(d["forecast"]["forecastday"][3]["day"]["mintemp_f"]) + " F"
#     #                         day4avgtemp = str(d["forecast"]["forecastday"][3]["day"]["avgtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][3]["day"]["avgtemp_f"]) + " F"
#     #                         day4maxwind = str(d["forecast"]["forecastday"][3]["day"]["maxwind_mph"]) + " mph / " + str(d["forecast"]["forecastday"][3]["day"]["maxwind_kph"]) + " kph"
#     #                         day4totalprecip = str(d["forecast"]["forecastday"][3]["day"]["totalprecip_mm"]) + "mm / " + str(d["forecast"]["forecastday"][3]["day"]["totalprecip_in"]) + "in"
#     #                         day4avghumidity = str(d["forecast"]["forecastday"][3]["day"]["avghumidity"])
#     #                         day4condition = str(d["forecast"]["forecastday"][3]["day"]["condition"]["text"])
#     #                         day4icon = str(d["forecast"]["forecastday"][3]["day"]["condition"]["icon"])
#     #                         day4sunrise = str(d["forecast"]["forecastday"][3]["astro"]["sunrise"])
#     #                         day4sunset = str(d["forecast"]["forecastday"][3]["astro"]["sunset"])
#     #                         day4moonrise = str(d["forecast"]["forecastday"][3]["astro"]["moonrise"])
#     #                         day4moonset = str(d["forecast"]["forecastday"][3]["astro"]["moonset"])
#     #                     except:
#     #                         return messageDetail.ReplyToChat("Sorry, I am not able to get the weather, please try again later")
#     #
#     #                     table_body += "<tr><td>" + day4date + "</td><td>" + day4maxtemp + "</td><td>" + day4mintemp + "</td><td>" + day4avgtemp + "</td><td>" + day4maxwind + "</td><td>" + day4totalprecip + "</td><td>" + day4avghumidity + "</td><td>" + day4condition + "</td><td><img src=\"" + day4icon + "\"/></td><td>" + day4sunrise + "</td><td>" + day4sunset + "</td><td>" + day4moonrise + "</td><td>" + day4moonset + "</td></tr>"
#     #
#     #                     try:
#     #                         #print("5 days")
#     #                         day5date = str(d["forecast"]["forecastday"][4]["date"])
#     #                         day5maxtemp = str(d["forecast"]["forecastday"][4]["day"]["maxtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][4]["day"]["maxtemp_f"]) + " F"
#     #                         day5mintemp = str(d["forecast"]["forecastday"][4]["day"]["mintemp_c"]) + " C / " + str(d["forecast"]["forecastday"][4]["day"]["mintemp_f"]) + " F"
#     #                         day5avgtemp = str(d["forecast"]["forecastday"][4]["day"]["avgtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][4]["day"]["avgtemp_f"]) + " F"
#     #                         day5maxwind = str(d["forecast"]["forecastday"][4]["day"]["maxwind_mph"]) + " mph / " + str(d["forecast"]["forecastday"][4]["day"]["maxwind_kph"]) + " kph"
#     #                         day5totalprecip = str(d["forecast"]["forecastday"][4]["day"]["totalprecip_mm"]) + "mm / " + str(d["forecast"]["forecastday"][4]["day"]["totalprecip_in"]) + "in"
#     #                         day5avghumidity = str(d["forecast"]["forecastday"][4]["day"]["avghumidity"])
#     #                         day5condition = str(d["forecast"]["forecastday"][4]["day"]["condition"]["text"])
#     #                         day5icon = str(d["forecast"]["forecastday"][4]["day"]["condition"]["icon"])
#     #                         day5sunrise = str(d["forecast"]["forecastday"][4]["astro"]["sunrise"])
#     #                         day5sunset = str(d["forecast"]["forecastday"][4]["astro"]["sunset"])
#     #                         day5moonrise = str(d["forecast"]["forecastday"][4]["astro"]["moonrise"])
#     #                         day5moonset = str(d["forecast"]["forecastday"][4]["astro"]["moonset"])
#     #                     except:
#     #                         return messageDetail.ReplyToChat("Sorry, I am not able to get the weather, please try again later")
#     #
#     #                     table_body += "<tr><td>" + day5date + "</td><td>" + day5maxtemp + "</td><td>" + day5mintemp + "</td><td>" + day5avgtemp + "</td><td>" + day5maxwind + "</td><td>" + day5totalprecip + "</td><td>" + day5avghumidity + "</td><td>" + day5condition + "</td><td><img src=\"" + day5icon + "\"/></td><td>" + day5sunrise + "</td><td>" + day5sunset + "</td><td>" + day5moonrise + "</td><td>" + day5moonset + "</td></tr>"
#     #
#     #                     try:
#     #                         #print("6 days")
#     #                         day6date = str(d["forecast"]["forecastday"][5]["date"])
#     #                         day6maxtemp = str(d["forecast"]["forecastday"][5]["day"]["maxtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][5]["day"]["maxtemp_f"]) + " F"
#     #                         day6mintemp = str(d["forecast"]["forecastday"][5]["day"]["mintemp_c"]) + " C / " + str(d["forecast"]["forecastday"][5]["day"]["mintemp_f"]) + " F"
#     #                         day6avgtemp = str(d["forecast"]["forecastday"][5]["day"]["avgtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][5]["day"]["avgtemp_f"]) + " F"
#     #                         day6maxwind = str(d["forecast"]["forecastday"][5]["day"]["maxwind_mph"]) + " mph / " + str(d["forecast"]["forecastday"][5]["day"]["maxwind_kph"]) + " kph"
#     #                         day6totalprecip = str(d["forecast"]["forecastday"][5]["day"]["totalprecip_mm"]) + "mm / " + str(d["forecast"]["forecastday"][5]["day"]["totalprecip_in"]) + "in"
#     #                         day6avghumidity = str(d["forecast"]["forecastday"][5]["day"]["avghumidity"])
#     #                         day6condition = str(d["forecast"]["forecastday"][5]["day"]["condition"]["text"])
#     #                         day6icon = str(d["forecast"]["forecastday"][5]["day"]["condition"]["icon"])
#     #                         day6sunrise = str(d["forecast"]["forecastday"][5]["astro"]["sunrise"])
#     #                         day6sunset = str(d["forecast"]["forecastday"][5]["astro"]["sunset"])
#     #                         day6moonrise = str(d["forecast"]["forecastday"][5]["astro"]["moonrise"])
#     #                         day6moonset = str(d["forecast"]["forecastday"][5]["astro"]["moonset"])
#     #                     except:
#     #                         return messageDetail.ReplyToChat("Sorry, I am not able to get the weather, please try again later")
#     #
#     #                     table_body += "<tr><td>" + day6date + "</td><td>" + day6maxtemp + "</td><td>" + day6mintemp + "</td><td>" + day6avgtemp + "</td><td>" + day6maxwind + "</td><td>" + day6totalprecip + "</td><td>" + day6avghumidity + "</td><td>" + day6condition + "</td><td><img src=\"" + day6icon + "\"/></td><td>" + day6sunrise + "</td><td>" + day6sunset + "</td><td>" + day6moonrise + "</td><td>" + day6moonset + "</td></tr>"
#     #
#     #                     try:
#     #                         #print("7 days")
#     #                         day7date = str(d["forecast"]["forecastday"][6]["date"])
#     #                         day7maxtemp = str(d["forecast"]["forecastday"][6]["day"]["maxtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][6]["day"]["maxtemp_f"]) + " F"
#     #                         day7mintemp = str(d["forecast"]["forecastday"][6]["day"]["mintemp_c"]) + " C / " + str(d["forecast"]["forecastday"][6]["day"]["mintemp_f"]) + " F"
#     #                         day7avgtemp = str(d["forecast"]["forecastday"][6]["day"]["avgtemp_c"]) + " C / " + str(d["forecast"]["forecastday"][6]["day"]["avgtemp_f"]) + " F"
#     #                         day7maxwind = str(d["forecast"]["forecastday"][6]["day"]["maxwind_mph"]) + " mph / " + str(d["forecast"]["forecastday"][6]["day"]["maxwind_kph"]) + " kph"
#     #                         day7totalprecip = str(d["forecast"]["forecastday"][6]["day"]["totalprecip_mm"]) + "mm / " + str(d["forecast"]["forecastday"][6]["day"]["totalprecip_in"]) + "in"
#     #                         day7avghumidity = str(d["forecast"]["forecastday"][6]["day"]["avghumidity"])
#     #                         day7condition = str(d["forecast"]["forecastday"][6]["day"]["condition"]["text"])
#     #                         day7icon = str(d["forecast"]["forecastday"][6]["day"]["condition"]["icon"])
#     #                         day7sunrise = str(d["forecast"]["forecastday"][6]["astro"]["sunrise"])
#     #                         day7sunset = str(d["forecast"]["forecastday"][6]["astro"]["sunset"])
#     #                         day7moonrise = str(d["forecast"]["forecastday"][6]["astro"]["moonrise"])
#     #                         day7moonset = str(d["forecast"]["forecastday"][6]["astro"]["moonset"])
#     #                     except:
#     #                         return messageDetail.ReplyToChat("Sorry, I am not able to get the weather, please try again later")
#     #
#     #                     table_body += "<tr><td>" + day7date + "</td><td>" + day7maxtemp + "</td><td>" + day7mintemp + "</td><td>" + day7avgtemp + "</td><td>" + day7maxwind + "</td><td>" + day7totalprecip + "</td><td>" + day7avghumidity + "</td><td>" + day7condition + "</td><td><img src=\"" + day7icon + "\"/></td><td>" + day7sunrise + "</td><td>" + day7sunset + "</td><td>" + day7moonrise + "</td><td>" + day7moonset + "</td></tr>"
#     #
#     #                 table_body += "</tbody></table>"
#     #
#     #                 #return messageDetail.ReplyToChatV2_noBotLog("<card iconSrc=\"https://thumb.ibb.co/csXBgU/Symphony2018_App_Icon_Mobile.png\" accent=\"tempo-bg-color--blue\"><header>The current condition in " + LocationName + ", " + Region + ", " + Country + " as of " + LastUpdated + " is " + Condition + ", <img src=\"" + CurrentURL + "\"/> (" + TempC + " C / " + TempF + " F)<br/></header><body>" + table_body + "</body></card>")
#     #                 return messageDetail.ReplyToChatV2_noBotLog("<card iconSrc=\"\" accent=\"tempo-bg-color--blue\"><header>The current condition in " + LocationName + ", " + Region + ", " + Country + " as of " + LastUpdated + " is " + Condition + ", <img src=\"" + CurrentURL + "\"/> (" + TempC + " C / " + TempF + " F)<br/></header><body>" + table_body + "</body></card>")
#     #
#     #     except:
#     #         return botlog.LogSymphonyInfo("Weather call failed entirely")


### NEW WEATHER API ###
def weather(messageDetail):

    try:

        commandCallerUID = messageDetail.FromUserId

        connComp.request("GET", "/pod/v3/users?uid=" + commandCallerUID, headers=headersCompany)

        resComp = connComp.getresponse()
        dataComp = resComp.read()
        data_raw = str(dataComp.decode('utf-8'))
        # data_dict = ast.literal_eval(data_raw)
        data_dict = json.loads(str(data_raw))

        dataRender = json.dumps(data_dict, indent=2)
        d_org = json.loads(dataRender)

        for index_org in range(len(d_org["users"])):
            firstName = d_org["users"][index_org]["firstName"]
            lastName = d_org["users"][index_org]["lastName"]
            displayName = d_org["users"][index_org]["displayName"]
            #companyName = d_org["users"][index_org]["company"]
            companyNameTemp = d_org["users"][index_org]["company"]
            companyTemp = str(companyNameTemp).replace("&", "&amp;").replace("<", "&lt;").replace('"', "&quot;").replace("'", "&apos;").replace(">", "&gt;")
            companyName = str(companyTemp)
            userID = str(d_org["users"][index_org]["id"])

        botlog.LogSymphonyInfo(firstName + " " + lastName + " (" + displayName + ") from Company/Pod name: " + str(companyName) + " with UID: " + str(userID))
        callerCheck = (firstName + " " + lastName + " - " + displayName + " - " + companyName + " - " + str(userID))

    except:
        botlog.LogSymphonyInfo("Inside second user check")
        commandCallerUID = messageDetail.FromUserId

        connComp.request("GET", "/pod/v3/users?uid=" + commandCallerUID, headers=headersCompany)

        resComp = connComp.getresponse()
        dataComp = resComp.read()
        data_raw = str(dataComp.decode('utf-8'))
        # data_dict = ast.literal_eval(data_raw)
        data_dict = json.loads(str(data_raw))

        dataRender = json.dumps(data_dict, indent=2)
        d_org = json.loads(dataRender)

        for index_org in range(len(d_org["users"])):
            firstName = d_org["users"][index_org]["firstName"]
            lastName = d_org["users"][index_org]["lastName"]
            displayName = d_org["users"][index_org]["displayName"]
            #companyName = d_org["users"][index_org]["company"]
            companyNameTemp = d_org["users"][index_org]["company"]
            companyTemp = str(companyNameTemp).replace("&", "&amp;").replace("<", "&lt;").replace('"', "&quot;").replace("'", "&apos;").replace(">", "&gt;")
            companyName = str(companyTemp)
            userID = str(d_org["users"][index_org]["id"])

        botlog.LogSymphonyInfo(firstName + " " + lastName + " (" + displayName + ") from Company/Pod name: " + str(companyName) + " with UID: " + str(userID))
        callerCheck = (firstName + " " + lastName + " - " + displayName + " - " + companyName + " - " + str(userID))

    try:
        # if callerCheck in AccessFile:
        if companyName in _configDef['AuthCompany']['PodList']:
            #return messageDetail.ReplyToChat("Sorry, the developer is working on a new endpoint, please try this again in few days..")
            botlog.LogSymphonyInfo("Bot Call: Weather")

            #try:

            message = (messageDetail.Command.MessageText)
            weatherCatcher = message.split()
            location = ""

            catchLength = len(weatherCatcher)
            #print("Lenght is: " + (str(catchLength)))

            try:
                emptyLocation = catchLength == 0 or weatherCatcher[0] == ""
                if emptyLocation:
                    return messageDetail.ReplyToChat("Please enter a location, if it is more than one word, e.g New York, please use underscore as in New_York")
                else:
                    location = weatherCatcher[0]
                    #print("Location: " + location)
            except:
                messageDetail.ReplyToChat("Loading the weather forecast")

            url = _configDef['weather']['API_URL']

            querystring = {"access_key": _configDef['weather']['API_Key'], "query": str(location), "units": "m"}

            headers = {
                'Cache-Control': "no-cache",
            }

            response = requests.request("GET", url, headers=headers, params=querystring)
            d = response.json()
            #print(str(d))

            try:

                requestType = str(d["request"]["type"])
                requestQuery = str(d["request"]["query"])
                requestLanguage = str(d["request"]["language"])
                requestUnit = str(d["request"]["unit"])

                locName = str(d["location"]["name"])
                locCountry = str(d["location"]["country"])
                locRegion = str(d["location"]["region"])
                locTimeZone = str(d["location"]["timezone_id"])
                locLocalTime = str(d["location"]["localtime"])


                currentObsTime = str(d["current"]["observation_time"])
                currentTempC = str(d["current"]["temperature"])
                currentTempF_raw = ((int(currentTempC) * (9/5)) + 32)
                currentTempF = str(currentTempF_raw)[:4]

                currentWeatherCode = str(d["current"]["weather_code"])
                currentWeatherIcon = str(d["current"]["weather_icons"]).replace("['", "").replace("']","")
                currentWeatherDesc = str(d["current"]["weather_descriptions"]).replace("['", "").replace("']","")
                currentWindSpeed = str(d["current"]["wind_speed"])
                currentWindDeg = str(d["current"]["wind_degree"])
                currentWindDir = str(d["current"]["wind_dir"])
                currentPressure = str(d["current"]["pressure"])
                currentPrecip = str(d["current"]["precip"])
                currentHumidity = str(d["current"]["humidity"])
                currentCloudCover = str(d["current"]["cloudcover"])
                currentFeeslike = str(d["current"]["feelslike"])
                currentUvIndex = str(d["current"]["uv_index"])
                currentVisibility = str(d["current"]["visibility"])
                currentIsDay = str(d["current"]["is_day"])

            except:
                return messageDetail.ReplyToChat("Sorry, I am not able to get the weather, please try again later")

            table_body = "<table style='table-layout:auto;width:100%'>" \
                         "<thead>" \
                         "<tr class=\"tempo-text-color--white tempo-bg-color--black\">" \
                         "<td>City</td>" \
                         "<td>Region</td>" \
                         "<td>Country</td>" \
                         "<td>Time Zone</td>" \
                         "<td>Local Time</td>" \
                         "<td>Observation Time</td>" \
                         "<td>Temperature</td>" \
                         "<td>Icon</td>" \
                         "<td>Description</td>" \
                         "<td>Wind Speed</td>" \
                         "<td>Wind Degree</td>" \
                         "<td>Wind Direction</td>" \
                         "<td>Pressure</td>" \
                         "<td>Precipitation</td>" \
                         "<td>Humidity</td>" \
                         "<td>Cloud Cover</td>"\
                         "<td>Feels like</td>" \
                         "<td>UV index</td>" \
                         "<td>Visibility</td>" \
                         "<td>Is It Day?</td>" \
                         "</tr>" \
                         "</thead><tbody>"

            table_body += "<tr>" \
                          "<td>" + locName + "</td>" \
                          "<td>" + locRegion + "</td>" \
                          "<td>" + locCountry + "</td>" \
                          "<td>" + locTimeZone + "</td>" \
                          "<td>" + locLocalTime + "</td>" \
                          "<td>" + currentObsTime + "</td>" \
                          "<td>" + currentTempC + "</td>" \
                          "<td><img src=\"" + currentWeatherIcon + "\"/></td>" \
                          "<td>" + currentWeatherDesc + "</td>" \
                          "<td>" + currentWindSpeed + " km/h</td>" \
                          "<td>" + currentWindDeg + "</td>" \
                          "<td>" + currentWindDir + "</td>" \
                          "<td>" + currentPressure + " MB - millibar</td>" \
                          "<td>" + currentPrecip + "M M - millimeters</td>" \
                          "<td>" + currentHumidity + "%</td>" \
                          "<td>" + currentCloudCover + "%</td>" \
                          "<td>" + currentFeeslike + " C</td>" \
                          "<td>" + currentUvIndex + "</td>" \
                          "<td>" + currentVisibility + " km</td>" \
                          "<td>" + currentIsDay + "</td>" \
                          "</tr>"

            table_body += "</tbody></table>"

            #return messageDetail.ReplyToChatV2_noBotLog("<card iconSrc=\"https://thumb.ibb.co/csXBgU/Symphony2018_App_Icon_Mobile.png\" accent=\"tempo-bg-color--blue\"><header>The current condition in " + LocationName + ", " + Region + ", " + Country + " as of " + LastUpdated + " is " + Condition + ", <img src=\"" + CurrentURL + "\"/> (" + TempC + " C / " + TempF + " F)<br/></header><body>" + table_body + "</body></card>")
            return messageDetail.ReplyToChatV2_noBotLog("<card iconSrc=\"\" accent=\"tempo-bg-color--blue\"><header>The current condition in " + locName + ", " + locRegion + ", " + locCountry + " as of " + currentObsTime + " is " + currentTempC + ", <img src=\"" + currentWeatherIcon + "\"/> (" + currentTempC + " C / " + str(currentTempF) + " F)<br/></header><body>" + table_body + "</body></card>")
        # else:
        #     return messageDetail.ReplyToChat("Noy authorized")

    except:
        try:
            botlog.LogSymphonyInfo("Inside Second call Weather")

            # if callerCheck in AccessFile:
            if companyName in _configDef['AuthCompany']['PodList']:
                #return messageDetail.ReplyToChat("Sorry, the developer is working on a new endpoint, please try this again in few days..")
                botlog.LogSymphonyInfo("Bot Call: Weather")

                #try:

                message = (messageDetail.Command.MessageText)
                weatherCatcher = message.split()
                location = ""

                catchLength = len(weatherCatcher)
                #print("Lenght is: " + (str(catchLength)))

                try:
                    emptyLocation = catchLength == 0 or weatherCatcher[0] == ""
                    if emptyLocation:
                        return messageDetail.ReplyToChat("Please enter a location, if it is more than one word, e.g New York, please use underscore as in New_York")
                    else:
                        location = weatherCatcher[0]
                        #print("Location: " + location)
                except:
                    messageDetail.ReplyToChat("Loading the weather forecast")

                url = _configDef['weather']['API_URL']

                querystring = {"access_key": _configDef['weather']['API_Key'], "query": str(location), "units": "m"}

                headers = {
                    'Cache-Control': "no-cache",
                }

                response = requests.request("GET", url, headers=headers, params=querystring)
                d = response.json()
                #print(str(d))

                try:

                    requestType = str(d["request"]["type"])
                    requestQuery = str(d["request"]["query"])
                    requestLanguage = str(d["request"]["language"])
                    requestUnit = str(d["request"]["unit"])

                    locName = str(d["location"]["name"])
                    locCountry = str(d["location"]["country"])
                    locRegion = str(d["location"]["region"])
                    locTimeZone = str(d["location"]["timezone_id"])
                    locLocalTime = str(d["location"]["localtime"])


                    currentObsTime = str(d["current"]["observation_time"])
                    currentTempC = str(d["current"]["temperature"])
                    currentTempF_raw = ((int(currentTempC) * (9/5)) + 32)
                    currentTempF = str(currentTempF_raw)[:4]

                    currentWeatherCode = str(d["current"]["weather_code"])
                    currentWeatherIcon = str(d["current"]["weather_icons"]).replace("['", "").replace("']","")
                    currentWeatherDesc = str(d["current"]["weather_descriptions"]).replace("['", "").replace("']","")
                    currentWindSpeed = str(d["current"]["wind_speed"])
                    currentWindDeg = str(d["current"]["wind_degree"])
                    currentWindDir = str(d["current"]["wind_dir"])
                    currentPressure = str(d["current"]["pressure"])
                    currentPrecip = str(d["current"]["precip"])
                    currentHumidity = str(d["current"]["humidity"])
                    currentCloudCover = str(d["current"]["cloudcover"])
                    currentFeeslike = str(d["current"]["feelslike"])
                    currentUvIndex = str(d["current"]["uv_index"])
                    currentVisibility = str(d["current"]["visibility"])
                    currentIsDay = str(d["current"]["is_day"])

                except:
                    return messageDetail.ReplyToChat("Sorry, I am not able to get the weather, please try again later")

                table_body = "<table style='table-layout:auto;width:100%'>" \
                             "<thead>" \
                             "<tr class=\"tempo-text-color--white tempo-bg-color--black\">" \
                             "<td>City</td>" \
                             "<td>Region</td>" \
                             "<td>Country</td>" \
                             "<td>Time Zone</td>" \
                             "<td>Local Time</td>" \
                             "<td>Observation Time</td>" \
                             "<td>Temperature</td>" \
                             "<td>Icon</td>" \
                             "<td>Description</td>" \
                             "<td>Wind Speed</td>" \
                             "<td>Wind Degree</td>" \
                             "<td>Wind Direction</td>" \
                             "<td>Pressure</td>" \
                             "<td>Precipitation</td>" \
                             "<td>Humidity</td>" \
                             "<td>Cloud Cover</td>"\
                             "<td>Feels like</td>" \
                             "<td>UV index</td>" \
                             "<td>Visibility</td>" \
                             "<td>Is It Day?</td>" \
                             "</tr>" \
                             "</thead><tbody>"

                table_body += "<tr>" \
                              "<td>" + locName + "</td>" \
                              "<td>" + locRegion + "</td>" \
                              "<td>" + locCountry + "</td>" \
                              "<td>" + locTimeZone + "</td>" \
                              "<td>" + locLocalTime + "</td>" \
                              "<td>" + currentObsTime + "</td>" \
                              "<td>" + currentTempC + "</td>" \
                              "<td><img src=\"" + currentWeatherIcon + "\"/></td>" \
                              "<td>" + currentWeatherDesc + "</td>" \
                              "<td>" + currentWindSpeed + " km/h</td>" \
                              "<td>" + currentWindDeg + "</td>" \
                              "<td>" + currentWindDir + "</td>" \
                              "<td>" + currentPressure + " MB - millibar</td>" \
                              "<td>" + currentPrecip + "M M - millimeters</td>" \
                              "<td>" + currentHumidity + "%</td>" \
                              "<td>" + currentCloudCover + "%</td>" \
                              "<td>" + currentFeeslike + " C</td>" \
                              "<td>" + currentUvIndex + "</td>" \
                              "<td>" + currentVisibility + " km</td>" \
                              "<td>" + currentIsDay + "</td>" \
                              "</tr>"

                table_body += "</tbody></table>"

                #return messageDetail.ReplyToChatV2_noBotLog("<card iconSrc=\"https://thumb.ibb.co/csXBgU/Symphony2018_App_Icon_Mobile.png\" accent=\"tempo-bg-color--blue\"><header>The current condition in " + LocationName + ", " + Region + ", " + Country + " as of " + LastUpdated + " is " + Condition + ", <img src=\"" + CurrentURL + "\"/> (" + TempC + " C / " + TempF + " F)<br/></header><body>" + table_body + "</body></card>")
                return messageDetail.ReplyToChatV2_noBotLog("<card iconSrc=\"\" accent=\"tempo-bg-color--blue\"><header>The current condition in " + locName + ", " + locRegion + ", " + locCountry + " as of " + currentObsTime + " is " + currentTempC + ", <img src=\"" + currentWeatherIcon + "\"/> (" + currentTempC + " C / " + str(currentTempF) + " F)<br/></header><body>" + table_body + "</body></card>")

        except:
            return botlog.LogSymphonyInfo("Weather call failed entirely")


def funQuote(messageDetail):

    try:

        commandCallerUID = messageDetail.FromUserId

        connComp.request("GET", "/pod/v3/users?uid=" + commandCallerUID, headers=headersCompany)

        resComp = connComp.getresponse()
        dataComp = resComp.read()
        data_raw = str(dataComp.decode('utf-8'))
        # data_dict = ast.literal_eval(data_raw)
        data_dict = json.loads(str(data_raw))

        dataRender = json.dumps(data_dict, indent=2)
        d_org = json.loads(dataRender)

        for index_org in range(len(d_org["users"])):
            firstName = d_org["users"][index_org]["firstName"]
            lastName = d_org["users"][index_org]["lastName"]
            displayName = d_org["users"][index_org]["displayName"]
            #companyName = d_org["users"][index_org]["company"]
            companyNameTemp = d_org["users"][index_org]["company"]
            companyTemp = str(companyNameTemp).replace("&", "&amp;").replace("<", "&lt;").replace('"', "&quot;").replace("'", "&apos;").replace(">", "&gt;")
            companyName = str(companyTemp)
            userID = str(d_org["users"][index_org]["id"])

        botlog.LogSymphonyInfo(firstName + " " + lastName + " (" + displayName + ") from Company/Pod name: " + str(companyName) + " with UID: " + str(userID))
        callerCheck = (firstName + " " + lastName + " - " + displayName + " - " + companyName + " - " + str(userID))

        # if callerCheck in AccessFile:
        if companyName in _configDef['AuthCompany']['PodList']:

            botlog.LogSymphonyInfo("Bot Call: Fun Quote")
            try:

                try:
                    conn = http.client.HTTPSConnection(_configDef['x-mashape']['URL'])

                    headers = {
                        'x-mashape-key': _configDef['x-mashape']['API_Key'],
                        'cache-control': "no-cache"
                    }

                    conn.request("GET", "/", headers=headers)

                    res = conn.getresponse()
                    data = res.read().decode("utf-8")
                    #print("data: " + data)

                    fundata = str(data)
                    quotedata = fundata.split(":")
                    quote = quotedata[1][:-9]
                    author = quotedata[2][1:][:-12]
                    category = quotedata[3][:-2].replace("\"", "")
                except:
                    return messageDetail.ReplyToChat("Please try FunQuote later.")

                return messageDetail.ReplyToChatV2_noBotLog(category + " quote from <b>" + author + "</b>: <b>" + quote + "</b>")
            except:
                botlog.LogSymphonyInfo("Fun Quote did not work")
    except:
        try:
            botlog.LogSymphonyInfo("Inside Second FunQuote")
            try:
                try:
                    conn = http.client.HTTPSConnection(_configDef['x-mashape']['URL'])

                    headers = {
                        'x-mashape-key': _configDef['x-mashape']['API_Key'],
                        'cache-control': "no-cache"
                    }

                    conn.request("GET", "/", headers=headers)

                    res = conn.getresponse()
                    data = res.read().decode("utf-8")
                    #print("data: " + data)

                    fundata = str(data)
                    quotedata = fundata.split(":")
                    quote = quotedata[1][:-9]
                    author = quotedata[2][1:][:-12]
                    category = quotedata[3][:-2].replace("\"", "")
                except:
                    return messageDetail.ReplyToChat("Please try FunQuote later.")

                return messageDetail.ReplyToChat(category + " quote from <b>" + author + "</b>: <b>" + quote + "</b>")
            except:
                botlog.LogSymphonyInfo("Fun Quote did not work")
        except:
            botlog.LogSymphonyInfo("Fun Quote did not work entirely")

def joke(messageDetail):

    try:
        commandCallerUID = messageDetail.FromUserId

        connComp.request("GET", "/pod/v3/users?uid=" + commandCallerUID, headers=headersCompany)

        resComp = connComp.getresponse()
        dataComp = resComp.read()
        data_raw = str(dataComp.decode('utf-8'))
        # data_dict = ast.literal_eval(data_raw)
        data_dict = json.loads(str(data_raw))

        dataRender = json.dumps(data_dict, indent=2)
        d_org = json.loads(dataRender)

        for index_org in range(len(d_org["users"])):
            firstName = d_org["users"][index_org]["firstName"]
            lastName = d_org["users"][index_org]["lastName"]
            displayName = d_org["users"][index_org]["displayName"]
            #companyName = d_org["users"][index_org]["company"]
            companyNameTemp = d_org["users"][index_org]["company"]
            companyTemp = str(companyNameTemp).replace("&", "&amp;").replace("<", "&lt;").replace('"', "&quot;").replace("'", "&apos;").replace(">", "&gt;")
            companyName = str(companyTemp)
            userID = str(d_org["users"][index_org]["id"])

        botlog.LogSymphonyInfo(firstName + " " + lastName + " (" + displayName + ") from Company/Pod name: " + str(companyName) + " with UID: " + str(userID))
        callerCheck = (firstName + " " + lastName + " - " + displayName + " - " + companyName + " - " + str(userID))

    except:
        try:
            commandCallerUID = messageDetail.FromUserId

            connComp.request("GET", "/pod/v3/users?uid=" + commandCallerUID, headers=headersCompany)

            resComp = connComp.getresponse()
            dataComp = resComp.read()
            data_raw = str(dataComp.decode('utf-8'))
            # data_dict = ast.literal_eval(data_raw)
            data_dict = json.loads(str(data_raw))

            dataRender = json.dumps(data_dict, indent=2)
            d_org = json.loads(dataRender)

            for index_org in range(len(d_org["users"])):
                firstName = d_org["users"][index_org]["firstName"]
                lastName = d_org["users"][index_org]["lastName"]
                displayName = d_org["users"][index_org]["displayName"]
                # companyName = d_org["users"][index_org]["company"]
                companyNameTemp = d_org["users"][index_org]["company"]
                companyTemp = str(companyNameTemp).replace("&", "&amp;").replace("<", "&lt;").replace('"',
                                                                                                      "&quot;").replace(
                    "'", "&apos;").replace(">", "&gt;")
                companyName = str(companyTemp)
                userID = str(d_org["users"][index_org]["id"])

            botlog.LogSymphonyInfo(firstName + " " + lastName + " (" + displayName + ") from Company/Pod name: " + str(
                companyName) + " with UID: " + str(userID))
            callerCheck = (firstName + " " + lastName + " - " + displayName + " - " + companyName + " - " + str(userID))

        except:
            return messageDetail.ReplyToChat("Please try Joke later.")

    # if callerCheck in AccessFile:
    if companyName in _configDef['AuthCompany']['PodList']:

        botlog.LogSymphonyInfo("Bot Call: Joke")

        try:

            try:
                conn = http.client.HTTPSConnection(_configDef['Jokes']['URL'])

                headers = {
                    'accept': "application/json",
                    'user-agent': _configDef['Jokes']['user-agent'],
                    'cache-control': "no-cache"
                }

                conn.request("GET", "/", headers=headers)

                res = conn.getresponse()
                data = res.read().decode("utf-8")

                render = data.split("\":")

                jokeData_raw = render[2][:-8]
                #print(jokeData_raw)
                jokeData = str(jokeData_raw).replace("\\u2013",",").replace("\\u2019", "'").replace("\\u2028", "").replace("\\u201c","").replace("\\u201d", "").replace("\\r\\n", " ").replace("\\n", "").replace('\\"', "")
                #print("Joke: " + str(jokeData))

            except:
                return messageDetail.ReplyToChat("Please try Joke later.")

            return messageDetail.ReplyToChatV2_noBotLog("Here's a joke for you <b> " + jokeData + "</b>")
        except:
            botlog.LogSymphonyInfo("Joke did not work")

def addAcronym(messageDetail):

    try:

        botlog.LogSymphonyInfo("Bot Call: Add Acronym")

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
            # data_dict = ast.literal_eval(data_raw)
            data_dict = json.loads(str(data_raw))

            dataRender = json.dumps(data_dict, indent=2)
            d_org = json.loads(dataRender)

            for index_org in range(len(d_org["users"])):
                firstName = d_org["users"][index_org]["firstName"]
                lastName = d_org["users"][index_org]["lastName"]
                displayName = d_org["users"][index_org]["displayName"]
                #companyName = d_org["users"][index_org]["company"]
                companyNameTemp = d_org["users"][index_org]["company"]
                companyTemp = str(companyNameTemp).replace("&", "&amp;").replace("<", "&lt;").replace('"', "&quot;").replace("'", "&apos;").replace(">", "&gt;")
                companyName = str(companyTemp)
                userID = str(d_org["users"][index_org]["id"])

                botlog.LogSymphonyInfo(str(firstName) + " " + str(lastName) + " from Company/Pod name: " + str(companyName) + " with UID: " + str(userID))
                callerCheck = (str(firstName) + " " + str(lastName) + " - " + str(displayName) + " - " + str(companyName) + " - " + str(userID))
        except:
            return messageDetail.ReplyToChat("Cannot validate user access")

        if callerCheck in AccessFile:

            try:
                #message = (messageDetail.Command.MessageText)
                message_raw = (messageDetail.Command.MessageFlattened)
                message = str(message_raw).replace("/addacronym ", "").replace("/addAcronym ", "")
                info = message.split("|")
                acronym = str(info[0]).strip()
                answer = str(info[1][1:])

                AcronymsDictionary.update({acronym.upper(): str(answer)})
                sortDict(messageDetail)

                return messageDetail.ReplyToChat(acronym + " was successfully added")

            except:
                return messageDetail.ReplyToChat("Invalid format, please use /addAcronym abbreviation | full_sentense")
        # else:
        #     return messageDetail.ReplyToChat("You aren't authorised to use this command.")
    except:
        botlog.LogSymphonyInfo("AddAccronym did not work entirely")

def removeAcronym(messageDetail):

    try:

        botlog.LogSymphonyInfo("Bot Call: Remove Acronym")

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
            # data_dict = ast.literal_eval(data_raw)
            data_dict = json.loads(str(data_raw))

            dataRender = json.dumps(data_dict, indent=2)
            d_org = json.loads(dataRender)

            for index_org in range(len(d_org["users"])):
                firstName = d_org["users"][index_org]["firstName"]
                lastName = d_org["users"][index_org]["lastName"]
                displayName = d_org["users"][index_org]["displayName"]
                #companyName = d_org["users"][index_org]["company"]
                companyNameTemp = d_org["users"][index_org]["company"]
                companyTemp = str(companyNameTemp).replace("&", "&amp;").replace("<", "&lt;").replace('"', "&quot;").replace("'", "&apos;").replace(">", "&gt;")
                companyName = str(companyTemp)
                userID = str(d_org["users"][index_org]["id"])

                botlog.LogSymphonyInfo(firstName + " " + lastName + " from Company/Pod name: " + str(companyName) + " with UID: " + str(userID))
                callerCheck = (firstName + " " + lastName + " - " + displayName + " - " + companyName + " - " + str(userID))

        except:
            return messageDetail.ReplyToChat("Cannot validate user access")

        if callerCheck in AccessFile:

            try:

                Acronym = (messageDetail.Command.MessageText)[1:]

                del AcronymsDictionary[Acronym.upper()]

                updatedDictionary = 'AcronymsDictionary = ' + str(AcronymsDictionary)

                #file = open("modules/command/dictionary.py", "w+")
                file = open("Data/dictionary.py", "w+")
                file.write(updatedDictionary)
                file.close()

                return messageDetail.ReplyToChat(Acronym + " was successfully removed.")
            except:
                return messageDetail.ReplyToChat(Acronym + " was not found.")
        # else:
        #     return messageDetail.ReplyToChat("You aren't authorised to use this command.")
    except:
        botlog.LogSymphonyInfo("Remove Accronym did not work entirely")

def findAcronym(messageDetail):

    try:
        botlog.LogSymphonyInfo("Bot Call: Find Acronym")

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
            # data_dict = ast.literal_eval(data_raw)
            data_dict = json.loads(str(data_raw))

            dataRender = json.dumps(data_dict, indent=2)
            d_org = json.loads(dataRender)

            for index_org in range(len(d_org["users"])):
                firstName = d_org["users"][index_org]["firstName"]
                lastName = d_org["users"][index_org]["lastName"]
                displayName = d_org["users"][index_org]["displayName"]
                #companyName = d_org["users"][index_org]["company"]
                companyNameTemp = d_org["users"][index_org]["company"]
                companyTemp = str(companyNameTemp).replace("&", "&amp;").replace("<", "&lt;").replace('"', "&quot;").replace("'", "&apos;").replace(">", "&gt;")
                companyName = str(companyTemp)
                userID = str(d_org["users"][index_org]["id"])

                botlog.LogSymphonyInfo(
                    firstName + " " + lastName + " from Company/Pod name: " + str(companyName) + " with UID: " + str(userID))
                callerCheck = (firstName + " " + lastName + " - " + displayName + " - " + companyName + " - " + str(userID))

        except:
            return messageDetail.ReplyToChat("Cannot validate user access")

        # if callerCheck in AccessFile:
        if companyName in _configDef['AuthCompany']['PodList']:
            try:
                Acronym = str((messageDetail.Command.MessageText)[1:]).strip()

                return messageDetail.ReplyToChat(Acronym.upper() + " - " + str(AcronymsDictionary[Acronym.upper()]).replace("\n  \n", "<br/><br/>").replace("\n", "<br/>").replace("\u200b",""))
            except:
                return messageDetail.ReplyToChat("No result for " + str(Acronym) + " found")
        else:
            return messageDetail.ReplyToChat("You aren't authorised to use this command.")
    except:
        botlog.LogSymphonyInfo("Find Accronym did not work entirely")

def listAllAcronyms(messageDetail):

    backColor = _configDef['tableBackColor']

    try:

        botlog.LogSymphonyInfo("Bot Call: List All Acronyms")

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
            # data_dict = ast.literal_eval(data_raw)
            data_dict = json.loads(str(data_raw))

            dataRender = json.dumps(data_dict, indent=2)
            d_org = json.loads(dataRender)

            for index_org in range(len(d_org["users"])):
                firstName = d_org["users"][index_org]["firstName"]
                lastName = d_org["users"][index_org]["lastName"]
                displayName = d_org["users"][index_org]["displayName"]
                #companyName = d_org["users"][index_org]["company"]
                companyNameTemp = d_org["users"][index_org]["company"]
                companyTemp = str(companyNameTemp).replace("&", "&amp;").replace("<", "&lt;").replace('"', "&quot;").replace("'", "&apos;").replace(">", "&gt;")
                companyName = str(companyTemp)
                userID = str(d_org["users"][index_org]["id"])

                botlog.LogSymphonyInfo(
                    firstName + " " + lastName + " from Company/Pod name: " + str(companyName) + " with UID: " + str(userID))
                callerCheck = (firstName + " " + lastName + " - " + displayName + " - " + companyName + " - " + str(userID))
        except:
            return messageDetail.ReplyToChat("Cannot validate user access")

        # if callerCheck in AccessFile:
        if companyName in _configDef['AuthCompany']['PodList']:
            try:
                sortDict(messageDetail)
                table_body = ""
                table_header = "<table style='max-width:50%'><thead><tr style='background-color:#4D94FF;color:#ffffff;font-size:1rem' class=\"tempo-text-color--white tempo-bg-color--black\">" \
                               "<td style='max-width:10%'>Acronym</td>" \
                               "</tr></thead><tbody>"
                numberCheck = 0
                for acronym in AcronymsDictionary:
                    numberCheck += 1
                    if (numberCheck % 2) == 0:
                        table_body += "<tr style='background-color:#" + backColor + "'>" \
                                    "<td>" + acronym + " - " + str(AcronymsDictionary[acronym]).replace("\n  \n", "<br/><br/>").replace("\n", "<br/>").replace("\u200b","") + "</td>" \
                                    "</tr>"
                    else:
                        table_body += "<tr>" \
                                  "<td>" + acronym + " - " + str(AcronymsDictionary[acronym]).replace("\n  \n", "<br/><br/>").replace("\n", "<br/>").replace("\u200b","") + "</td>" \
                                  "</tr>"

                table_body += "</tbody></table>"

                reply = table_header + table_body
                #print(str(reply))
                #return messageDetail.ReplyToChatV2_noBotLog("<card iconSrc =\"https://thumb.ibb.co/csXBgU/Symphony2018_App_Icon_Mobile.png\" accent=\"tempo-bg-color--blue\"><header>Acronyms List</header><body>" + reply + "</body></card>")
                return messageDetail.ReplyToChatV2_noBotLog("<card iconSrc =\"\" accent=\"tempo-bg-color--blue\"><header>Acronyms List</header><body>" + reply + "</body></card>")

            except:
                return messageDetail.ReplyToChat("Acronyms not found")
        # else:
        #     return messageDetail.ReplyToChat("You aren't authorised to use this command.")
    except:
        botlog.LogSymphonyInfo("List All Accronym did not work entirely")

def sortDict(messageDetail):

    sortedAcronymsDictionary = {}

    for key in sorted(AcronymsDictionary.keys()):

        sortedAcronymsDictionary.update({key : AcronymsDictionary[key]})


    updatedDictionary = 'AcronymsDictionary = ' + str(sortedAcronymsDictionary)
    file = open("Data/dictionary.py","w+")
    file.write(updatedDictionary)
    file.close()


def wikiSearch(messageDetail):
    ## https://cse.google.com/cse/create/new
    ## https://developers.google.com/custom-search/v1/overview

    try:
        commandCallerUID = messageDetail.FromUserId

        connComp.request("GET", "/pod/v3/users?uid=" + commandCallerUID, headers=headersCompany)

        resComp = connComp.getresponse()
        dataComp = resComp.read()
        data_raw = str(dataComp.decode('utf-8'))
        # data_dict = ast.literal_eval(data_raw)
        data_dict = json.loads(str(data_raw))

        dataRender = json.dumps(data_dict, indent=2)
        d_org = json.loads(dataRender)

        for index_org in range(len(d_org["users"])):
            firstName = d_org["users"][index_org]["firstName"]
            lastName = d_org["users"][index_org]["lastName"]
            displayName = d_org["users"][index_org]["displayName"]
            #companyName = d_org["users"][index_org]["company"]
            companyNameTemp = d_org["users"][index_org]["company"]
            companyTemp = str(companyNameTemp).replace("&", "&amp;").replace("<", "&lt;").replace('"', "&quot;").replace("'", "&apos;").replace(">", "&gt;")
            companyName = str(companyTemp)
            userID = str(d_org["users"][index_org]["id"])

            botlog.LogSymphonyInfo(
                firstName + " " + lastName + " from Company/Pod name: " + str(companyName) + " with UID: " + str(userID))
            callerCheck = (firstName + " " + lastName + " - " + displayName + " - " + companyName + " - " + str(userID))
    except:
        try:
            botlog.LogSymphonyInfo("Inside Second user check")
            commandCallerUID = messageDetail.FromUserId

            connComp.request("GET", "/pod/v3/users?uid=" + commandCallerUID, headers=headersCompany)

            resComp = connComp.getresponse()
            dataComp = resComp.read()
            data_raw = str(dataComp.decode('utf-8'))
            # data_dict = ast.literal_eval(data_raw)
            data_dict = json.loads(str(data_raw))

            dataRender = json.dumps(data_dict, indent=2)
            d_org = json.loads(dataRender)

            for index_org in range(len(d_org["users"])):
                firstName = d_org["users"][index_org]["firstName"]
                lastName = d_org["users"][index_org]["lastName"]
                displayName = d_org["users"][index_org]["displayName"]
                #companyName = d_org["users"][index_org]["company"]
                companyNameTemp = d_org["users"][index_org]["company"]
                companyTemp = str(companyNameTemp).replace("&", "&amp;").replace("<", "&lt;").replace('"', "&quot;").replace("'", "&apos;").replace(">", "&gt;")
                companyName = str(companyTemp)
                userID = str(d_org["users"][index_org]["id"])

                botlog.LogSymphonyInfo(
                    firstName + " " + lastName + " from Company/Pod name: " + str(companyName) + " with UID: " + str(userID))
                callerCheck = (firstName + " " + lastName + " - " + displayName + " - " + companyName + " - " + str(userID))
        except:
            return messageDetail.ReplyToChat("Cannot validate user access")


    # if callerCheck in AccessFile:
    if companyName in _configDef['AuthCompany']['PodList']:
        botlog.LogSymphonyInfo("Bot Call: Wiki Search")
        try:
            request_raw = (messageDetail.Command.MessageText)
            request = str(request_raw).split()

            my_api_key = _configDef['Wiki']['API_Key']
            my_cse_id = _configDef['Wiki']['token']

            try:
                service = build("customsearch", "v1", developerKey=my_api_key)
                res = service.cse().list(q=request, cx=my_cse_id, num=5).execute()
                results = res['items']
                #print(str(results))
            except:
                return messageDetail.ReplyToChat("Please use a valid search")

            table_body = ""
            table_header = "<table style='max-width:95%'><thead><tr style='background-color:#4D94FF;color:#ffffff;font-size:1rem' class=\"tempo-text-color--white tempo-bg-color--black\">" \
                           "<td style='max-width:10%'>Link</td>" \
                           "<td>Information</td>" \
                           "</tr></thead><tbody>"

            for result in results:
                link_raw = result["link"]
                link = str(link_raw).replace(_configDef['Wiki']['replace'], "")
                print(str(link))

                table_body += "<tr>" \
                              "<td><a href =\"" + link_raw + "\">" + link + "</a></td>" \
                              "<td>" + str(result["snippet"]).replace("&", "&amp;").replace("<", "&lt;").replace('"', "&quot;").replace("'", "&apos;").replace(">", "&gt;") + "</td>" \
                              "</tr>"

            table_body += "</tbody></table>"

            reply = table_header + table_body
            return messageDetail.ReplyToChatV2_noBotLog(reply)

        except:
            try:
                botlog.LogSymphonyInfo("Inside Second Wiki")
                try:
                    request_raw = (messageDetail.Command.MessageText)
                    request = str(request_raw).split()

                    my_api_key = _configDef['Wiki']['API_Key']
                    my_cse_id = _configDef['Wiki']['token']

                    try:
                        service = build("customsearch", "v1", developerKey=my_api_key)
                        res = service.cse().list(q=request, cx=my_cse_id, num=3).execute()
                        results = res['items']
                        #print(str(results))
                    except:
                        return messageDetail.ReplyToChat("Please use a valid search")

                    table_body = ""
                    table_header = "<table style='max-width:95%'><thead><tr style='background-color:#4D94FF;color:#ffffff;font-size:1rem' class=\"tempo-text-color--white tempo-bg-color--black\">" \
                                   "<td style='max-width:10%'>Link</td>" \
                                   "<td>Information</td>" \
                                   "</tr></thead><tbody>"

                    for result in results:
                        link_raw = result["link"]
                        link = str(link_raw).replace(_configDef['Wiki']['replace'], "")

                        table_body += "<tr>" \
                                      "<td><a href =\"" + link_raw + "\">" + link + "</a></td>" \
                                      "<td>" + str(result["snippet"]).replace("&", "&amp;").replace("<", "&lt;").replace('"', "&quot;").replace("'", "&apos;").replace(">", "&gt;") + "</td>" \
                                      "</tr>"

                    table_body += "</tbody></table>"

                    reply = table_header + table_body
                    return messageDetail.ReplyToChatV2_noBotLog(reply)

                except:
                    return messageDetail.ReplyToChat("Please make sure to use /wiki <data>")
            except:
                botlog.LogSymphonyInfo("WikiSearch did not work entirely")

##############

def whois(messageDetail):
    botlog.LogSymphonyInfo("Bot Call: Whois")

    try:
        # try:
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
        # data_dict = ast.literal_eval(data_raw)
        data_dict = json.loads(str(data_raw))

        dataRender = json.dumps(data_dict, indent=2)
        d_org = json.loads(dataRender)

        for index_org in range(len(d_org["users"])):
            firstName = d_org["users"][index_org]["firstName"]
            lastName = d_org["users"][index_org]["lastName"]
            displayName = d_org["users"][index_org]["displayName"]
            #companyName = d_org["users"][index_org]["company"]
            companyNameTemp = d_org["users"][index_org]["company"]
            companyTemp = str(companyNameTemp).replace("&", "&amp;").replace("<", "&lt;").replace('"', "&quot;").replace("'", "&apos;").replace(">", "&gt;")
            companyName = str(companyTemp)
            userID = str(d_org["users"][index_org]["id"])

            botlog.LogSymphonyInfo(firstName + " " + lastName + " (" + displayName + ") from Company/Pod name: " + str(companyName) + " with UID: " + str(userID))
            callerCheck = (firstName + " " + lastName + " - " + displayName + " - " + companyName + " - " + str(userID))
        # except:
        #     return messageDetail.ReplyToChat("Cannot validate user access")

        if callerCheck in AccessFile:

            try:
                try:
                    flat = messageDetail.Command.MessageFlattened.split("_u_")
                    #UID = flat[1][:int(_configDef['UID'])]
                    UID = flat[1]
                    botlog.LogSymphonyInfo("User UI: " + UID)
                    connComp.request("GET", "/pod/v3/users?uid=" + UID + "&local=false", headers=headersCompany)
                except:
                    try:
                        flat = messageDetail.Command.MessageText
                        user_email = str(flat).strip()
                        botlog.LogSymphonyInfo("User Email: " + str(user_email))
                        connComp.request("GET", "/pod/v3/users?email=" + user_email + "&local=false", headers=headersCompany)
                    except:
                        return messageDetail.ReplyToChat("Please use @mention or email address to do the user lookup")

                resComp = connComp.getresponse()
                dataComp = resComp.read()
                data_raw = str(dataComp.decode('utf-8'))
                # data_dict = ast.literal_eval(data_raw)
                data_dict = json.loads(str(data_raw))

                dataRender = json.dumps(data_dict, indent=2)
                d_org = json.loads(dataRender)

                table_body = ""
                table_header = "<table style='max-width:100%;table-layout:auto'><thead><tr style='background-color:#4D94FF;color:#ffffff;font-size:1rem' class=\"tempo-text-color--white tempo-bg-color--black\">" \
                               "<td style='max-width:20%'>ID</td>" \
                               "<td style='max-width:20%'>EMAIL ADDRESS</td>" \
                               "<td style='max-width:20%'>FIRST NAME</td>" \
                               "<td style='max-width:20%'>LAST NAME</td>" \
                               "<td style='max-width:20%'>DISPLAY NAME</td>" \
                               "<td style='max-width:20%'>TITLE</td>" \
                               "<td style='max-width:20%'>COMPANY</td>" \
                               "<td style='max-width:20%'>LOCATION</td>" \
                               "</tr></thead><tbody>"

                for index_org in range(len(d_org["users"])):

                    try:
                        try:
                            firstName = d_org["users"][index_org]["firstName"]
                            lastName = d_org["users"][index_org]["lastName"]
                        except:
                            return messageDetail.ReplyToChat("I am a Top Secret Agent Bot, I do no share my info :)")
                        displayName = d_org["users"][index_org]["displayName"]
                        try:
                            title = d_org["users"][index_org]["title"]
                        except:
                            title = "N/A"
                        try:
                            companyName = d_org["users"][index_org]["company"]
                        except:
                            companyName = "N/A"
                        userID = str(d_org["users"][index_org]["id"])
                        try:
                            emailAddress = str(d_org["users"][index_org]["emailAddress"])
                        except:
                            emailAddress = "N/A"
                        try:
                            location = str(d_org["users"][index_org]["location"])
                        except:
                            location = "N/A"
                    except:
                        return messageDetail.ReplyToChat("Cannot find user info for Whois command")

                    table_body += "<tr>" \
                                  "<td>" + str(userID) + "</td>" \
                                  "<td>" + str(emailAddress) + "</td>" \
                                  "<td>" + str(firstName) + "</td>" \
                                  "<td>" + str(lastName) + "</td>" \
                                  "<td>" + str(displayName) + "</td>" \
                                  "<td>" + str(title) + "</td>" \
                                  "<td>" + str(companyName) + "</td>" \
                                  "<td>" + str(location) + "</td>" \
                                  "</tr>"

                    table_body += "</tbody></table>"

                reply = table_header + table_body
                #return messageDetail.ReplyToChatV2_noBotLog("<card iconSrc =\"https://thumb.ibb.co/csXBgU/Symphony2018_App_Icon_Mobile.png\" accent=\"tempo-bg-color--blue\"><header>User details</header><body>" + reply + "</body></card>")
                return messageDetail.ReplyToChatV2_noBotLog("<card iconSrc =\"\" accent=\"tempo-bg-color--blue\"><header>User details</header><body>" + reply + "</body></card>")

            # else:
            #     return messageDetail.ReplyToChat("You aren't authorised to use this command.")
            except:
                return messageDetail.ReplyToChatV2_noBotLog("Please make sure you have entered a valid UID or email address")
    except:
        try:
            botlog.LogSymphonyInfo("Inside second try for Whois")

            try:
                flat = messageDetail.Command.MessageFlattened.split("_u_")
                #UID = flat[1][:int(_configDef['UID'])]
                UID = flat[1]
                botlog.LogSymphonyInfo("User UI: " + UID)
                connComp.request("GET", "/pod/v3/users?uid=" + UID + "&local=false", headers=headersCompany)
            except:
                try:
                    flat = messageDetail.Command.MessageText
                    user_email = str(flat).strip()
                    botlog.LogSymphonyInfo("User Email: " + str(user_email))
                    connComp.request("GET", "/pod/v3/users?email=" + user_email + "&local=false", headers=headersCompany)
                except:
                    return messageDetail.ReplyToChat("Please use @mention or email address to do the user lookup")

            resComp = connComp.getresponse()
            dataComp = resComp.read()
            data_raw = str(dataComp.decode('utf-8'))
            # data_dict = ast.literal_eval(data_raw)
            data_dict = json.loads(str(data_raw))

            dataRender = json.dumps(data_dict, indent=2)
            d_org = json.loads(dataRender)

            table_body = ""
            table_header = "<table style='max-width:100%;table-layout:auto'><thead><tr style='background-color:#4D94FF;color:#ffffff;font-size:1rem' class=\"tempo-text-color--white tempo-bg-color--black\">" \
                           "<td style='max-width:20%'>ID</td>" \
                           "<td style='max-width:20%'>EMAIL ADDRESS</td>" \
                           "<td style='max-width:20%'>FIRST NAME</td>" \
                           "<td style='max-width:20%'>LAST NAME</td>" \
                           "<td style='max-width:20%'>DISPLAY NAME</td>" \
                           "<td style='max-width:20%'>TITLE</td>" \
                           "<td style='max-width:20%'>COMPANY</td>" \
                           "<td style='max-width:20%'>LOCATION</td>" \
                           "</tr></thead><tbody>"

            for index_org in range(len(d_org["users"])):

                try:
                    try:
                        firstName = d_org["users"][index_org]["firstName"]
                        lastName = d_org["users"][index_org]["lastName"]
                    except:
                        return messageDetail.ReplyToChat("I am a Top Secret Agent Bot, I do no share my info :)")
                    displayName = d_org["users"][index_org]["displayName"]
                    try:
                        title = d_org["users"][index_org]["title"]
                    except:
                        title = "N/A"
                    try:
                        companyName = d_org["users"][index_org]["company"]
                    except:
                        companyName = "N/A"
                    userID = str(d_org["users"][index_org]["id"])
                    try:
                        emailAddress = str(d_org["users"][index_org]["emailAddress"])
                    except:
                        emailAddress = "N/A"
                    try:
                        location = str(d_org["users"][index_org]["location"])
                    except:
                        location = "N/A"
                except:
                    return messageDetail.ReplyToChat("Cannot find user info for Whois command")

                table_body += "<tr>" \
                              "<td>" + str(userID) + "</td>" \
                              "<td>" + str(emailAddress) + "</td>" \
                              "<td>" + str(firstName) + "</td>" \
                              "<td>" + str(lastName) + "</td>" \
                              "<td>" + str(displayName) + "</td>" \
                              "<td>" + str(title) + "</td>" \
                              "<td>" + str(companyName) + "</td>" \
                              "<td>" + str(location) + "</td>" \
                              "</tr>"

                table_body += "</tbody></table>"

            reply = table_header + table_body
            #return messageDetail.ReplyToChatV2_noBotLog("<card iconSrc =\"https://thumb.ibb.co/csXBgU/Symphony2018_App_Icon_Mobile.png\" accent=\"tempo-bg-color--blue\"><header>User details</header><body>" + reply + "</body></card>")
            return messageDetail.ReplyToChatV2_noBotLog("<card iconSrc =\"\" accent=\"tempo-bg-color--blue\"><header>User details</header><body>" + reply + "</body></card>")

            # else:
            #     return messageDetail.ReplyToChat("You aren't authorised to use this command.")
        except:
            botlog.LogSymphonyInfo("Whois did not work entirely")


def streamCheck(messageDetail):

    botlog.LogSymphonyInfo("Bot Call: streamCheck")

    try:
        # try:
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
        # data_dict = ast.literal_eval(data_raw)
        data_dict = json.loads(str(data_raw))

        dataRender = json.dumps(data_dict, indent=2)
        d_org = json.loads(dataRender)

        for index_org in range(len(d_org["users"])):
            firstName = d_org["users"][index_org]["firstName"]
            lastName = d_org["users"][index_org]["lastName"]
            displayName = d_org["users"][index_org]["displayName"]
            #companyName = d_org["users"][index_org]["company"]
            companyNameTemp = d_org["users"][index_org]["company"]
            companyTemp = str(companyNameTemp).replace("&", "&amp;").replace("<", "&lt;").replace('"', "&quot;").replace("'", "&apos;").replace(">", "&gt;")
            companyName = str(companyTemp)
            userID = str(d_org["users"][index_org]["id"])

            botlog.LogSymphonyInfo(firstName + " " + lastName + " (" + displayName + ") from Company/Pod name: " + str(companyName) + " with UID: " + str(userID))
            callerCheck = (firstName + " " + lastName + " - " + displayName + " - " + companyName + " - " + str(userID))
        # except:
        #     return messageDetail.ReplyToChat("Cannot validate user access")


        if callerCheck in AccessFile:
            try:

                try:
                    stream_raw = messageDetail.Command.MessageFlattened.split(" ")
                    stream_split = str(stream_raw).split(",")
                    stream_split_Data = stream_split[1].replace("'", "").replace("]","")
                    try:
                        streamID = str(stream_split_Data).replace(" ","")
                    except:
                        streamID = str(stream_split_Data).replace(" ","").replace("/", "_").replace("==", "").replace("+", "-")
                except:
                    return messageDetail.ReplyToChatV2("Please a valid stream ID converted into <a href=\"https://rest-api.symphony.com/docs/message-id\">base64</a>")

                connComp = http.client.HTTPSConnection(_configDef['symphonyinfo']['pod_hostname'])
                sessionTok = callout.GetSessionToken()

                headersCompany = {
                    'sessiontoken': sessionTok,
                    'cache-control': "no-cache"
                }

                connComp.request("GET", "/pod/v2/streams/" + streamID + "/info", headers=headersCompany)

                res = connComp.getresponse()
                data = res.read().decode("utf-8")
                #print(data)

                invalidStreamID = "{\"code\":400,\"message\":\"Invalid stream ID\"}"

                if data == invalidStreamID:
                    return messageDetail.ReplyToChatV2("Please enter a valid StreamID/ConversationID, converted into <a href=\"https://rest-api.symphony.com/docs/message-id\">base64</a>")

                data_raw = str(data).split(",\"")

                try:
                    stream_id_raw = data_raw[0]
                    stream_id_split = str(stream_id_raw).split(":")
                    stream_id = str(stream_id_split[1]).replace("\"","")
                except:
                    return messageDetail.ReplyToChat("Cannot find stream Id")

                try:
                    xpod_raw = data_raw[1]
                    xpod_split = str(xpod_raw).split(":")
                    xpod = str(xpod_split[1])
                except:
                    return messageDetail.ReplyToChat("Cannot find Xpod info")

                try:
                    active_raw = data_raw[3]
                    active_split = str(active_raw).split(":")
                    active = str(active_split[1])
                except:
                    return messageDetail.ReplyToChat("Cannot find Active info")

                try:
                    last_msg_raw = data_raw[4]
                    last_msg_split = str(last_msg_raw).split(":")
                    last_msg = str(last_msg_split[1])
                except:
                    return messageDetail.ReplyToChat("Cannot find Last Message time")

                try:
                    streamType_raw = data_raw[5]
                    streamType_split = str(streamType_raw).split(":{")
                    streamType = str(streamType_split[1]).replace("\"","").replace("type:","").replace("}","")
                except:
                    return messageDetail.ReplyToChat("Cannot find stream type")

                try:
                    attribute_raw = data_raw[6]
                    attribute_split = str(attribute_raw).split(":")
                    attribute = str(attribute_split[2]).replace("\"","").replace("}","").replace("'","").replace("[","").replace("]","")
                except:
                    return messageDetail.ReplyToChat("Cannot find stream attributes")


                table_body = ""
                table_header = "<table style='max-width:100%;table-layout:auto'><thead><tr style='background-color:#4D94FF;color:#ffffff;font-size:1rem' class=\"tempo-text-color--white tempo-bg-color--black\">" \
                               "<td style='max-width:20%'>ID</td>" \
                               "<td style='max-width:20%'>CROSS POD</td>" \
                               "<td style='max-width:20%'>ACTIVE</td>" \
                               "<td style='max-width:20%'>LAST MSG</td>" \
                               "<td style='max-width:20%'>STREAM TYPE</td>" \
                               "<td style='max-width:20%'>ATTRIBUTES</td>" \
                               "</tr></thead><tbody>"

                table_body += "<tr>" \
                              "<td>" + str(stream_id) + "</td>" \
                              "<td>" + str(xpod) + "</td>" \
                              "<td>" + str(active) + "</td>" \
                              "<td>" + str(last_msg) + "</td>" \
                              "<td>" + str(streamType) + "</td>" \
                              "<td>" + str(attribute) + "</td>" \
                              "</tr>"

                table_body += "</tbody></table>"

                reply = table_header + table_body
                #return messageDetail.ReplyToChatV2_noBotLog("<card iconSrc =\"https://thumb.ibb.co/csXBgU/Symphony2018_App_Icon_Mobile.png\" accent=\"tempo-bg-color--blue\"><header>Stream details</header><body>" + reply + "</body></card>")
                return messageDetail.ReplyToChatV2_noBotLog("<card iconSrc =\"\" accent=\"tempo-bg-color--blue\"><header>Stream details</header><body>" + reply + "</body></card>")

            # else:
            #     return messageDetail.ReplyToChat("You aren't authorised to use this command.")
            except:
                botlog.LogSymphonyInfo("StreamCheck did not work")
    except:
        try:
            botlog.LogSymphonyInfo("Inside second try for StreamCheck")
            try:
                stream_raw = messageDetail.Command.MessageFlattened.split(" ")
                stream_split = str(stream_raw).split(",")
                stream_split_Data = stream_split[1].replace("'", "").replace("]","")
                try:
                    streamID = str(stream_split_Data).replace(" ","")
                except:
                    streamID = str(stream_split_Data).replace(" ","").replace("/", "_").replace("==", "").replace("+", "-")
            except:
                return messageDetail.ReplyToChatV2("Please a valid stream ID converted into <a href=\"https://rest-api.symphony.com/docs/message-id\">base64</a>")

            connComp = http.client.HTTPSConnection(_configDef['symphonyinfo']['pod_hostname'])
            sessionTok = callout.GetSessionToken()

            headersCompany = {
                'sessiontoken': sessionTok,
                'cache-control': "no-cache"
            }

            connComp.request("GET", "/pod/v2/streams/" + streamID + "/info", headers=headersCompany)

            res = connComp.getresponse()
            data = res.read().decode("utf-8")

            invalidStreamID = "{\"code\":400,\"message\":\"Invalid stream ID\"}"

            if data == invalidStreamID:
                return messageDetail.ReplyToChatV2("Please enter a valid StreamID/ConversationID, converted into <a href=\"https://rest-api.symphony.com/docs/message-id\">base64</a>")

            data_raw = str(data).split(",\"")

            try:
                stream_id_raw = data_raw[0]
                stream_id_split = str(stream_id_raw).split(":")
                stream_id = str(stream_id_split[1]).replace("\"","")
            except:
                return messageDetail.ReplyToChat("Cannot find stream Id")

            try:
                xpod_raw = data_raw[1]
                xpod_split = str(xpod_raw).split(":")
                xpod = str(xpod_split[1])
            except:
                return messageDetail.ReplyToChat("Cannot find Xpod info")

            try:
                active_raw = data_raw[3]
                active_split = str(active_raw).split(":")
                active = str(active_split[1])
            except:
                return messageDetail.ReplyToChat("Cannot find Active info")

            try:
                last_msg_raw = data_raw[4]
                last_msg_split = str(last_msg_raw).split(":")
                last_msg = str(last_msg_split[1])
            except:
                return messageDetail.ReplyToChat("Cannot find Last Message time")

            try:
                streamType_raw = data_raw[5]
                streamType_split = str(streamType_raw).split(":")
                streamType = str(streamType_split[1]).replace("\"","").replace("type:","").replace("}","")
            except:
                return messageDetail.ReplyToChat("Cannot find stream type")

            try:
                attribute_raw = data_raw[6]
                attribute_split = str(attribute_raw).split(":")
                attribute = str(attribute_split[2]).replace("\"","").replace("}","").replace("'","").replace("[","").replace("]","")
            except:
                return messageDetail.ReplyToChat("Cannot find stream attributes")


            table_body = ""
            table_header = "<table style='max-width:100%;table-layout:auto'><thead><tr style='background-color:#4D94FF;color:#ffffff;font-size:1rem' class=\"tempo-text-color--white tempo-bg-color--black\">" \
                           "<td style='max-width:20%'>ID</td>" \
                           "<td style='max-width:20%'>CROSS POD</td>" \
                           "<td style='max-width:20%'>ACTIVE</td>" \
                           "<td style='max-width:20%'>LAST MSG</td>" \
                           "<td style='max-width:20%'>STREAM TYPE</td>" \
                           "<td style='max-width:20%'>ATTRIBUTES</td>" \
                           "</tr></thead><tbody>"

            table_body += "<tr>" \
                          "<td>" + str(stream_id) + "</td>" \
                          "<td>" + str(xpod) + "</td>" \
                          "<td>" + str(active) + "</td>" \
                          "<td>" + str(last_msg) + "</td>" \
                          "<td>" + str(streamType) + "</td>" \
                          "<td>" + str(attribute) + "</td>" \
                          "</tr>"

            table_body += "</tbody></table>"

            reply = table_header + table_body
            #return messageDetail.ReplyToChatV2_noBotLog("<card iconSrc =\"https://thumb.ibb.co/csXBgU/Symphony2018_App_Icon_Mobile.png\" accent=\"tempo-bg-color--blue\"><header>Stream details</header><body>" + reply + "</body></card>")
            return messageDetail.ReplyToChatV2_noBotLog("<card iconSrc =\"\" accent=\"tempo-bg-color--blue\"><header>Stream details</header><body>" + reply + "</body></card>")

            # else:
            #     return messageDetail.ReplyToChat("You aren't authorised to use this command.")
        except:
            botlog.LogSymphonyInfo("StreamCheck did not work entirely")

def UIDCheck(messageDetail):
    botlog.LogSymphonyInfo("Bot Call: UIDCheck")
    try:
        # try:
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
        # data_dict = ast.literal_eval(data_raw)
        data_dict = json.loads(str(data_raw))

        dataRender = json.dumps(data_dict, indent=2)
        d_org = json.loads(dataRender)

        for index_org in range(len(d_org["users"])):
            firstName = d_org["users"][index_org]["firstName"]
            lastName = d_org["users"][index_org]["lastName"]
            displayName = d_org["users"][index_org]["displayName"]
            #companyName = d_org["users"][index_org]["company"]
            companyNameTemp = d_org["users"][index_org]["company"]
            companyTemp = str(companyNameTemp).replace("&", "&amp;").replace("<", "&lt;").replace('"', "&quot;").replace("'", "&apos;").replace(">", "&gt;")
            companyName = str(companyTemp)
            userID = str(d_org["users"][index_org]["id"])

            botlog.LogSymphonyInfo(firstName + " " + lastName + " (" + displayName + ") from Company/Pod name: " + str(companyName) + " with UID: " + str(userID))
            callerCheck = (firstName + " " + lastName + " - " + displayName + " - " + companyName + " - " + str(userID))

        # except:
        #     return messageDetail.ReplyToChat("Cannot validate user access")

        if callerCheck in AccessFile:
            try:

                try:
                    UID_raw = messageDetail.Command.MessageText
                    UID = str(UID_raw).replace(" ", "")
                    #UID_lenght = len(str(UID))
                except:
                    return messageDetail.ReplyToChat("Please use enter UID of the Symphony user to lookup")

                # # if str(UID_lenght) != "14":
                # if str(UID_lenght) != _configDef['UID']:
                #     return messageDetail.ReplyToChat("Please enter a valid UID, with " + _configDef['UID'] + " digits")

                connComp = http.client.HTTPSConnection(_configDef['symphonyinfo']['pod_hostname'])
                sessionTok = callout.GetSessionToken()

                headersCompany = {
                    'sessiontoken': sessionTok,
                    'cache-control': "no-cache"
                }

                connComp.request("GET", "/pod/v3/users?uid=" + UID + "&local=false", headers=headersCompany)

                try:
                    resComp = connComp.getresponse()
                    dataComp = resComp.read()
                    data_raw = str(dataComp.decode('utf-8'))
                    # data_dict = ast.literal_eval(data_raw)
                    data_dict = json.loads(str(data_raw))

                    dataRender = json.dumps(data_dict, indent=2)
                    d_org = json.loads(dataRender)

                except:
                    return messageDetail.ReplyToChat("Please enter a valid UID")

                notValidUI = "{'code': 400, 'message': 'At least one query paramemer (uid or email) needs to be present.'}"
                notValidUID = "{'code': 400, 'message': 'All uids are invalid.'}"

                if str(d_org).startswith(notValidUI):
                    return messageDetail.ReplyToChat("Please enter the UID of the Symphony User to Lookup")
                if str(d_org).startswith(notValidUID):
                    return messageDetail.ReplyToChat("Please enter the UID of the Symphony User to Lookup")

                table_body = ""
                table_header = "<table style='max-width:100%;table-layout:auto'><thead><tr style='background-color:#4D94FF;color:#ffffff;font-size:1rem' class=\"tempo-text-color--white tempo-bg-color--black\">" \
                               "<td style='max-width:20%'>ID</td>" \
                               "<td style='max-width:20%'>EMAIL ADDRESS</td>" \
                               "<td style='max-width:20%'>FIRST NAME</td>" \
                               "<td style='max-width:20%'>LAST NAME</td>" \
                               "<td style='max-width:20%'>DISPLAY NAME</td>" \
                               "<td style='max-width:20%'>TITLE</td>" \
                               "<td style='max-width:20%'>COMPANY</td>" \
                               "<td style='max-width:20%'>LOCATION</td>" \
                               "</tr></thead><tbody>"

                for index_org in range(len(d_org["users"])):
                    try:
                        firstName = d_org["users"][index_org]["firstName"]
                        lastName = d_org["users"][index_org]["lastName"]
                    except:
                        return messageDetail.ReplyToChat("I am a Top Secret Agent Bot, I do no share my info :)")
                    displayName = d_org["users"][index_org]["displayName"]
                    try:
                        title = d_org["users"][index_org]["title"]
                    except:
                        title = "N/A"
                    try:
                        #companyName = d_org["users"][index_org]["company"]
                        companyNameTemp = d_org["users"][index_org]["company"]
                        companyTemp = str(companyNameTemp).replace("&", "&amp;").replace("<", "&lt;").replace('"', "&quot;").replace("'", "&apos;").replace(">", "&gt;")
                        companyName = str(companyTemp)
                    except:
                        companyName = "N/A"
                    userID = str(d_org["users"][index_org]["id"])
                    try:
                        emailAddress = str(d_org["users"][index_org]["emailAddress"])
                    except:
                        emailAddress = "N/A"
                    try:
                        location = str(d_org["users"][index_org]["location"])
                    except:
                        location = "N/A"

                    table_body += "<tr>" \
                                  "<td>" + str(userID) + "</td>" \
                                  "<td>" + str(emailAddress) + "</td>" \
                                  "<td>" + str(firstName) + "</td>" \
                                  "<td>" + str(lastName) + "</td>" \
                                  "<td>" + str(displayName) + "</td>" \
                                  "<td>" + str(title) + "</td>" \
                                  "<td>" + str(companyName) + "</td>" \
                                  "<td>" + str(location) + "</td>" \
                                  "</tr>"

                    table_body += "</tbody></table>"

                reply = table_header + table_body
                #return messageDetail.ReplyToChatV2_noBotLog("<card iconSrc =\"https://thumb.ibb.co/csXBgU/Symphony2018_App_Icon_Mobile.png\" accent=\"tempo-bg-color--blue\"><header>User details</header><body>" + reply + "</body></card>")
                return messageDetail.ReplyToChatV2_noBotLog("<card iconSrc =\"\" accent=\"tempo-bg-color--blue\"><header>User details</header><body>" + reply + "</body></card>")

            # else:
        #     return messageDetail.ReplyToChat("You aren't authorised to use this command.")
            except:
                botlog.LogSymphonyInfo("UIDCheck did not work")
    except:
        try:
            botlog.LogSymphonyInfo("Inside second try for UIDCheck")
            try:
                UID_raw = messageDetail.Command.MessageText
                UID = str(UID_raw).replace(" ", "")
                #UID_lenght = len(str(UID))
            except:
                return messageDetail.ReplyToChat("Please use enter UID of the Symphony user to lookup")

            # # if str(UID_lenght) != "14":
            # if str(UID_lenght) != _configDef['UID']:
            #     return messageDetail.ReplyToChat("Please enter a valid UID, with " + _configDef['UID'] + " digits")

            connComp = http.client.HTTPSConnection(_configDef['symphonyinfo']['pod_hostname'])
            sessionTok = callout.GetSessionToken()

            headersCompany = {
                'sessiontoken': sessionTok,
                'cache-control': "no-cache"
            }

            connComp.request("GET", "/pod/v3/users?uid=" + UID + "&local=false", headers=headersCompany)

            try:
                resComp = connComp.getresponse()
                dataComp = resComp.read()
                data_raw = str(dataComp.decode('utf-8'))
                # data_dict = ast.literal_eval(data_raw)
                data_dict = json.loads(str(data_raw))

                dataRender = json.dumps(data_dict, indent=2)
                d_org = json.loads(dataRender)
            except:
                return messageDetail.ReplyToChat("Please enter a valid UID")

            notValidUI = "{'code': 400, 'message': 'At least one query paramemer (uid or email) needs to be present.'}"
            notValidUID = "{'code': 400, 'message': 'All uids are invalid.'}"

            if str(d_org).startswith(notValidUI):
                return messageDetail.ReplyToChat("Please enter the UID of the Symphony User to Lookup")
            if str(d_org).startswith(notValidUID):
                return messageDetail.ReplyToChat("Please enter the UID of the Symphony User to Lookup")

            table_body = ""
            table_header = "<table style='max-width:100%;table-layout:auto'><thead><tr style='background-color:#4D94FF;color:#ffffff;font-size:1rem' class=\"tempo-text-color--white tempo-bg-color--black\">" \
                           "<td style='max-width:20%'>ID</td>" \
                           "<td style='max-width:20%'>EMAIL ADDRESS</td>" \
                           "<td style='max-width:20%'>FIRST NAME</td>" \
                           "<td style='max-width:20%'>LAST NAME</td>" \
                           "<td style='max-width:20%'>DISPLAY NAME</td>" \
                           "<td style='max-width:20%'>TITLE</td>" \
                           "<td style='max-width:20%'>COMPANY</td>" \
                           "<td style='max-width:20%'>LOCATION</td>" \
                           "</tr></thead><tbody>"

            for index_org in range(len(d_org["users"])):
                try:
                    firstName = d_org["users"][index_org]["firstName"]
                    lastName = d_org["users"][index_org]["lastName"]
                except:
                    return messageDetail.ReplyToChat("I am a Top Secret Agent Bot, I do no share my info :)")
                displayName = d_org["users"][index_org]["displayName"]
                try:
                    title = d_org["users"][index_org]["title"]
                except:
                    title = "N/A"
                try:
                    #companyName = d_org["users"][index_org]["company"]
                    companyNameTemp = d_org["users"][index_org]["company"]
                    companyTemp = str(companyNameTemp).replace("&", "&amp;").replace("<", "&lt;").replace('"', "&quot;").replace("'", "&apos;").replace(">", "&gt;")
                    companyName = str(companyTemp)
                except:
                    companyName = "N/A"
                userID = str(d_org["users"][index_org]["id"])
                try:
                    emailAddress = str(d_org["users"][index_org]["emailAddress"])
                except:
                    emailAddress = "N/A"
                try:
                    location = str(d_org["users"][index_org]["location"])
                except:
                    location = "N/A"

                table_body += "<tr>" \
                              "<td>" + str(userID) + "</td>" \
                              "<td>" + str(emailAddress) + "</td>" \
                              "<td>" + str(firstName) + "</td>" \
                              "<td>" + str(lastName) + "</td>" \
                              "<td>" + str(displayName) + "</td>" \
                              "<td>" + str(title) + "</td>" \
                              "<td>" + str(companyName) + "</td>" \
                              "<td>" + str(location) + "</td>" \
                              "</tr>"

                table_body += "</tbody></table>"

            reply = table_header + table_body
            #return messageDetail.ReplyToChatV2_noBotLog("<card iconSrc =\"https://thumb.ibb.co/csXBgU/Symphony2018_App_Icon_Mobile.png\" accent=\"tempo-bg-color--blue\"><header>User details</header><body>" + reply + "</body></card>")
            return messageDetail.ReplyToChatV2_noBotLog("<card iconSrc =\"\" accent=\"tempo-bg-color--blue\"><header>User details</header><body>" + reply + "</body></card>")

        # else:
        #     return messageDetail.ReplyToChat("You aren't authorised to use this command.")
        except:
            botlog.LogSymphonyInfo("UIDCheck did not work entirely")


#########################
#
# def addTask(messageDetail):
#
#     try:
#
#         botlog.LogSymphonyInfo("Bot Call: Add Task")
#
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
#             #data_dict = ast.literal_eval(data_raw)
#             data_dict = json.loads(str(data_raw))
#
#             dataRender = json.dumps(data_dict, indent=2)
#             d_org = json.loads(dataRender)
#
#             for index_org in range(len(d_org["users"])):
#                 firstName = d_org["users"][index_org]["firstName"]
#                 lastName = d_org["users"][index_org]["lastName"]
#                 displayName = d_org["users"][index_org]["displayName"]
#                 #companyName = d_org["users"][index_org]["company"]
#                 companyNameTemp = d_org["users"][index_org]["company"]
#                 companyTemp = str(companyNameTemp).replace("&", "&amp;").replace("<", "&lt;").replace('"', "&quot;").replace("'", "&apos;").replace(">", "&gt;")
#                 companyName = str(companyTemp)
#                 userID = str(d_org["users"][index_org]["id"])
#
#                 botlog.LogSymphonyInfo(str(firstName) + " " + str(lastName) + " from Company/Pod name: " + str(companyName) + " with UID: " + str(userID))
#                 callerCheck = (str(firstName) + " " + str(lastName) + " - " + str(displayName) + " - " + str(companyName) + " - " + str(userID))
#         except:
#             try:
#                 botlog.LogSystemInfo("Inside Second try for user check")
#                 commandCallerUID = messageDetail.FromUserId
#
#                 connComp = http.client.HTTPSConnection(_configDef['symphonyinfo']['pod_hostname'])
#                 sessionTok = callout.GetSessionToken()
#
#                 headersCompany = {
#                     'sessiontoken': sessionTok,
#                     'cache-control': "no-cache"
#                 }
#
#                 connComp.request("GET", "/pod/v3/users?uid=" + commandCallerUID, headers=headersCompany)
#
#                 resComp = connComp.getresponse()
#                 dataComp = resComp.read()
#                 data_raw = str(dataComp.decode('utf-8'))
#                 #data_dict = ast.literal_eval(data_raw)
#                 data_dict = json.loads(str(data_raw))
#
#                 dataRender = json.dumps(data_dict, indent=2)
#                 d_org = json.loads(dataRender)
#
#                 for index_org in range(len(d_org["users"])):
#                     firstName = d_org["users"][index_org]["firstName"]
#                     lastName = d_org["users"][index_org]["lastName"]
#                     displayName = d_org["users"][index_org]["displayName"]
#                     #companyName = d_org["users"][index_org]["company"]
#                     companyNameTemp = d_org["users"][index_org]["company"]
#                     companyTemp = str(companyNameTemp).replace("&", "&amp;").replace("<", "&lt;").replace('"', "&quot;").replace("'", "&apos;").replace(">", "&gt;")
#                     companyName = str(companyTemp)
#                     userID = str(d_org["users"][index_org]["id"])
#
#                     botlog.LogSymphonyInfo(str(firstName) + " " + str(lastName) + " from Company/Pod name: " + str(companyName) + " with UID: " + str(userID))
#                     callerCheck = (str(firstName) + " " + str(lastName) + " - " + str(displayName) + " - " + str(companyName) + " - " + str(userID))
#             except:
#                 return messageDetail.ReplyToChat("Cannot validate user access")
#
#         if callerCheck in AccessFile:
#
#             try:
#                 #message = (messageDetail.Command.MessageText)
#                 message_raw = (messageDetail.Command.MessageFlattened)
#                 message = str(message_raw).replace("/addtask ", "").replace("/addTask ", "")
#                 #print(str(message))
#                 info = message.split("|")
#                 #print(str(info))
#                 orgTask = str(info[0]).strip()
#                 streamTask = str(info[1][1:]).replace("+", "-").replace("/", "_").replace("=", "")
#                 weekDayTask = str(info[2][1:])
#                 hourTask = str(info[3][1:])
#                 minTask = str(info[4][1:])
#
#                 #AcronymsDictionary.update({acronym.upper(): str(answer)})
#                 Tasker.update({orgTask.upper(): str(streamTask) + ": " + str(weekDayTask) + ": " + str(hourTask) + ": " + str(minTask)})
#                 sortTask(messageDetail)
#
#                 weekday = ""
#                 if int(weekDayTask) == 0:
#                     weekday = "Monday"
#                 elif int(weekDayTask) == 1:
#                     weekday = "Tuesday"
#                 elif int(weekDayTask) == 2:
#                     weekday = "Wednesday"
#                 elif int(weekDayTask) == 3:
#                     weekday = "Thursday"
#                 elif int(weekDayTask) == 4:
#                     weekday = "Friday"
#                 elif int(weekDayTask) == 5:
#                     weekday = "Saturday"
#                 elif int(weekDayTask) == 6:
#                     weekday = "Sunday"
#
#                 return messageDetail.ReplyToChatV2("<b>" + orgTask.upper() + "</b> task was successfully added to the Scheduler as <b>" + orgTask.upper() + " room with streamID: " + streamTask + " on every " + str(weekday) + " at " + hourTask + ":" + minTask + "</b>")
#
#             except:
#                 return messageDetail.ReplyToChat("Invalid format, please use /addTask org | streamid | weekday | hour | min")
#         else:
#             return messageDetail.ReplyToChat("You aren't authorised to use this command.")
#     except:
#         botlog.LogSymphonyInfo("AddTask did not work entirely")
#
# def removeTask(messageDetail):
#
#     try:
#
#         botlog.LogSymphonyInfo("Bot Call: Remove Task")
#
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
#             #data_dict = ast.literal_eval(data_raw)
#             data_dict = json.loads(str(data_raw))
#
#             dataRender = json.dumps(data_dict, indent=2)
#             d_org = json.loads(dataRender)
#
#             for index_org in range(len(d_org["users"])):
#                 firstName = d_org["users"][index_org]["firstName"]
#                 lastName = d_org["users"][index_org]["lastName"]
#                 displayName = d_org["users"][index_org]["displayName"]
#                 #companyName = d_org["users"][index_org]["company"]
#                 companyNameTemp = d_org["users"][index_org]["company"]
#                 companyTemp = str(companyNameTemp).replace("&", "&amp;").replace("<", "&lt;").replace('"', "&quot;").replace("'", "&apos;").replace(">", "&gt;")
#                 companyName = str(companyTemp)
#                 userID = str(d_org["users"][index_org]["id"])
#
#                 botlog.LogSymphonyInfo(firstName + " " + lastName + " from Company/Pod name: " + str(companyName) + " with UID: " + str(userID))
#                 callerCheck = (firstName + " " + lastName + " - " + displayName + " - " + companyName + " - " + str(userID))
#
#         except:
#             return messageDetail.ReplyToChat("Cannot validate user access")
#
#         if callerCheck in AccessFile:
#
#             try:
#
#                 remTask = (messageDetail.Command.MessageText)[1:]
#
#                 del Tasker[remTask.upper()]
#
#                 updatedTasker = 'Tasker = ' + str(Tasker)
#
#                 #file = open("modules/command/dictionary.py", "w+")
#                 file = open("Data/tasker.py", "w+")
#                 file.write(updatedTasker)
#                 file.close()
#
#                 return messageDetail.ReplyToChat(remTask + " was successfully removed.")
#             except:
#                 return messageDetail.ReplyToChat(remTask + " was not found.")
#         # else:
#         #     return messageDetail.ReplyToChat("You aren't authorised to use this command.")
#     except:
#         botlog.LogSymphonyInfo("Remove Accronym did not work entirely")
#
# def findTask(messageDetail):
#
#     try:
#         botlog.LogSymphonyInfo("Bot Call: Find Task")
#
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
#             #data_dict = ast.literal_eval(data_raw)
#             data_dict = json.loads(str(data_raw))
#
#             dataRender = json.dumps(data_dict, indent=2)
#             d_org = json.loads(dataRender)
#
#             for index_org in range(len(d_org["users"])):
#                 firstName = d_org["users"][index_org]["firstName"]
#                 lastName = d_org["users"][index_org]["lastName"]
#                 displayName = d_org["users"][index_org]["displayName"]
#                 #companyName = d_org["users"][index_org]["company"]
#                 companyNameTemp = d_org["users"][index_org]["company"]
#                 companyTemp = str(companyNameTemp).replace("&", "&amp;").replace("<", "&lt;").replace('"', "&quot;").replace("'", "&apos;").replace(">", "&gt;")
#                 companyName = str(companyTemp)
#                 userID = str(d_org["users"][index_org]["id"])
#
#                 botlog.LogSymphonyInfo(
#                     firstName + " " + lastName + " from Company/Pod name: " + str(companyName) + " with UID: " + str(userID))
#                 callerCheck = (firstName + " " + lastName + " - " + displayName + " - " + companyName + " - " + str(userID))
#
#         except:
#             return messageDetail.ReplyToChat("Cannot validate user access")
#
#         if callerCheck in AccessFile:
#
#             try:
#                 findTask = str((messageDetail.Command.MessageText)[1:]).strip()
#
#                 return messageDetail.ReplyToChat(findTask.upper() + " - " + str(Tasker[findTask.upper()]).replace("\n  \n", "<br/><br/>").replace("\n", "<br/>").replace("\u200b",""))
#             except:
#                 return messageDetail.ReplyToChat("No result for " + str(findTask) + " found")
#         else:
#             return messageDetail.ReplyToChat("You aren't authorised to use this command.")
#     except:
#         botlog.LogSymphonyInfo("Find Accronym did not work entirely")
#
# def listAllTasks(messageDetail):
#
#     try:
#
#         botlog.LogSymphonyInfo("Bot Call: List All Task")
#
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
#             #data_dict = ast.literal_eval(data_raw)
#             data_dict = json.loads(str(data_raw))
#
#             dataRender = json.dumps(data_dict, indent=2)
#             d_org = json.loads(dataRender)
#
#             for index_org in range(len(d_org["users"])):
#                 firstName = d_org["users"][index_org]["firstName"]
#                 lastName = d_org["users"][index_org]["lastName"]
#                 displayName = d_org["users"][index_org]["displayName"]
#                 #companyName = d_org["users"][index_org]["company"]
#                 companyNameTemp = d_org["users"][index_org]["company"]
#                 companyTemp = str(companyNameTemp).replace("&", "&amp;").replace("<", "&lt;").replace('"', "&quot;").replace("'", "&apos;").replace(">", "&gt;")
#                 companyName = str(companyTemp)
#                 userID = str(d_org["users"][index_org]["id"])
#
#                 botlog.LogSymphonyInfo(
#                     firstName + " " + lastName + " from Company/Pod name: " + str(companyName) + " with UID: " + str(userID))
#                 callerCheck = (firstName + " " + lastName + " - " + displayName + " - " + companyName + " - " + str(userID))
#         except:
#             return messageDetail.ReplyToChat("Cannot validate user access")
#
#         if callerCheck in AccessFile:
#
#             try:
#                 sortTask(messageDetail)
#                 table_body = ""
#                 table_header = "<table style='max-width:100%'><thead><tr style='background-color:#4D94FF;color:#ffffff;font-size:1rem' class=\"tempo-text-color--white tempo-bg-color--black\">" \
#                                "<td style='max-width:10%'>Task(s) on Scheduler</td>" \
#                                "</tr></thead><tbody>"
#
#                 for task in Tasker:
#                     tasklist = task + " : " + str(Tasker[task])
#                     #print(tasklist)
#
#                     table_body += "<tr>" \
#                                   "<td><b>" + task + "</b> - " + str(Tasker[task]).replace("\n  \n", "<br/><br/>").replace("\n", "<br/>").replace("\u200b","") + "</td>" \
#                                   "</tr>"
#                 table_body += "</tbody></table>"
#
#                 reply = table_header + table_body
#                 #return messageDetail.ReplyToChatV2_noBotLog("<card iconSrc =\"https://thumb.ibb.co/csXBgU/Symphony2018_App_Icon_Mobile.png\" accent=\"tempo-bg-color--blue\"><header>Task List</header><body>" + reply + "</body></card>")
#                 return messageDetail.ReplyToChatV2_noBotLog("<card iconSrc =\"\" accent=\"tempo-bg-color--blue\"><header>Task List</header><body>" + reply + "</body></card>")
#
#             except:
#                 return messageDetail.ReplyToChat("Acronyms not found")
#         # else:
#         #     return messageDetail.ReplyToChat("You aren't authorised to use this command.")
#     except:
#         botlog.LogSymphonyInfo("List All Tasks did not work entirely")
#
# # def listAllTasksTask():
# #
# #     # global taskIndex
# #     # taskIndex = 0
# #
# #     for task in Tasker:
# #         print("Test inside tasker")
# #         #print(int(taskIndex))
# #         # print(task)
# #        #print(Tasker)
# #         tasklist = task + " : " + str(Tasker[task])
# #         tasklist_split = str(tasklist).split(":")
# #         #print(tasklist_split)
# #         # _configDef['searchOrgTicket']['org'] = tasklist_split[0]
# #         # print(str(_configDef['searchOrgTicket']['org']).strip())
# #         # _configDef['searchOrgTicket']['stream_id'] = tasklist_split[1]
# #         # print(str(_configDef['searchOrgTicket']['stream']).strip())
# #         # _configDef['searchOrgTicket']['weekday'] = tasklist_split[2]
# #         # print(str(_configDef['searchOrgTicket']['weekday']).strip())
# #         # _configDef['searchOrgTicket']['hour'] = tasklist_split[3]
# #         # print(str(_configDef['searchOrgTicket']['hour']).strip())
# #         # _configDef['searchOrgTicket']['min'] = tasklist_split[4]
# #         # print(str(_configDef['searchOrgTicket']['minute']).strip())
# #
# #         global searchOrgTicketorg
# #         searchOrgTicketorg = tasklist_split[0]
# #         #print(str(searchOrgTicketorg).strip())
# #         global searchOrgTicketstream_id
# #         searchOrgTicketstream_id = tasklist_split[1]
# #         #print(str(searchOrgTicketstream_id).strip())
# #         global searchOrgTicketweekday
# #         searchOrgTicketweekday = tasklist_split[2]
# #         #print(str(searchOrgTicketweekday).strip())
# #         global searchOrgTickethour
# #         searchOrgTickethour = tasklist_split[3]
# #         #print(str(searchOrgTickethour).strip())
# #         global searchOrgTicketmin
# #         searchOrgTicketmin = tasklist_split[4]
# #         #print(str(searchOrgTicketmin).strip())
# #
# #         # global searchOrgTicketorg
# #         # searchOrgTicketorg[taskIndex] = tasklist_split[0]
# #         # #print(str(searchOrgTicketorg).strip())
# #         # global searchOrgTicketstream_id
# #         # searchOrgTicketstream_id[taskIndex] = tasklist_split[1]
# #         # #print(str(searchOrgTicketstream_id).strip())
# #         # global searchOrgTicketweekday
# #         # searchOrgTicketweekday[taskIndex] = tasklist_split[2]
# #         # #print(str(searchOrgTicketweekday).strip())
# #         # global searchOrgTickethour
# #         # searchOrgTickethour[taskIndex] = tasklist_split[3]
# #         # #print(str(searchOrgTickethour).strip())
# #         # global searchOrgTicketmin
# #         # searchOrgTicketmin[taskIndex] = tasklist_split[4]
# #         # #print(str(searchOrgTicketmin).strip())
# #
# #         # taskIndex += 1
#
# def sortTask(messageDetail):
#
#     sortedTask = {}
#
#     for key in sorted(Tasker.keys()):
#
#         sortedTask.update({key : Tasker[key]})
#
#
#     updatedTask = 'Tasker = ' + str(sortedTask)
#     file = open("Data/tasker.py","w+")
#     file.write(updatedTask)
#     file.close()


def atMentionRoom(messageDetail):
    botlog.LogSymphonyInfo("##############################")
    botlog.LogSymphonyInfo("##############################")
    botlog.LogSymphonyInfo("Bot Call - @mention room Check")
    botlog.LogSymphonyInfo("##############################")

    try:
        commandCallerUID = messageDetail.FromUserId
        roomStreamID = messageDetail.StreamId
        print(str(roomStreamID))

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
        # data_dict = ast.literal_eval(data_raw)
        data_dict = json.loads(str(data_raw))

        dataRender = json.dumps(data_dict, indent=2)
        d_org = json.loads(dataRender)

        for index_org in range(len(d_org["users"])):
            firstName = str(d_org["users"][index_org]["firstName"])
            lastName = str(d_org["users"][index_org]["lastName"])
            displayName = str(d_org["users"][index_org]["displayName"])
            #companyName = d_org["users"][index_org]["company"]
            companyNameTemp = d_org["users"][index_org]["company"]
            companyTemp = str(companyNameTemp).replace("&", "&amp;").replace("<", "&lt;").replace('"', "&quot;").replace("'", "&apos;").replace(">", "&gt;")
            companyName = str(companyTemp)
            userID = str(d_org["users"][index_org]["id"])

            botlog.LogSymphonyInfo(str(firstName) + " " + str(lastName) + " from Company/Pod name: " + str(companyName) + " with UID: " + str(userID))
            callerCheck = (firstName + " " + lastName + " - " + displayName + " - " + companyName + " - " + str(userID))

    except:
        #return messageDetail.ReplyToChat("Cannot validate user access")
        return botlog.LogSymphonyInfo("Cannot validate user access")

    if callerCheck in (_configDef['AuthUser']['AdminList']):

        message = (messageDetail.Command.MessageText)

        conn = http.client.HTTPSConnection(_configDef['symphonyinfo']['pod_hostname'])

        headers = {
            #'sessiontoken': callout.GetSessionToken(),
            'sessiontoken':sessionTok,
            'cache-control': "no-cache"
        }

        conn.request("GET", "/pod/v1/admin/stream/" + str(roomStreamID) + "/membership/list", headers=headers)

        res = conn.getresponse()
        data_raw = res.read().decode("utf-8")

        data_dict = json.loads(str(data_raw))

        dataRender = json.dumps(data_dict, indent=2)
        userAccess = json.loads(dataRender)

        table_body = ""
        table_header = "<table style='border-collapse:collapse;border:2px solid black;table-layout:fixed;max-width:25%;box-shadow: 5px 5px'><thead><tr style='background-color:#4D94FF;color:#ffffff;font-size:1rem' class=\"tempo-text-color--white tempo-bg-color--black\">" \
                       "<td style='border:1px solid blue;border-bottom: double blue;width:60%;text-align:center'>DISPLAY NAME</td>" \
                       "<td style='border:1px solid blue;border-bottom: double blue;width:40%;text-align:center'>USER ID?</td>" \
                       "</tr></thead><tbody>"

        for index in range(len(userAccess["members"])):

            displayName = str(userAccess["members"][index]["user"]["displayName"])
            userId = str(userAccess["members"][index]["user"]["userId"])

            table_body += "<tr>" \
                          "<td style='border:1px solid black;text-align:center'>" + str(displayName) + "</td>" \
                          "<td style='border:1px solid black;text-align:center'>" + str(userId) + "</td>" \
                          "</tr>"

        table_body += "</tbody></table>"
        render = table_header + table_body

        return messageDetail.ReplyToChatV2_noBotLog(
            "<card iconSrc =\"https://thumb.ibb.co/csXBgU/Symphony2018_App_Icon_Mobile.png\" accent=\"tempo-bg-color--blue\"><header>Please find the result below</header><body>" + render + "</body></card>")


    else:
        #return messageDetail.ReplyToChat("You aren't authorised to use this command.")
        return botlog.LogSymphonyInfo("You aren't authorised to use this command.")