from os import path
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import os
from wordcloud import WordCloud, STOPWORDS, get_single_color_func
import random
import modules.botlog as botlog
import modules.symphony.messaging as msg
import mimetypes

def trendingword(messageDetail):
    botlog.LogSymphonyInfo("#########################")
    botlog.LogSymphonyInfo("Bot Call - Trending words")
    botlog.LogSymphonyInfo("#########################")

    #http://www.writewords.org.uk/word_count.asp
    d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()

    # Read the whole text.
    text = open(path.join(d, 'Data/wordcloud.py')).read()

    trendingword_mask = np.array(Image.open(path.join(d, "Data/SymphonyLogo.png")))

    stopwords = set(STOPWORDS)
    stopwords.add("said")

    wc = WordCloud(background_color="white", max_words=2000, mask=trendingword_mask,
                   stopwords=stopwords, contour_width=3, contour_color='steelblue')

    # generate word cloud
    wc.generate(text)

    # store to file
    wc.to_file(path.join(d, "Temp/Symphony.png"))

    # show
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")
    plt.figure()
    plt.imshow(trendingword_mask, cmap=plt.cm.gray, interpolation='bilinear')
    plt.axis("off")
    #plt.show()
    #plt.savefig('masked.png')

    ######################
    upload_raw = os.path.abspath("Temp/Symphony.png")
    f = open(upload_raw, 'rb')
    fdata = f.read()

    ctype, encoding = mimetypes.guess_type(upload_raw)
    att = ("Symphony.png", fdata, ctype)
    att_list = [att]

    message = "Trending Words"

    botlog.LogSymphonyInfo(messageDetail.MessageRaw)
    msg.SendSymphonyMessageV2_data(messageDetail.StreamId, message, None, att_list)
    ######################

def trendingwordbw(messageDetail):

    botlog.LogSymphonyInfo("#######################################")
    botlog.LogSymphonyInfo("Bot Call - Trending words Black & White")
    botlog.LogSymphonyInfo("#######################################")


    def grey_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
        return "hsl(0, 0%%, %d%%)" % random.randint(60, 100)

    # get data directory (using getcwd() is needed to support running example in generated IPython notebook)
    d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()

    # read the mask image taken from
    # http://www.stencilry.org/stencils/movies/star%20wars/storm-trooper.gif
    mask = np.array(Image.open(path.join(d, "Data/SymphonyLogoBW.png")))

    text = open(path.join(d, 'Data/wordcloud.py')).read()

    text = text.replace("HAN", "Han")

    stopwords = set(STOPWORDS)
    stopwords.add("said")

    wc = WordCloud(max_words=1000, mask=mask, stopwords=stopwords, margin=10,
                   random_state=1).generate(text)
    # store default colored image
    default_colors = wc.to_array()
    plt.title("Custom colors")
    plt.imshow(wc.recolor(color_func=grey_color_func, random_state=3),
               interpolation="bilinear")
    wc.to_file("Temp/SymphonyBW.png")
    plt.axis("off")
    plt.figure()
    plt.title("Default colors")
    plt.imshow(default_colors, interpolation="bilinear")
    plt.axis("off")
    #plt.show()
    #plt.savefig('Temp/SymphonyBW.png')

    ######################
    upload_raw = os.path.abspath("Temp/SymphonyBW.png")
    f = open(upload_raw, 'rb')
    fdata = f.read()

    ctype, encoding = mimetypes.guess_type(upload_raw)
    att = ("SymphonyBW.png", fdata, ctype)
    att_list = [att]

    message = "Trending Words"

    botlog.LogSymphonyInfo(messageDetail.MessageRaw)
    msg.SendSymphonyMessageV2_data(messageDetail.StreamId, message, None, att_list)
    ######################


