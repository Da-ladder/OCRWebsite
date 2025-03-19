# chat/consumers.py
import json
import time # testing delay w/ async

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

# imports all databases
from .models import *


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"_trivia" # sets all user websockets to link together

        # Join room group
        print("room" + str(self.room_group_name))
        # print("User" + str(self.scope["user"])) # will show up as AnonymousUser if not logged in and their email otherwise
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"].strip()

        if (len(message) == 0):
            return # makes sure the message is not just spaces
    
        await self.post_comment(message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": message} # . is replaced with _ so chat.message calls chat_message
        )

    """ json list will be sent in this format:
     [ message - Message to be displayed in chat
     [Option 1 True/False, Option 2 True/False, - Question Answers
     Option 3 True/False, Option 4 True/False], - Question Answers
     Countdown? True/False, - gives the message to start countdown
     [Question, Option 1, Option 2, Option 3], - Array of Questions (OVERRIDES COUNTDOWN WHEN SENT)
     eliminated? True/False, ] - State of the user, if they are eliminated, answers will NOT be
                                 sent to the server.
    """
    # Receive message from room group
    # triggers for every connected websocket when ".group_send" is called
    async def chat_message(self, event):
        message = event["message"]
    
        # Send message to WebSocket - eliminated parameter is a one way switch so we send False as a default
        await self.send(text_data=json.dumps([message, [], False, [], False]))

    # Log user comments
    @database_sync_to_async
    def post_comment(self, commentText):
        # time.sleep(30) # delays by 30 sec (await waits for this function to complete)

        # TODO Anon users can still post, prevent this in future iterations!!!
        try:
            creator = Users.objects.get(email = self.scope["user"])
        except:
            # if there is no vaild user in the database, don't store it in the database
            return
        
        club_wrapper = Club.objects.get(name = "Trivia")
        # Logs comment in the latest post
        latest_post = LiveFeed.objects.filter(club=club_wrapper).latest('creationTime')

        Replies.objects.create(
        text = commentText,
        post = latest_post,
        edited = False,
        linkToOtherReply = False,
        creator = creator
        )
    
    # it will currently fetch from the db EVERY time it needs to check the answer,
    # improve this via using cache & redis later on
    @database_sync_to_async
    def checkAnswer(answer):
        club_wrapper = Club.objects.get(name = "Trivia")

        # Get the question list
        questionList = ClubData.objects.filter(club=club_wrapper).latest('creationTime')
        questionList = questionList.data()

        # get the current question that we are on
        curQnum = questionList[0]

        # answer*2+2 is the exact index we need to fetch the answer from to compare it to the user's answer
        # the if statement will evaluate to true if the answer is correct
        if (questionList[2][curQnum][answer*2+2]):
            return True
        else:
            # remove them from the "player list"
            pass
        
        pass


class AdminConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = f"_triviaAdmin" # sets all admin websockets to link together 'room_triviaAdmin'

        # print("User" + str(self.scope["user"])) # will show up as AnonymousUser if not logged in and their email otherwise
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        pass

    # Receive message from room group
    async def chat_message(self, event):
        pass
    
    # it will currently fetch from the db EVERY time it needs to check the answer,
    # improve this via using cache & redis later on
    @database_sync_to_async
    def startRound():
        pass