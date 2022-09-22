#!/usr/bin/env python3.10
from __future__ import print_function
from email import message
from re import A
import discord
import random
import os
import requests
from discord.ext import commands
import datetime
import os.path
import time
import asyncio
import pytz
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='.', description = "Hi :)", intents = intents)
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
WHEN = datetime.time(16, 31, 0)  # 6:00 PM
tz = pytz.timezone('US/Eastern')
channel_id = int(os.environ['channel_id'])
guild_id = int(os.environ['guild_id'])
#defining out of discord bot for use in functions

def main(response,arg):
        
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    creds_json = os.environ['GOOGLE_APPLICATION_CREDENTIALS']
    alright = json.loads(creds_json)
    creds = Credentials.from_authorized_user_info(alright,SCOPES)
    


    try:
        service = build('calendar', 'v3', credentials=creds)

    #uses arg supplied with command to get schedule to specified day
        print(response)
        if response == "no" or response == "invalid input":
            return response
        advance = 0
        if arg == 'today':
            advance = 0
        elif arg == "tomorrow":
            advance = 1
        elif arg.isdigit() == True:
            advance = int(arg)
        #sets day and day end for specified day to get events on that day
        day = datetime.datetime.now(datetime.timezone.utc).astimezone()
        day = day.replace(hour=0, minute=0, second=0, microsecond=0)
        day = day + datetime.timedelta(days=advance)
        dayend = day.replace(hour=23, minute=59, second=59, microsecond=0)
        day = day.isoformat()
        dayend = dayend.isoformat()
        now = datetime.datetime.now(datetime.timezone.utc).astimezone()
        #checking if user who gave the command is intended user
        #getting events
        events_result = service.events().list(calendarId=os.environ['calendar_email'], timeMin=day,
                                            timeMax = dayend, singleEvents=True,
                                            orderBy='startTime').execute()
        events_result1 = service.events().list(calendarId=os.environ['schedule_id'], timeMin=day,
                                            timeMax = dayend, singleEvents=True,
                                            orderBy='startTime').execute()
        #setting end of day for to only get free time within school day  
        endOfDay = now.replace(hour=15, minute=15, second=0)
        endOfDay = endOfDay + datetime.timedelta(days=advance)
        #function that sorts the events to give result
        def dayschedule(event_result,event_result1,response,dayend):
            events = events_result.get('items', [])
            events1 = events_result1.get('items', [])
            if not events and not events1:
                response += 'free all day, go watch some anime\n'
                return response
            dayend = datetime.datetime.strftime(dayend,'%Y-%m-%d %H:%M:%S')
            dayend = datetime.datetime.strptime(dayend,'%Y-%m-%d %H:%M:%S')
            #grabs start and end time for all events
            for event in events1:
                start = event['start'].get('dateTime', event['start'].get('date'))
                end = event['end'].get('dateTime', event['end'].get('date'))
                start = start.replace("T", " ")
                start = start[:-6]
                start = datetime.datetime.strptime(start,'%Y-%m-%d %H:%M:%S')
                end = end.replace("T", " ")
                end = end[:-6]
                end = datetime.datetime.strptime(end,'%Y-%m-%d %H:%M:%S')
                class_event = "You have class " + event['summary'] + " at " + datetime.datetime.strftime(start,"%I:%M") + "-" + datetime.datetime.strftime(end,"%I:%M %p") + "\n"
                response += str(class_event)
            #gets free time and adds to response
            
            #gets other events and adds to calendar
            for event in events:
                print(event)
                start = event['start'].get('dateTime', event['start'].get('date'))
                print(start)
                end = event['end'].get('dateTime', event['end'].get('date'))
                if "T" in start and start != end:
                    start = start.replace("T", " ")
                    start = start[:-6]
                    start = datetime.datetime.strptime(start,'%Y-%m-%d %H:%M:%S')
                    end = end.replace("T", " ")
                    end = end[:-6]
                    end = datetime.datetime.strptime(end,'%Y-%m-%d %H:%M:%S')
                    calendar_events = "You have an event " + event['summary'] + " at " + datetime.datetime.strftime(start,"%I:%M") + "-" + datetime.datetime.strftime(end,"%I:%M %p") + "\n"
                    response += str(calendar_events)
                #for all day events
                else:
                    response = "**" + event['summary'] + "**" + "\n" + response
                    

            return response
        response = dayschedule(events_result,events_result1,response,endOfDay)
    except HttpError as error:
        print('An error occurred: %s' % error)
    print(response)
    return response
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="Colossal Cave Adventure"))
    