def trendingwordGroupedColor(messageDetail):

    botlog.LogSymphonyInfo("########################################")
    botlog.LogSymphonyInfo("Bot Call - Trending words Grouped Colour")
    botlog.LogSymphonyInfo("########################################")

    class SimpleGroupedColorFunc(object):
        """Create a color function object which assigns EXACT colors
           to certain words based on the color to words mapping

           Parameters
           ----------
           color_to_words : dict(str -> list(str))
             A dictionary that maps a color to the list of words.

           default_color : str
             Color that will be assigned to a word that's not a member
             of any value from color_to_words.
        """

        def __init__(self, color_to_words, default_color):
            self.word_to_color = {word: color
                                  for (color, words) in color_to_words.items()
                                  for word in words}

            self.default_color = default_color

        def __call__(self, word, **kwargs):
            return self.word_to_color.get(word, self.default_color)


    class GroupedColorFunc(object):
        """Create a color function object which assigns DIFFERENT SHADES of
           specified colors to certain words based on the color to words mapping.

           Uses wordcloud.get_single_color_func

           Parameters
           ----------
           color_to_words : dict(str -> list(str))
             A dictionary that maps a color to the list of words.

           default_color : str
             Color that will be assigned to a word that's not a member
             of any value from color_to_words.
        """

        def __init__(self, color_to_words, default_color):
            self.color_func_to_words = [
                (get_single_color_func(color), set(words))
                for (color, words) in color_to_words.items()]

            self.default_color_func = get_single_color_func(default_color)

        def get_color_func(self, word):
            """Returns a single_color_func associated with the word"""
            try:
                color_func = next(
                    color_func for (color_func, words) in self.color_func_to_words
                    if word in words)
            except StopIteration:
                color_func = self.default_color_func

            return color_func

        def __call__(self, word, **kwargs):
            return self.get_color_func(word)(word, **kwargs)

    d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()
    text = open(path.join(d, 'Data/wordcloud.py')).read()

    # Since the text is small collocations are turned off and text is lower-cased
    wc = WordCloud(collocations=False).generate(text.lower())

    color_to_words = {
        # words below will be colored with a green single color function
        '#00ff00': ['zendesk', 'ticket', 'user', 'issue'],
        # will be colored with a red single color function
        'red': ['alice', 'mouse', 'bird']
    }

    # Words that are not in any of the color_to_words values
    # will be colored with a grey single color function
    default_color = 'grey'

    # Create a color function with single tone
    # grouped_color_func = SimpleGroupedColorFunc(color_to_words, default_color)

    # Create a color function with multiple tones
    grouped_color_func = GroupedColorFunc(color_to_words, default_color)

    # Apply our color function
    wc.recolor(color_func=grouped_color_func)

    # Plot
    plt.figure()
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    #plt.show()
    plt.savefig('Temp/SymphonyGC.png')

    ######################
    upload_raw = os.path.abspath("Temp/SymphonyGC.png")
    f = open(upload_raw, 'rb')
    fdata = f.read()

    ctype, encoding = mimetypes.guess_type(upload_raw)
    att = ("SymphonyGC.png", fdata, ctype)
    att_list = [att]

    message = "Trending Words"

    botlog.LogSymphonyInfo(messageDetail.MessageRaw)
    msg.SendSymphonyMessageV2_data(messageDetail.StreamId, message, None, att_list)
    ######################


#######################################################################################################################


from zdesk import Zendesk
import json
import os
import codecs
import modules.symphony.messaging as msg
import http.client
import requests
import base64
import re
import modules.botlog as botlog
import modules.symphony.callout as callout
import ast
from datetime import date, datetime, timedelta
from Data.access import AccessFile
from Data.zendesk_trend import ZendeskTrend

#Grab the config.json main parameters
_configPathdDefault = os.path.abspath('config.json')

with codecs.open(_configPathdDefault, 'r', 'utf-8-sig') as json_file:
    _configDef = json.load(json_file)

#Zendesk libary
testconfig = {
    'zdesk_email': _configDef['zdesk_config']['zdesk_email'],
    'zdesk_password': _configDef['zdesk_config']['zdesk_password'],
    'zdesk_url': _configDef['zdesk_config']['zdesk_url'],
    'zdesk_token': True
}
zendesk = Zendesk(**testconfig)

#Zendesk API call config/header
conn = http.client.HTTPSConnection(_configDef['zdesk_config']['zdesk_api'])

# Converting id by real value
## https://support.zendesk.com/hc/en-us/articles/115000510267-Authentication-for-API-requests
## Generate the base64 authorization:
## <emailaddress>/token:<Zendesk_API_Token>
headers = {
    'username': _configDef['zdesk_config']['zdesk_email'] + "/token",
    'password': _configDef['zdesk_config']['zdesk_password'],
    'authorization': _configDef['zdesk_config']['zdesk_auth'],
    'cache-control': "no-cache",
    'Content-Type': 'application/json',
    'zdesk_token': True
}

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


