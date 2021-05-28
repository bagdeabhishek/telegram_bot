# Ngrok Telegram bot
This bot works along with [Ngrok](https://ngrok.com/). Ngrok is a tool that is used to expose your local service to the internet. A simple use case would be a local web application you created that you want your friends to check out. 
The tool comes with a free version which is okay for private use but the major limitation is you cannot choose a submdomain for your end point. To solve this problem I've come up with a simple solution
## Solution
Ngrok provides an API to query the information from your system. What this bot does, is it queries the Ngrok API end point to get the the public URLs and returns the formatted output as a text message. You can add this bot to any telegram group so your friends can get the URL directly. 
## How to run this bot
1. Create a telegram bot following [this](https://core.telegram.org/bots) guide
2. Copy the access token, you'll require this token to respond to this bot.
3. Set this token as an Environment variable using command `export BOT_TOKEN="<access-token>"` command or just replace the variable with actual value on line 31
4. Once you set the access token run this python script using command similar to `python3 bot-telegram.py`
5. Now once this bot is accepting connections you can just type `/url` command to get a list of all the public URLs along with the tunnel name. 

<div align="center">
    <img src="ss.jpg" alt="drawing" width="400"/>
</div>
