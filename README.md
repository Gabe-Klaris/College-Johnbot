Johnbot for college schedule<br />
Johnbot will never die, long live Johnbot!<br />
Currently johnbot its hosted on Oracle (#sponsored) and termius is used for ssh connectiong<br />
You can use any service for vm hosting and for ssh, but this will show you how to use these tools <br />
Required tools: github account and git, oracle account, termius account discord account and bot, pip and python downloaded on computer<br />
#Steps:

#Step 1: Download your school schedule and put in events if you have them.
Make sure you put these in a personal email

#Step 2: Clone this repo using git clone https://github.com/Tubby101/College-Johnbot

#Step 3: Fill in the variables in the newly downloaded bot.py 
This step takes multiple parts so it will be split up
#Step 3.1: Discord bot
First create an application at this link https://discord.com/developers/applications
Copy the discord token and store it as DISCORD_ID in your config vars
Go to "URL generator" under the OAuth2 tab and click on the "bot" tick mark, then copy the url at the bottom of the page, paste it in your browser and add the bot to your server
Also make sure to enable all the intents for the bot
In the server create a channel for the auto messages to go into, and copy the id of the channel by right clicking it, put that in the config vars with the key "channel_id"
Also copy the id of the server, and put that with "guild_id", you can also copy your own user id and put it with the key "DISCORD_ID" (this makes it so only you can access your schedule)
#Step 3.2: Calendar ids
First put the email address that you downloaded the schedule to 
