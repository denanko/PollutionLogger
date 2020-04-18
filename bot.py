#This script is independet of lib or python version (tested on python 2.7 and 3.5)

import telegram 
import sys
#token that can be generated talking with @BotFather on telegram
my_token = '1226990741:AAGyw_wYHCe7M7iQVfNV8tYmqFTGKQtgrxY'

def send(msg, chat_id, token=my_token):
	"""
	Send a mensage to a telegram user specified on chatId
	chat_id must be a number!
	"""
	bot = telegram.Bot(token=token)
	bot.sendMessage(chat_id=chat_id, text=msg)
    

sys.stdout.write("hello from Python %s\n" % (sys.version,)) 
send("test", -487653262)