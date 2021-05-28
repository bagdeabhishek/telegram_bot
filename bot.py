from telegram.ext import Updater
import os
import logging
from telegram.ext import CommandHandler
from github import Github
g = None
repo_name = None
page = "index.md"
def get_github_object(token):
    global g, repo_name
    g = Github(token)
    for repo in g.get_user().get_repos():
        if(repo.full_name.endswith(g.get_user().login+".github.io")):
            repo_name = repo.full_name
    if not repo_name:
        return "Did not find any github pages repo"
    else:
        return "Set up the Github repo, successfully!"
def setup_github(update,context):
    token= context.args[0]
    context.bot.send_message(chat_id=update.effective_chat.id, text=get_github_object(token))

def select_page(update,context):
    global page
    page_name_argument= context.args[0]
    if page_name_argument :
        page = page_name_argument
    
    context.bot.send_message(chat_id=update.effective_chat.id, text="Set page as "+page)

def update_page(update,context):
    repo = g.get_repo(repo_name)
    file = repo.get_contents(page)
    append_string = file.decoded_content.decode("utf-8")+ "\n" + " ".join(context.args)
    status = repo.update_file(file.path, "Updated by telegram bot", append_string,file.sha,branch="main")
    context.bot.send_message(chat_id=update.effective_chat.id, text="Updated the file \n "+status)



logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
token = os.getenv("BOT_TOKEN")
updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot Abhishek, please talk to me!")
start_handler = CommandHandler('start', start)
setup_github_handler = CommandHandler('setup', setup_github)
setup_set_page_handler = CommandHandler('setpage', select_page)
update_page_handler = CommandHandler('update', update_page)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(setup_github_handler)
dispatcher.add_handler(setup_set_page_handler)
dispatcher.add_handler(update_page_handler)
updater.start_polling()