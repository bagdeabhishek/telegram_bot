from telegram.ext import Updater
import os
import logging
from telegram.ext import CommandHandler
import requests
NGROK_URL = "http://127.0.0.1:4040/api/tunnels"
PUBLIC_URL_SUCCCESS_MESSAGE = "The public urls are \n ---------------------- \n{0}"
PUBLIC_URL_FAILURE_MESSAGE = "The server isn't running currently! Ping @bagdeabhishek"
def get_public_urls():
    response = requests.get(NGROK_URL)
    try:
        if response.status_code != 200:
            return None
        public_urls = []
        response = response.json()
        for tunnel in response.get('tunnels'):
            public_urls.append(tunnel.get('name')+ " : " + tunnel.get('public_url'))
        return public_urls
    except Exception:
        logging.error("Exception occured", exc_info=True)
        return None
def url(update, context):
    urls = get_public_urls()
    if urls:
        public_urls_string = "\n".join(urls)
        context.bot.send_message(chat_id=update.effective_chat.id, text=PUBLIC_URL_SUCCCESS_MESSAGE.format(public_urls_string))
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=PUBLIC_URL_FAILURE_MESSAGE)
logging.basicConfig(filename='bot.log', filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
token = os.getenv("BOT_TOKEN")
updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher
start_handler = CommandHandler('url', url)
dispatcher.add_handler(start_handler)
updater.start_polling()