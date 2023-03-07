Johnbot for college schedule<br />
Johnbot will never die, long live Johnbot!<br />
Currently johnbot its hosted on Oracle (#sponsored) and termius is used for ssh connectiong<br />
You can use any service for vm hosting and for ssh, but this will show you how to use these tools <br />
Required tools: github account and git, oracle account, termius account discord account and bot, pip and python downloaded on computer<br />
#Steps:<br />

#Step 1: Download your school schedule and put in events if you have them.
Make sure you put these in a personal email<br />

#Step 2: Clone this repo using git clone https://github.com/Tubby101/College-Johnbot<br />

#Step 3: Fill in the variables in the file keys.py <br />
This step takes multiple parts so it will be split up<br />
#Step 3.1: Discord bot<br />
First create an application at this link https://discord.com/developers/applications<br />
Copy the discord token and store it as Discord_Token in your config vars<br />
Go to "URL generator" under the OAuth2 tab and click on the "bot" tickmark, then copy the url at the bottom of the page, paste it in your browser and add the bot to your server<br />
Also make sure to enable all the intents for the bot<br />
In the server create a channel for the auto messages to go into, and copy the id of the channel by right clicking it, put that in the config vars with the key "channel_id"<br />
Also copy the id of the server, and put that with "guild_id", you can also copy your own user id and put it with the key "Discord_ID" (this makes it so only you can access your schedule)<br />
#Step 3.2: Calendar ids<br />
First put the email address that you downloaded the schedule to calendar_email<br />
Now go to your google calendar and on the left of your screen there should be a list of your calendars.<br />
Click on the three dots next to the name of your classes schedule(should be and go to settings.<br />
scroll down to "integrate calendar" and there should be a field named "Calendar ID", copy this field and save it with "schedule_id" in config vars.<br />
Also put the name of this calendar in the field named "Classes name". <br />
#Step 3.3: Token<br />
For the last step we need to generate the token to link to your calendar<br />
First download the google api library using this command in your terminal "pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib"<br />
Now run the quickstart.py file using the command "python quickstart.py"<br />
If either of these dont work, make sure you have everything installed correctly and you are in the folder with quickstart.py<br />
Log into the google account you saved the calendars on, and accept the authorization(basically you are using the connection to google calendar I set up instead of setting one up on your own, It doesn't give me access to anything).<br />
Once the authoirzation for the app is finished, the file "token.json" should have been created in the folder you ran quickstart.py in<br />
Copy the contents of the file into the key (including the brackets)<br />
#Step 4: Hosting<br />
Create an oracle account at https://www.oracle.com/ and create a VM instance<br />
What core or specs the VM doesn't really matter and I don't really understand but I use the VM.Standard.A1.Flex version with 4 cores and 24 gb of ram. <br />
Also be sure that the vm is run in linux/ubuntu operating system and that you download the ssh key<br />
Once the VM is up, go to terminus and paste the IP (public IP address in) and use the ssh key to connect to the vm<br />
Then run "Sudo apt update", and "Sudo apt install pip" on the vm<br />
Install the discord package "pip install discord" and google package "pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib" on the vm<br />
Run the program using "python3 bot.py" command and you should be all good<br />
*I am not the best at explaining hosting so if you run into any problems there are many videos explaining how to do it for other vms or ssh connecting things.*<br />
