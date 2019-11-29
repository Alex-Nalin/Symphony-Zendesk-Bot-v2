Bot written from the Symphony-Ares bot base.

# Symphony Zendesk Bot
A multi-function bot for use with the Symphony communications platform

Symphony Zendesk Bot is an example of a multi-function command and chat-bot for the Symphony communications platform. It was written using Python 3.5.

The main purpose of Symphony Zendesk Bot is to assist the Support team and other Symphony Teams with their daily work

These are the functions added for this to integrate to Zendesk Support Ticket Management:
* Search Org Ticket (`/ZDOrgTicket org <open/new/pending/solved/closed/unresolved/all> (optional)`) to get a list of Zendesk tickets for a given company and filtered by status, if needed.
* Search Ticket as requester (`/ZDUserTicket <open/new/pending/solved/closed/unresolved/all> (optional)`) to search for your own Zendesk ticket as a requester or (`/ZDUserTicket <open/new/pending/solved/closed/unresolved/all> @mention`) to search for a colleague's Zendesk ticket as requester by status.
* Search Ticket as assignee (`/ZDAssigneeTicket <open/new/pending/solved/closed/unresolved/all> (optional)`) to search for your own Zendesk ticket as an assignee/agent or (`/ZDAssigneeTicket <open/new/pending/solved/closed/unresolved/all> @mention`) to search for a colleague's Zendesk ticket as assignee by status.
* Search Ticket as CCed/contributor (`/ZDCCTicket <open/new/pending/solved/closed/unresolved/all> (optional)`) to search for your own Zendesk ticket as a CCed/contributor person or (`/ZDCCTicket <open/new/pending/solved/closed/unresolved/all> @mention`) to search for a colleague's Zendesk ticket as a CCed/contributor person by status.
* Search by KeyWord (`/ZDKeyWord KEYWORD`) to search Zendesk by a given keyword
* Show Zendesk Comments (`/ZDComments <ticket_id>`) will show the updates made to a ticket and its author. This will show attachments and their respective size
* Create Zendesk Ticket (`/ZDTicket subject| description`) as an agent and, this will use the agent as the ticket requester with default values.
* Create Zendesk Request (`/ZDRequest <@mention user>| <subject>| <description>`) by @mentioning a Symphony user, the bot will cross check the user on Zendesk and once validated, it will create a Zendesk ticket with the provided title and description of the issue/problem.
* Recent Zendesk ticket (`/ZDRecent`), this will show all the recent ticket the agents have reviewed.
* Search Zendesk User (`/ZDUser alex| Symphony`) will return all the users named Alex on the Symphony Zendesk account. (`/ZDUser alex nalin| symphony`) will return all users name Alex Nalin on the Symphony Zendesk account. If you want to get the full list of users on a given account use this method (`/user | symphony`) (to look for all users on the Symphony Zendesk account)
* Show Zendesk ticket by id  (`/ZDShow <ticketid>`) is a call to display a given Zendesk ticket by its ID.
* Search ticket open until today (`/ZDToday`) will show all the tickets raised today, you can also specify how many days back to go (`/ZDToday 3`) to get a bigger list of recently raised support issue from 3 days ago.
* Ticket Update (`/ZDUpdate <ticketID>| comment| status| public/private`) will allow the caller to add a public or private update to an existing Support Ticket.
* Assign Ticket (`ZDAssign` <ticketID> <@mention user>) will assign the Zendesk ticket to the @mentioned Zendesk Agent who is also a Symphony user.

