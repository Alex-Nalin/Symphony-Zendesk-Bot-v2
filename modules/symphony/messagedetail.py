from typing import List
import re
from bs4 import BeautifulSoup

import modules.symphony.messaging as msg
import modules.symphony.tokenizer as tokenizer

import modules.botlog as log


class ResponseType:
    IM, MIM, ROOM = range(3)


class MessageDetail:
    def __init__(self, respItem):
        self.MessageId = msg.FormatSymphonyId(respItem.id) if hasattr(respItem, 'id') else '-1'
        #self.MessageId = msg.FormatSymphonyId(respItem.messageId) if hasattr(respItem, 'messageId') else '-1'
        # I REALLY don't like the idea of EAFP. Sometimes it's just better to check things first
        # instead of just throwing an exception like a big 'ol tantrum.
        self.FromUserId = str(respItem.fromUserId) if hasattr(respItem, 'fromUserId') else '-1'
        #self.FromUserId = str(respItem.initiator.user.userId) if hasattr(respItem, 'initiator') else '-1'
        self.StreamId = msg.FormatSymphonyId(respItem.streamId) if hasattr(respItem, 'streamId') else '-1'
        #self.StreamId = msg.FormatSymphonyId(respItem.payload.messageSent.message.stream.streamId) if hasattr(respItem, 'payload') else '-1'
        #self.externalRecipients = str(respItem.payload.messageSent.message.externalRecipients) if hasattr(respItem, 'payload') else '-1'
        # Some of the message types (like room additions) have no message
        self.MessageRaw = respItem.message if hasattr(respItem, 'message') else None
        # if hasattr(respItem, 'payload'):
        #     test = str(respItem.payload.messageSent.message.message)
        #     soup = BeautifulSoup(test, "lxml")
        #     for hit in soup.findAll('div'):
        #         hit = hit.text.strip()
        #         hit = hit.replace('<', '&lt;')
        #     # test = re.search("(?<=<p>)(.*?)(?=</p>)", test, flags=re.IGNORECASE).group(0)
        #     hit = "<messageML>" + hit + "</messageML>"
        #     self.MessageRaw = hit
        # else: None
        self.Type = respItem.v2messageType if hasattr(respItem, 'v2messageType') else ''

        self.Attachments = self.ParseAttachments(respItem)
        # respItem.attachments if hasattr(respItem, 'attachments') else []

        self.IsValid = self.Type == 'V2Message'
        #self.IsValid = self.Type == 'MESSAGESENT'
        self.Sender = None
        self.ChatRoom = None
        self.Command = None

        if len(self.Attachments) > 0:
            log.LogConsoleInfo(respItem)

    def ParseAttachments(self, respItem):
        attachList = []

        if hasattr(respItem, 'attachments'):
            for att in respItem.attachments:
                attJ = {"id": att.id, "name": att.name, "size": att.size}
                attachList.append(attJ)

        return attachList

    def InitiateCommandParsing(self):
        if self.MessageRaw is not None:
            if self.MessageRaw.startswith('<message'):
                self.Command = tokenizer.CommandParser(self.MessageRaw, True)
            else:
                log.LogSymphonyError('Invalid MessageML: ' + self.MessageRaw)
                self.IsValid = False

    def GetConsoleLogLine(self):
        # Python's ternary conditional is a stupid order just to be different
        lineout = 'User: ' + self.Sender.Name if self.Sender is not None else 'Unknown'
        lineout += ' (' + self.FromUserId + ') - '

        if self.ChatRoom is not None:
            lineout += '<' + self.ChatRoom.Type + '> ' + self.ChatRoom.Name + ' (' + self.ChatRoom.StreamId + ')'
        else:
            lineout += '<Unknown Room> (' + self.StreamId + ')'

        return lineout

    def ReplyToChat(self, message: str):
        msg.SendSymphonyMessage(self.StreamId, message)

    def ReplyToChatAttachment(self, message: str, attach_data: str):
        msg.SendSymphonyMessageAttachment(self.StreamId, message, attach_data)

    def ReplyToChatV2(self, message: str, data=None):
        msg.SendSymphonyMessageV2(self.StreamId, message, data)

    def ReplyToChatV2_data(self, message: str, data=None, attachments=None):
        msg.SendSymphonyMessageV2_data(self.StreamId, message, data, attachments)

    def ReplyToChatV2_noBotLog(self, message: str, data=None):
        msg.SendSymphonyMessageV2_noBotLog(self.StreamId, message, data)

    def ReplyToSender(self, message: str):
        msg.SendUserIM([self.FromUserId], message)

    def ReplyToSenderv2(self, message: str, data=None):
        msg.SendUserIMv2([self.FromUserId], message, data)

    def ReplyToSenderv2_noBotLog(self, message: str, data=None):
        msg.SendUserIMv2_noBotLog([self.FromUserId], message, data)

    def NewIM(self, message: str, users: List[int]):
        msg.SendUserIM(users, message)

    def NewChat(self, message: str, streamId):
        msg.SendSymphonyMessage(streamId, message)