# chat/consumers.py
import json
import time # testing delay w/ async

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from asgiref.sync import async_to_sync
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
        userOptPicked = int(text_data_json["optionSelected"])

        # if branch when 
        if (userOptPicked != -1):
            self.checkAnswer()

            return
        elif (len(message) == 0):
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
     [Question, Option 1, Option 2, Option 3, Option 4], - Array of Questions (OVERRIDES COUNTDOWN WHEN SENT)
     eliminated? True/False, ] - State of the user, if they are eliminated, answers will NOT be
                                 sent to the server.
    """
    # Receive message from room group
    # triggers for every connected websocket when ".group_send" is called
    async def chat_message(self, event):    
        message = event["message"]
    
        # Send message to WebSocket - eliminated parameter is a one way switch so we send False as a default
        await self.send(text_data=json.dumps([message, [], False, [], False]))

    async def start_countdown(self, event):
        await self.send(text_data=json.dumps(["", [], True, [], False]))

    async def send_questions(self, event):
        question = event["question"]
        opt1 = event["opt1"]
        opt2 = event["opt2"]
        opt3 = event["opt3"]
        opt4 = event["opt4"]
        await self.send(text_data=json.dumps(["", [], False, [question, opt1, opt2, opt3, opt4], False]))

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
    def checkAnswer(self, answer):
        club_wrapper = Club.objects.get(name = "Trivia")

        # Get the question list
        questionList = ClubData.objects.filter(club=club_wrapper).latest('creationTime')
        questionList = questionList.data

        # get the current question that we are on
        if (not questionList[1]):
            return False
        curQnum = questionList[0]
        

        # answer*2+2 is the exact index we need to fetch the answer from to compare it to the user's answer
        # the if statement will evaluate to true if the answer is correct
        if (questionList[2][curQnum][answer*2+2]):
            return True
        else:
            # remove them from the "player list"
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

    # Receive message from WebSocket dkdj
    async def receive(self, text_data):
        if (text_data == "START"):
            await self.startRound()
            
        sync_to_async(time.sleep(6))


    # Receive message from room group
    async def chat_message(self, event):
        pass

    @database_sync_to_async
    def startRound(self):
        club_wrapper = Club.objects.get(name = "Trivia")

        # Get the question list
        dBquestionList = ClubData.objects.filter(club=club_wrapper).latest('creationTime')
        questionList = json.loads(dBquestionList.data)

        # Abort if another round is in progress
        if (questionList[1]):
            print("Aborted round: round in progress!")
            return
        
        # locks down round
        # questionList[1] = True # blocks another round from starting
        dBquestionList.data = json.dumps(questionList)
        dBquestionList.save() 

        curQuest = questionList[0]
        
        # start countdown for all users
        print("Countdown Started")
        async_to_sync(self.channel_layer.group_send)(
            "_trivia", {"type": "start.countdown"} # . is replaced with _ so chat.message calls chat_message
        )
        
        # wait for countdown to end
        time.sleep(4)


        print("Current Question: " + str(curQuest))

        # get questions from the database to give to the user
        # index 2 is where the question list is and the other numbers are due to
        # dB storage being opt1, t/f ans, opt2, t/f ans...
        async_to_sync(self.channel_layer.group_send)(
            "_trivia", {"type": "send.questions", "question" : questionList[2][curQuest][0], 
                        "opt1" : questionList[2][curQuest][1],
                        "opt2" : questionList[2][curQuest][3],
                        "opt3" : questionList[2][curQuest][5],
                        "opt4" : questionList[2][curQuest][7]}
        )
        print("Questions and options given")


        # time.sleep(31) # 30 seconds to answer the question + some headroom

        # shut down ability to answer questions

        print("Round over")