def ZDTodayTrend(messageDetail):
    botlog.LogSymphonyInfo("######################")
    botlog.LogSymphonyInfo("Bot Call: ZDTodayTrend")
    botlog.LogSymphonyInfo("######################")

    isAllowed = False
    render = ""
    table_header = ""
    table_bodyFull = ""
    allTicket = ""
    counter = True
    totTickets = 0
    todayMinusDays = 0
    commandCallerUID = messageDetail.FromUserId

    try:

        connComp.request("GET", "/pod/v3/users?uid=" + commandCallerUID, headers=headersCompany)

        resComp = connComp.getresponse()
        dataComp = resComp.read()
        data_raw = str(dataComp.decode('utf-8'))
        data_dict = ast.literal_eval(data_raw)

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

            ##############################
            try:
                emailAddress = d_org["users"][index_org]["emailAddress"]
                #print("User is connected: " + emailAddress)
                emailZendesk = emailAddress
                #print(emailZendesk)
                connectionRequired = False
                # isAllowed = True
            except:
                connectionRequired = True

            # if connectionRequired:

            data_lenght = len(dataComp)

            if data_lenght > 450:
                try:
                    #print("inside > 450")
                    query = "type:user " + emailAddress
                except:
                    query = "type:user " + firstName + " " + lastName
                #print(query)
            elif data_lenght < 450:
                try:
                    #print("inside < 450")
                    #query = "type:user " + emailAddress + " organization:" + companyName
                    query = "type:user " + emailAddress
                except:
                    #query = "type:user " + firstName + " " + lastName + " organization:" + companyName
                    query = "type:user " + firstName + " " + lastName
                #print(query)
            else:
                return messageDetail.ReplyToChat("No user information available")

            #print(query)
            results = zendesk.search(query=query)
            #print(results)

            if str(results).startswith(
                    "{'results': [], 'facets': None, 'next_page': None, 'previous_page': None, 'count': 0}"):
                return messageDetail.ReplyToChat(
                    "This user does not exist on Zendesk, the name is misspelled or does not belong to this organisation")
            elif str(results).startswith(
                    "{'results': [], 'facets': {'type': {'entry': 0, 'ticket': 0, 'organization': 0, 'user': 0, 'article': 0, 'group': 0}}, 'next_page': None, 'previous_page': None, 'count': 0}"):
                return messageDetail.ReplyToChat(
                    "This organisation/company does not exist in Zendesk or name is misspelled.")
            else:

                data = json.dumps(results, indent=2)
                d = json.loads(data)

                for index in range(len(d["results"])):
                    name = d["results"][index]["name"]
                    email = str(d["results"][index]["email"])
                    #print("EmailAddress from Zendesk: " + email)

                    role = str(d["results"][index]["role"])
                    botlog.LogSymphonyInfo("The calling user is a Zendesk " + role)

                    #if role == "Administrator" or role == "admin" or role == "Agent" or role == "agent":
                    if role == "Administrator" or role == "admin" or role == "Agent" or role == "agent":
                        isAllowed = True
                        botlog.LogSymphonyInfo("User is an " + role + " on Zendesk")
                    else:
                        isAllowed = False

                emailZendesk = email

            botlog.LogSymphonyInfo(firstName + " " + lastName + " (" + displayName + ") from Company/Pod name: " + str(companyName) + " with UID: " + str(userID))
            callerCheck = (firstName + " " + lastName + " - " + displayName + " - " + companyName + " - " + str(userID))
    except:
        try:
            botlog.LogSymphonyInfo("Inside second try for user check")
            connComp.request("GET", "/pod/v3/users?uid=" + commandCallerUID, headers=headersCompany)

            resComp = connComp.getresponse()
            dataComp = resComp.read()
            data_raw = str(dataComp.decode('utf-8'))
            data_dict = ast.literal_eval(data_raw)

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

                ##############################
                try:
                    emailAddress = d_org["users"][index_org]["emailAddress"]
                    #print("User is connected: " + emailAddress)
                    emailZendesk = emailAddress
                    #print(emailZendesk)
                    connectionRequired = False
                    # isAllowed = True
                except:
                    connectionRequired = True

                # if connectionRequired:

                data_lenght = len(dataComp)

                if data_lenght > 450:
                    try:
                        #print("inside > 450")
                        query = "type:user " + emailAddress
                    except:
                        query = "type:user " + firstName + " " + lastName
                    #print(query)
                elif data_lenght < 450:
                    try:
                        #print("inside < 450")
                        #query = "type:user " + emailAddress + " organization:" + companyName
                        query = "type:user " + emailAddress
                    except:
                        #query = "type:user " + firstName + " " + lastName + " organization:" + companyName
                        query = "type:user " + firstName + " " + lastName
                    #print(query)
                else:
                    return messageDetail.ReplyToChat("No user information available")

                #print(query)
                results = zendesk.search(query=query)
                #print(results)

                if str(results).startswith(
                        "{'results': [], 'facets': None, 'next_page': None, 'previous_page': None, 'count': 0}"):
                    return messageDetail.ReplyToChat(
                        "This user does not exist on Zendesk, the name is misspelled or does not belong to this organisation")
                elif str(results).startswith(
                        "{'results': [], 'facets': {'type': {'entry': 0, 'ticket': 0, 'organization': 0, 'user': 0, 'article': 0, 'group': 0}}, 'next_page': None, 'previous_page': None, 'count': 0}"):
                    return messageDetail.ReplyToChat(
                        "This organisation/company does not exist in Zendesk or name is misspelled.")
                else:

                    data = json.dumps(results, indent=2)
                    d = json.loads(data)

                    for index in range(len(d["results"])):
                        name = d["results"][index]["name"]
                        email = str(d["results"][index]["email"])
                        #print("EmailAddress from Zendesk: " + email)

                        role = str(d["results"][index]["role"])
                        botlog.LogSymphonyInfo("The calling user is a Zendesk " + role)

                        #if role == "Administrator" or role == "admin" or role == "Agent" or role == "agent":
                        if role == "Administrator" or role == "admin" or role == "Agent" or role == "agent":
                            isAllowed = True
                            botlog.LogSymphonyInfo("User is an " + role + " on Zendesk")
                        else:
                            isAllowed = False

                    emailZendesk = email

                botlog.LogSymphonyInfo(firstName + " " + lastName + " (" + displayName + ") from Company/Pod name: " + str(companyName) + " with UID: " + str(userID))
                callerCheck = (firstName + " " + lastName + " - " + displayName + " - " + companyName + " - " + str(userID))
        except:
            botlog.LogSymphonyInfo("There was a problem to verify the calling user")


    if callerCheck in AccessFile and isAllowed:
        botlog.LogSymphonyInfo("User is an " + role + " on Zendesk and an Agent or Admin with the bot")

        streamType = (messageDetail.ChatRoom.Type)
        #print(streamType)

        showRequest = (messageDetail.Command.MessageText)
        message_split = showRequest.split()

        try:
            todayMinusDays = message_split[0]
            todayTicket = int(todayMinusDays)
        except:
            todayTicket = 1
            #botlog.LogSystemInfo("Please use number of days to check back such as /today 1")

        # if int(todayMinusDays) > 5:
        #     return messageDetail.ReplyToChat("For optimal performance, please use 5 days or less in your query")

        ticketdate_raw = datetime.today() - timedelta(days=int(todayTicket))
        ticketdate = str(ticketdate_raw)[:-16]

        conn = http.client.HTTPSConnection(_configDef['zdesk_config']['zdesk_api'])

        headers = {
            'username': _configDef['zdesk_config']['zdesk_email'] + "/token",
            'password': _configDef['zdesk_config']['zdesk_password'],
            'authorization': _configDef['zdesk_config']['zdesk_auth'],
            'cache-control': "no-cache",
            'Content-Type': 'application/json',
        }

        conn.request("GET", "/api/v2/search?query=type%3Aticket%20created%3E" + str(ticketdate), headers=headers)

        res = conn.getresponse()
        data_raw = res.read()
        data = str(data_raw.decode('utf-8'))
        #data = remove_emoji(data_raw)
        reply = str(data)

        messageDetail.ReplyToChatV2("Trend Analysis for Ticket raised from " + ticketdate + " Please wait.")

        if str(reply).startswith("{\"results\":[],\"facets\":null,\"next_page\":null,\"previous_page\":null,\"count\":0}"):
            return messageDetail.ReplyToChatV2("No Zendesk ticket was created on " + ticketdate)

        data = json.dumps(reply, indent=2)
        data_dict = ast.literal_eval(data)
        d_tick = json.loads(data_dict)
        #print(d_tick)

        subject = ""
        description = ""
        comment = ""
        for index in range(len(d_tick["results"])):

            requestid = str(d_tick["results"][index]["id"])
            print(str(requestid))

            requestsubject_temps = str(d_tick["results"][index]["subject"])
            #requestsubject = str(requestsubject_temps).replace("&", "&amp;").replace("<", "&lt;").replace('"', "&quot;").replace("'", "&apos;").replace(">", "&gt;")
            requestsubject = str(requestsubject_temps).replace("?", "").replace("!", "").replace('"', "&quot;").replace("\"","").replace(",","").replace(".","").replace(";","")
            #print(str(requestsubject))
            requestdescription_temps = str(d_tick["results"][index]["description"])
            requestdescription = str(requestdescription_temps).replace("?", "").replace("!", "").replace('"', "&quot;").replace("\"","").replace("“","").replace("”","").replace(",","").replace(";","").replace("\n\n \n\n \n\n \n\n", "<br/><br/>").replace("\n\n \n\n \n\n", "<br/><br/>").replace("\n\n \n\n \n", "<br/><br/>").replace("\n\n \n\n", "<br/><br/>").replace("\n\n", "<br/><br/>").replace("\n", "<br/>").replace("<br/>", " ")
            #print(str(requestdescription))

            subject += str(requestsubject) + " "
            description += str(requestdescription) + " "

            ####################################

            url = _configDef['zdesk_config']['zdesk_url'] + "/api/v2/tickets/" + str(requestid) + "/comments?sort_order=desc"
            response = requests.request("GET", url, headers=headers)
            data = response.json()

            for result in data['comments']:
                body = str(result["body"]).replace("?", "").replace("!", "").replace("\"","").replace("“","").replace("”","").replace(",","").replace(";","").replace("\n\n \n\n \n\n \n\n", "<br/><br/>").replace("\n\n \n\n \n\n", "<br/><br/>").replace("\n\n \n\n \n", "<br/><br/>").replace("\n\n \n\n", "<br/><br/>").replace("\n\n", "<br/><br/>").replace("\n", "<br/>").replace("<br/>", " ")
                #print(str(body))
                comment += str(body) + " "
            ####################################

        # subject += str(requestsubject) + " "
        # description += str(requestdescription) + " "


        ZendeskTrend.append(subject.lower())
        ZendeskTrend.append(description.lower())
        ZendeskTrend.append(comment.lower())
        #updatedTrend = 'ZendeskTrend = ' + str(sorted(ZendeskTrend))
        updatedTrend = 'ZendeskTrend = ' + str(ZendeskTrend)
        file = open("Data/zendesk_trend.py", "w+", encoding="utf-8")
        #file = open("Data/zendesk_trend.py", "w+", errors='ignore')
        file.write(updatedTrend)
        #file.write(str(ZendeskTrend))
        file.close()

        #http://www.writewords.org.uk/word_count.asp
        d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()

        text = open(path.join(d, 'Data/zendesk_trend.py')).read()

        trendingword_mask = np.array(Image.open(path.join(d, "Data/SymphonyLogo.png")))

        stopwords = set(STOPWORDS)
        stopwords.add("&quot;")
        stopwords.add("https")
        stopwords.add("http")
        stopwords.add("email")
        stopwords.add("unsubscribe")
        stopwords.add("need")
        stopwords.add("receiving")
        stopwords.add("send")
        stopwords.add("using")
        stopwords.add("running")
        stopwords.add("mail")
        stopwords.add("hi")
        stopwords.add("quot")
        stopwords.add("kind")
        stopwords.add("regards")
        stopwords.add("quot")

        wc = WordCloud(background_color="white", max_words=2000, mask=trendingword_mask,
                       stopwords=stopwords, contour_width=3, contour_color='steelblue')

        # generate word cloud
        wc.generate(text)

        # store to file
        wc.to_file(path.join(d, "Temp/Zendesk_Trend.png"))

        # show
        plt.imshow(wc, interpolation='bilinear')
        plt.axis("off")
        plt.figure()
        plt.imshow(trendingword_mask, cmap=plt.cm.gray, interpolation='bilinear')
        plt.axis("off")
        #plt.show()
        #plt.savefig('masked.png')

        ######################
        upload_raw = os.path.abspath("Temp/Zendesk_Trend.png")
        f = open(upload_raw, 'rb')
        fdata = f.read()

        ctype, encoding = mimetypes.guess_type(upload_raw)
        att = ("Zendesk_Trend.png", fdata, ctype)
        att_list = [att]

        message = "Trending Words"

        botlog.LogSymphonyInfo(messageDetail.MessageRaw)
        msg.SendSymphonyMessageV2_data(messageDetail.StreamId, message, None, att_list)

        updatedTrend = 'ZendeskTrend = []'
        file = open("Data/zendesk_trend.py", "w", encoding="utf-8")
        file.write(updatedTrend)
        file.close()
        ######################