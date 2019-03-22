import time
import datetime
import botbuilder
import modules.botlog as botlog
import modules.command.commandhub as hub
import modules.symphony.datafeed as datafeed
import modules.plugins.commandloader as cmdloader
import modules.symphony.messaging as messaging
import modules.symphony.messagedetail as messageDetail
import os
import codecs
import json
import modules.plugins.Zendesk.commands as comm
import modules.command.defaultcommands as deff


#from Data.tasker import Tasker

#Grab the config.json main parameters
_configPathdDefault = os.path.abspath('config.json')

with codecs.open(_configPathdDefault, 'r', 'utf-8-sig') as json_file:
        _configDef = json.load(json_file)

loopCount = 0

def Main():
    global loopCount
    once = True

    botlog.LogSymphonyInfo('Starting Symphony Zendesk Bot session...')
    botSession = botbuilder.SymSession()

    # Bot Loop Begins here
    loopControl = botSession.StartBot()
    loopCount = 0

    # Pre-load the command definitions
    cmdloader.LoadAllCommands()

    #messaging.SendSymphonyMessage(_configDef['BotStreamForPing'], "Starting Bot session")

    while loopControl:

        messages = datafeed.PollDataFeed(botSession.DataFeedId)

        #For Tasker
        now = datetime.datetime.now()
        week = datetime.datetime.today().weekday()

        if messages is not None:

            if len(messages) == 0:
                # botlog.LogConsoleInfo('204 - No Content')
                # messaging.SendSymphonyMessage(_configDef['BotStreamForPing'], "Just a ping to keep the bot alive")
                pass

            for msg in messages:
                if msg.IsValid and msg.Sender.IsValidSender:
                    hub.ProcessCommand(msg)

            #################################


            now = datetime.datetime.now()
            ## Return the day of the week as an integer, where Monday is 0 and Sunday is 6.
            #week = datetime.datetime.today().weekday()

            #print(week)
            #print("###############################")
            #print(now.strftime("%Y-%m-%d %H:%M:%S"))

            #deff.listAllTasksTask()

            # for deff.task in Tasker:
            #
            #     tasklist = deff.task + " : " + str(Tasker[deff.task])
            #     tasklist_split = str(tasklist).split(":")
            #     #print(tasklist_split)
            #
            #     searchOrgTicketorg = tasklist_split[0]
            #     #print(str(searchOrgTicketorg).strip())
            #     searchOrgTicketstream_id = tasklist_split[1]
            #     #print(str(searchOrgTicketstream_id).strip())
            #     searchOrgTicketweekday = tasklist_split[2]
            #     #print(str(searchOrgTicketweekday).strip())
            #     searchOrgTickethour = tasklist_split[3]
            #     #print(str(searchOrgTickethour).strip())
            #     searchOrgTicketmin = tasklist_split[4]
            #     #print(str(searchOrgTicketmin).strip())

            ## Need to intent if used with tasker to be in side for loop
            if now.hour == int(_configDef['quoteOfTheDay']['hour']) and now.minute == int(_configDef['quoteOfTheDay']['minute']) and once:
                once = False
                deff.QoDTask()
                # messaging.SendSymphonyMessage(_configDef['quoteofthedayStream'], "Hello, test for QOD")

                ## TODO Scheduler to continue next stream when executed once

                # # if week == _configDef['searchOrgTicket']['weekday'] and now.hour == _configDef['searchOrgTicket']['hour'] and now.minute == _configDef['searchOrgTicket']['minute'] and once:
                # #     print("Inside")
                # #     once = False
                # #     comm.searchCompanyTicketsTask((_configDef['searchOrgTicket']['org']),(_configDef['searchOrgTicket']['stream']))
                #
                # if week == int(searchOrgTicketweekday) and now.hour == int(searchOrgTickethour) and now.minute == int(searchOrgTicketmin) and once:
                #     #print("Inside")
                #     #once = False
                #     comm.searchCompanyTicketsTask(str(searchOrgTicketorg),(str(searchOrgTicketstream_id)))


            if now.hour == 23:
                once = True
            #################################

        else:
            botlog.LogSymphonyInfo('Error detected reading datafeed. Invalidating session...')
            #messaging.SendSymphonyMessage(_configDef['BotStreamForPing'], "Error detected reading datafeed. Invalidating session...")
            botSession.InvalidateSession()
            loopControl = False

            loopControl = botSession.StartBot()


while loopCount < 10:
    try:
        Main()
    except SystemExit:
        loopCount = 99
        pass
    except Exception as ex:
        botlog.LogSystemError('Error: ' + str(ex))
        botlog.LogSymphonyError('Unhandled error, probably network difficulties at the Agent. Retrying in 5s.')
        #messaging.SendSymphonyMessage(_configDef['BotStreamForPing'],"There seems to be some network difficulties at the Agent. Please try again in 5s.")

        time.sleep(5)
        loopCount += 1