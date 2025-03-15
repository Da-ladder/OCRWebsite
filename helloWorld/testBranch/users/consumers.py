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
        self.room_group_name = f"_trivia" # sets all websockets to link together

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
        message = text_data_json["message"]
        await self.post_comment(message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": message} # . is replaced with _ so chat.message calls chat_message
        )

    # Receive message from room group
    # triggers for every connected websocket when ".group_send" is called
    async def chat_message(self, event):
        message = event["message"]
    
        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))

    # Recieve 

    
    @database_sync_to_async
    def post_comment(self, commentText):
        print(commentText)
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
