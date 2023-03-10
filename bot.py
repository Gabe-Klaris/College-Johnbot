from __future__ import print_function
from email import message
import discord
import random
import os
from discord.ext import commands
import datetime
import os.path
import time
import asyncio
import json
import pytz
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from keys import Discord_Token,Discord_ID,guild_id,channel_id,calendar_email,schedule_id, classes_name, google_creds
#new add idk
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='.', description = "Hi :)", intents = intents)
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
WHEN = datetime.time(8, 0, 0)  # 8:00 AM
tz = pytz.timezone('US/Eastern')
#server you want to send daily message
guild_id = int(guild_id)
#channel you want to send message in
channel_id = int(channel_id)
#defining out of discord bot for use in functions
def dayschedule(events_result,events_result1, response,day):
    events = events_result.get('items', [])
    events1 = events_result1.get('items', [])
    #no events
    if not events and not events1:
        response += 'free all day, go watch some anime\n'
        return response
    #puts all events in a list
    event_list = []
    for event in events1:
        event_list.append(event)
    for event in events:
        event_list.append(event)
    start_list = []
    #gets a datetime variable for the time each event starts in the list and adds it to a list
    for i in range(0,len(event_list)):
        start = event_list[i]['start'].get('dateTime', event_list[i]['start'].get('date'))
        end = event_list[i]['end'].get('dateTime', event_list[i]['end'].get('date'))
        #checks if an event is an "all day" event 
        if "T" in start and start != end:
            start = start.replace("T", " ")
            start = start[:-6]
            print(start)
            start = datetime.datetime.strptime(start,'%Y-%m-%d %H:%M:%S')
            start_list.append(start)
        else:
            day = datetime.datetime.strftime(day,"%Y-%m-%d")
            if start == day:
                response += "**" + event_list[i]['summary'] + "**" + "\n"
            else:
                if len(event_list)==1:
                    response += 'free all day, go watch some anime\n'  
            event_list.pop(i)
    #sorts event_list by time
    #since the index value of the time in start_list and full event in event_list are the same, sorts both
    i = 0
    while i < len(event_list)-1:
        if start_list[i] > start_list[i+1]:
            temp = start_list[i]
            start_list[i] = start_list[i+1]
            start_list[i+1] = temp
            temp1 = event_list[i]
            event_list[i] = event_list[i+1]
            event_list[i+1] = temp1
            i = 0
        else:
            i += 1
    #gets ordered events in format to return

    for event in event_list:
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        start = start.replace("T", " ")
        start = start[:-6]
        start = datetime.datetime.strptime(start,'%Y-%m-%d %H:%M:%S')
        end = end.replace("T", " ")
        end = end[:-6]
        end = datetime.datetime.strptime(end,'%Y-%m-%d %H:%M:%S')
        #differentiate between classes (imported from school site) and events (created by me)
        if len(event['organizer']) <= 2:
            class_event = "You have an event  " + event['summary'] + " at " + datetime.datetime.strftime(start,"%I:%M") + "-" + datetime.datetime.strftime(end,"%I:%M %p") + "\n"
        elif event['organizer']['displayName'] == classes_name:
            class_event = "You have class " + event['summary'] + " at " + datetime.datetime.strftime(start,"%I:%M") + "-" + datetime.datetime.strftime(end,"%I:%M %p") + "\n"
        response += str(class_event)
    return response
def main(response,arg):
    creds_json = google_creds
    alright = json.loads(creds_json)
    creds = Credentials.from_authorized_user_info(alright,SCOPES)
    try:
        service = build('calendar', 'v3', credentials=creds)
    #uses arg supplied with command to get schedule to specified day
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
        day = datetime.datetime.now(tz)
        day = day.replace(hour=0, minute=0, second=0, microsecond=0)
        day = day + datetime.timedelta(days=advance)
        dayend = day.replace(hour=23, minute=59, second=59, microsecond=0)
        day1 = day
        day = day.isoformat()
        dayend = dayend.isoformat()
        events_result = service.events().list(calendar_email, timeMin=day,
                                            timeMax = dayend, singleEvents=True,
                                            orderBy='startTime').execute()
        events_result1 = service.events().list(schedule_id, timeMin=day,
                                            timeMax = dayend, singleEvents=True,
                                            orderBy='startTime').execute()
        #function that sorts the events to give result
        response = dayschedule(events_result,events_result1, response, day1)
    except HttpError as error:
        print('An error occurred: %s' % error)
    print(response)
    return response
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="Colossal Cave Adventure"))
    
async def called_once_a_day():  # Fired every day
    print("lkshfds")
    await bot.wait_until_ready() 
    channel = bot.get_guild(guild_id).get_channel(channel_id) 
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

@bot.command(name='schedule',help ="""Gets free time for a day in the future
 Usage: ".schedule x" where x is how manys in the future you want your free time for
  You can use today or tomorrow instead of 0 and 1 respectively.""")
async def quotes(ctx,arg):
    username = str(ctx.message.author.id)
    response = ""
    arg = arg.lower()
    #makes sure only you can use the command
    if username == Discord_ID:
        if arg == '0' or arg == "today":
            response = "today's breakdown is:\n"
        elif arg == '1' or arg == "tomorrow":
            response = "tomorrow's breakdown is:\n"
        elif arg.isdigit():
            day = datetime.datetime.now(tz)
            
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
        await bot.start(Discord_Token)
asyncio.run(main2())