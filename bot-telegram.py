from telegram.ext import Updater
import os
import logging
from telegram.ext import CommandHandler
import requests
from git import Repo
from datetime import datetime
PATH_OF_GIT_REPO = r'/home/abhishek/universe/bagdeabhishek.github.io/'
COMMIT_MESSAGE = 'Committed URL at {0}'.format(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
NGROK_URL = "http://127.0.0.1:4040/api/tunnels"
PUBLIC_URL_SUCCCESS_MESSAGE = "The public urls are \n ---------------------- \n{0}"
PUBLIC_URL_FAILURE_MESSAGE = "The server isn't running currently! Ping @bagdeabhishek"
FILE_CONTENTS = "---\ntitle: {0}\nredirect_to: {1}\n---\n"
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

def change_redirect_file():
    try:
        public_urls = get_public_urls()
        repo = Repo(PATH_OF_GIT_REPO)
        for x in public_urls:
            tunnel_name = x.split(":")[0]
            url = x.split(" : ")[1]
            file_name = PATH_OF_GIT_REPO +tunnel_name.strip()+".md"
            with open(file_name,"w+") as f:
                file = FILE_CONTENTS.format(tunnel_name,url)
                f.write(file)
            repo.index.add([file_name])
        repo.index.commit(COMMIT_MESSAGE)
        origin = repo.remote(name='origin')
        origin.push()
    except Exception as e:
        logging.error("Exception occured", exc_info=True)

logging.basicConfig(filename='bot.log', filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
change_redirect_file() # Add redirection from github pages
token = os.getenv("BOT_TOKEN")
updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher
start_handler = CommandHandler('url', url)
dispatcher.add_handler(start_handler)
updater.start_polling()