* Add Access (`/ZDAccessAdd <@mention user(s)>`) to the list of authorised users to communicate with the Bot to execute commands. It will also sort the list when adding new user. This is an Admin restricted function
* Remove Access (`/ZDAccessRemove <@mention user>`) of the user to remove from the list of authorised users. This is an Admin restricted function
* List All Access (`/ZDAccessList`) as its function states, this will return all the authorised user list. This is an Admin restricted function
* Give a list of all the Bot Symphnony streams (`/ZDStream`) that exist with users, this include IM, MIM and ROOMs
* Send Bot message as blast (`/ZDBlast IM/ROOM/ALL <message>`) to IM/MIM/ROOMs where the bot is a member of to inform or an update or else.
* Create a Zendesk user (`/ZDCreateUser @mention`) by @mentioning the Symphony User, the user needs to be connected with the bot in order to do this a it requires the email address.
* Knowledge Base Article search (`/ZDKB <search query> `) will return the list of article with that text query

## Requirements

The bot was built using Pycharm on Windows 10 and runs against Python 3.8, though it likely will run against Python 2.7 with minor modifications. 

* Python 3.8 

    * requests - http://docs.python-requests.org/en/master/
    * lxml - http://lxml.de/
    * cryptography.io - https://cryptography.io/en/latest/
    * Redis - https://pypi.python.org/pypi/redis
    * RQ - http://python-rq.org/
    * requests-toolbelt
    * cryptography
    * rq
    * google-api-python-client
    * python-dateutil
    * pandas
    * zdesk
    * hurry.filesize
    * pdfkit
    * wkhtmltopdf
    * mimetypes
    * python-magic
    * python-magic-bin
    * python-jose
    * BeautifulSoup
    * bs4
    

* Redis 2.6.0 or better

    * https://redis.io/
    * Sample Docker config: https://github.com/sameersbn/docker-redis

* A Symphony bot account with client certificate files

    * Client certificates are generally provided as .p12 files. The code asks for .pem files in /certificates
    * You will need the certificate password to extract the .pem files
    * crt.pem: openssl pkcs12 -in path.p12 -out bot.crt.pem -clcerts -nokeys
    * key.pem: openssl pkcs12 -in path.p12 -out bot.key.pem -nocerts -nodes

* Access to your POD's REST endpoints

## Installation

You will need to install the following if you want to have the Help converted to PDF: https://github.com/JazzCore/python-pdfkit/wiki/Installing-wkhtmltopdf

Installation of the bot is somewhat manual today. 

1. Clone the repo to your local environment 

    * `git clone https://github.com/Alex-Nalin/Symphony-Zendesk-bot-v2`

2. Install and configure your Redis server. 
3. Create new config file by copying the *.sample.json to *.json (e.g. config.sample.json -> config.json)
4. Modify the main config files:

    * ./SymphonyZendeskBot/config.json - Contains general config details, including information about your Symphony configuration

5. Use access.sample.py to create -> `access.py` file and use dictionary.sample.py to create -> `dictionary.py`

## Starting the Bot

1. Ensure your Redis server is running
2. Start the Redis worker process

    * Open a new terminal session
    * Change to the bot folder, e.g. `cd /bots/symphony/SymphonyZendeskBotv2/`
    * Run the worker script: `python3 startWorker.py`

3. Start the bot

    * Open a new terminal session
    * Change to the bot folder
    * Run the bot script: `python3 startBot.py`

## Logging

SymphonyZendeskBot does not log messages, but will log other activity, including commands that are issued. Various logs can be found in ./SymphonyZendeskBot/logging


## Plugins

This initial python distribution includes a nascent framework for creating plugins for the bot. A plugin must contain several files:

* config.json - this file must be valid json and must contain a `"commands": []` array that will tell the plugin parser what commands you have provided for the users

    Each command must have the following attributes:

    * "triggers": [] -> An array of strings - each string will act as a command alias for this command

        E.g. "triggers": ["quote", "$", "qt"] => the /quote command will also trigger with /qt or /$

    * "function": FunctionName -> The method name in your commands.py that the triggers will execute
    * "description": [text] -> Description of your command. Returned with /[command] help
    * "helptext": [text] -> Help info for your command. Returned with /[command] help

* commands.py - Contains the method definitions specified in config.json
* __init__.py -> A blank file that python uses to correctly identify packages

Any additional files required for processing your command are ignored by the plugin parser
