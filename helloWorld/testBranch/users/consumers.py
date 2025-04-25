# chat/consumers.py
import asyncio
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
        # print("room" + str(self.room_group_name))
        # print("User" + str(self.scope["user"].email)) # will show up as AnonymousUser if not logged in and their email otherwise
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

        # only allow users to "join the list" if we haven't started the first question
        club_wrapper = await Club.objects.aget(name = "Trivia")
        dBquestionList = await ClubData.objects.filter(club=club_wrapper).alatest('creationTime')
        questionList = json.loads(dBquestionList.data)

        userEmail = str(self.scope["user"].email)

        print(userEmail)

        if (questionList[0] == 0 and not questionList[1]):
            # check if user is on the list
            # 3 is player safe list (only added when they get a question right)
            # 4 is current player list
            # 5 is eliminated list
            if (userEmail in questionList[4]):
                # don't do anything bc they're already in
                pass
            elif (userEmail in questionList[5]):
                # tell the user that they are already elimed
                await self.elim_notice([userEmail])
            else:
                # they're not in so add them to the list
                questionList[4].append(userEmail)
                dBquestionList.data = json.dumps(questionList)
                await database_sync_to_async(dBquestionList.save)()
        else:
            # elim the user if we have already started. Let the users know & send them the question
            questionList[5].append(userEmail)
            dBquestionList.data = json.dumps(questionList)
            await database_sync_to_async(dBquestionList.save)()
            await self.elim_notice([userEmail])
            
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
            await self.checkAnswer(userOptPicked)
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

    async def elim_notice(self, emails, answers = ""):
        if (str(self.scope["user"].email) in emails):
            if (answers == ""):
                await self.send(text_data=json.dumps(["", [], False, [], True]))
            else:
                await self.send(text_data=json.dumps(["", [answers], False, [], True]))
        else:
            if (answers == ""):
                await self.send(text_data=json.dumps(["", [], False, [], False]))
            else:
                await self.send(text_data=json.dumps(["", [answers], False, [], False]))

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
    async def checkAnswer(self, answer):
        print("Answer passed to function")
        club_wrapper = await Club.objects.aget(name = "Trivia")

        # Get the question list
        questionList = await ClubData.objects.filter(club=club_wrapper).alatest('creationTime')
        questionData = json.loads(questionList.data)

        # get the current question that we are on
        # if (not questionList[1]):
            # return False

        curQnum = questionData[0]

        userEmail = str(self.scope["user"].email)
        

        # answer*2+2 is the exact index we need to fetch the answer from to compare it to the user's answer
        # the if statement will evaluate to true if the answer is correct
        if (questionData[2][curQnum][answer*2+2]):
            # move their email address to the "safe" list
            if (userEmail in questionList[4]):
                questionList[4].remove(userEmail)
                questionList[4].remove(userEmail)
                pass
            print("ur right")
            return True
        else:
            # move their email address to the "elim" list
            if (userEmail in questionList[4]):
                questionList[4].remove(userEmail)
                pass
            print("ur wrong")
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
        if (text_data == "START"):
            await self.startRound()


    # Receive message from room group
    async def chat_message(self, event):
        pass

    #@database_sync_to_async
    async def startRound(self):
        club_wrapper = await Club.objects.aget(name = "Trivia")

        # Get the question list
        dBquestionList = await ClubData.objects.filter(club=club_wrapper).alatest('creationTime')
        questionList = json.loads(dBquestionList.data)

        # Abort if another round is in progress
        if (questionList[1]):
            print("Aborted round: round in progress!")
            return
        
        # locks down round
        questionList[1] = True # blocks another round from starting
        dBquestionList.data = json.dumps(questionList)
        await database_sync_to_async(dBquestionList.save)()

        curQuest = questionList[0]
        
        # start countdown for all users
        print("Countdown Started")
        await self.channel_layer.group_send(
            "_trivia", {"type": "start.countdown"} # . is replaced with _ so chat.message calls chat_message
        )
        
        # wait for countdown to end
        await asyncio.sleep(4)


        print("Current Question: " + str(curQuest))

        # get questions from the database to give to the user
        # index 2 is where the question list is and the other numbers are due to
        # dB storage being opt1, t/f ans, opt2, t/f ans...
        await self.channel_layer.group_send(
            "_trivia", {"type": "send.questions", "question" : questionList[2][curQuest][0], 
                        "opt1" : questionList[2][curQuest][1],
                        "opt2" : questionList[2][curQuest][3],
                        "opt3" : questionList[2][curQuest][5],
                        "opt4" : questionList[2][curQuest][7]}
        )
        print("Questions and options given")


        await asyncio.sleep(31) # 30 seconds to answer the question + some headroom

        # shut down ability to answer questions
        questionList[1] = False
        questionList[0] += 1 # move on to the next question

        # merge list of ppl who have unanswered questions with eliminated cluster
        # list 5 is eliminated email addresses and list 4 is ppl who did not answer yet
        questionList[5].extend(questionList[4])

        # save changes
        dBquestionList.data = json.dumps(questionList)
        await database_sync_to_async(dBquestionList.save)()

        # group send status in game + questions and answers


        print("Round over")