async def called_once_a_day():  # Fired every day
    print("lkshfds")
    await bot.wait_until_ready()  # Make sure your guild cache is ready so the channel can be found via get_channel
    channel = bot.get_guild(guild_id).get_channel(channel_id) # Note: It's more efficient to do bot.get_guild(guild_id).get_channel(channel_id) as there's less looping involved, but just get_channel still works fine
    print(channel)
    await channel.send(main("today's breakdown is:\n","today"))

async def background_task():
    now = datetime.datetime.now(tz)
    now = now.replace(tzinfo=None)
    print(now)
    if now.time() > WHEN:  # Make sure loop doesn't start after {WHEN} as then it will send immediately the first time as negative seconds will make the sleep yield instantly
        print("hello")
        tomorrow = datetime.datetime.combine(now.date() + datetime.timedelta(days=1), datetime.time(0))
        seconds = (tomorrow - now).total_seconds()  # Seconds until tomorrow (midnight)
        await asyncio.sleep(seconds)   # Sleep until tomorrow and then the loop will start 
    while True:
        now = datetime.datetime.now(tz)
        now = now.replace(tzinfo=None)
        target_time = datetime.datetime.combine(now.date(), WHEN)  
        seconds_until_target = (target_time - now).total_seconds()
        print(seconds_until_target)
        await asyncio.sleep(seconds_until_target)  # Sleep until we hit the target time
        await called_once_a_day()  # Call the helper function that sends the message
        tomorrow = datetime.datetime.combine(now.date() + datetime.timedelta(days=1), datetime.time(0))
        seconds = (tomorrow - now).total_seconds()  # Seconds until tomorrow (midnight)
        await asyncio.sleep(seconds)
            
            
@bot.command(name='quote',help = 'gives John quote')
async def quotes(ctx):
    John_quotes = [
    "So we do have class friday ya?", 
    "I don't think you understand what that is.", 
    "Can you go back to your error please." , 
    "Sara's actually getting worse at programming.", 
    "Do you have a program?", 
    "Can you get off pinterest and work on your program please.",
    "Most likely.", 
    "No!", 
    "Why don't you go lie under that table.", 
    "This would be better if it had legs.",
    "Making a text based rpg is kind of simple for you at this point.",
    "I would only consider teaching advanced physics if it were an emergency.",
    "What does that mean? tic tac?",
    "If you're doing loops and texts again, I will not be happy.",
    "Yeah I intentionally reformatted all these computers just to destory your golf program.",
    "The funny thing is I learned to write code by hand.",
    "Like maybe it's like really really trouble.",
    "I wonder if you can maybe like make the bottom layer disapear once in a while",
    "It has a little picture of a (hand motion). Have fun.",
    "Hey it's the string I've been looking for.",
    "Are you going to poison your computer science teacher so I can sub?"

    ]
    response = random.choice(John_quotes)
    await ctx.send(response)

@bot.command(name='schedule',help = 'coming soon to a John bot near you')
async def quotes(ctx,arg):
    username = str(ctx.message.author.id)
    response = ""
    arg = arg.lower()
    if username == os.environ['DISCORD_ID']:
        if arg == '0' or arg == "today":
            response = "today's breakdown is:\n"
        elif arg == '1' or arg == "tomorrow":
            response = "tomorrow's breakdown is:\n"
        elif arg.isdigit():
            day = datetime.datetime.now(datetime.timezone.utc).astimezone()
            day = day.replace(hour=0, minute=0, second=0, microsecond=0)
            day = day + datetime.timedelta(days=int(arg))
            response = "The breakdown on " +  datetime.datetime.strftime(day ,'%A') + ", " + datetime.datetime.strftime(day,'%m/%d') + ": \n"
        else:
            response = "invalid input"
    else:
        response = "no"
    if __name__ == '__main__':
        message = main(response,arg)
        await ctx.send(message)
#to update do git add . then git commit -m "message" then git push
async def main2():
    async with bot:
        bot.loop.create_task(background_task())
        await bot.start(os.environ['DISCORD_TOKEN'])
asyncio.run(main2())