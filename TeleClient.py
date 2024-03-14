import time
from datetime import datetime, timedelta
from telethon import TelegramClient, events
import os.path

# Use your own values from my.telegram.org
api_id = 1168521
api_hash = ''
client = TelegramClient('anon', api_id, api_hash)
MyChat = -487653262

logFilePath = "pollutionLog.txt"
PollCycleTime_min = 30
small_delay = 3

# Pollution logger variables
districtListRequest = [
    "Поділ",        "Троєщина",         "Видубичі",         "Печерськ", 
    "Університет",  "Протасів Яр",      "Липки",            "Оболонь", 
    "Дарниця",      "Харківський мас.", "Лісовий мас.",     "Соцмісто", 
    "Осокорки",     "Нивки",            "Шулявка",          "Відрадний", 
    "Голосіїв",     "Лук’янівка",       "Позняки",          "Борщагівка", 
    "Солом’янка",   "Святошин",         "Воскресенка",      "Русанівка", 
    "Мінський мас.","Теремки",          "м. Вишневе",       "м. Ірпінь", 
    "м. Бориспіль", "м. Бровари",       "ВДНГ"
    ]
    
districtListResponse = [
    "Поділ",        "Троєщина",         "Видубичі",         "Печерськ", 
    "Університет",  "Протасів Яр",      "Липки",            "Оболонь", 
    "Дарниця",      "Харківський мас.", "Лісовий мас.",     "Соцмісто", 
    "Осокорки",     "Нивки",            "Шулявка",          "Відрадний", 
    "Голосіїв",     "Лук’янівка",       "Позняки",          "Борщагівка", 
    "Солом’янка",   "Святошин",         "Воскресенка",      "Русанівка", 
    "Мінський мас.","Теремки",          "Вишневе",          "Ірпінь", 
    "Бориспіль",    "Бровари",          "ВДНГ"
    ]
districtIterator = 0
logStr = ""


# Telethon update handler for new messages
@client.on(events.NewMessage(chats=MyChat))
async def normal_handler(event):
    await parseNewMessage(event)
 
# Start aquality bot 
async def startBot():
    await client.send_message(MyChat, '/start@aqualitybot')
    time.sleep(small_delay)
    
    
async def parseNewMessage(event):
    global districtIterator
    global logStr
    global logFile
    #print(event.message.text)
    # Parse response with:
    # Main menu
    if "Що цікавить" in event.message.text:
        time.sleep(small_delay)
        await client.send_message(MyChat, '\U0001F504 Змінити район', reply_to=event.message.id)
    # Select district menu
    elif "Вибери район" in event.message.text:   
        time.sleep(small_delay)
        await client.send_message(MyChat, districtListRequest[districtIterator], reply_to=event.message.id)
        # Fill dummy info to log string to replace it when answer will come
        logStr += 'Err\t'
    # Answer with pollution level for selected district
    elif districtListResponse[districtIterator] in event.message.text: 
            # Parse pollution level value
            pollutionLevel = [int(i) for i in event.message.text.split() if i.isdigit()]
            dummyInfoIndex = logStr.rfind("Err")
            logStr = logStr[:dummyInfoIndex] + str(pollutionLevel[0]) + '\t'  
            # Proceed to next district (increment iterator)
            districtIterator += 1  
            # We complited the whole list of districts
            if districtIterator >= int(len(districtListResponse)):
                # Reset district iterator
                districtIterator = 0
                # Write log
                logFile.write(logStr + '\n')
                print(logStr)
                logFile.close()
                # Count delay to wake up for next poll
                currTime = datetime.now()
                wakeUpTime = ceil_time(currTime, timedelta(minutes=PollCycleTime_min))
                    #print(str((wakeUpTime-currTime).seconds))
                # Write time stamp for next log entry
                logStr = str(wakeUpTime) + '\t'
                # Sleep until next poll                
                time.sleep((wakeUpTime-currTime).seconds)
                logFile = open(logFilePath, "a+", encoding='utf-8')
            


def ceil_time(currTime, timeDelta):
    return currTime + (datetime.min - currTime) % timeDelta
    

#Prepaire log-file
if os.path.isfile(logFilePath) == True:
    # File exists, just open it
    logFile = open(logFilePath, "a+", encoding='utf-8')
else:
    # There is no log file yet
    #Create one and fill header       
    logFile = open(logFilePath, "a+", encoding='utf-8')
    logFile.write('Timestamp\t')
    for district in districtListResponse:
        logFile.write(district +'\t')      
    logFile.write('\n')


logStr = str(datetime.now())+'\t'
# Start client
client.start()
      
# Start aqualityBot
with client:
    client.loop.run_forever()

#Run untill complition (forever?)
#client.run_until_disconnected()

"""
    for i in range(0):
        
       # Get last message:
        async for message in client.iter_messages('test', 1):
            pass
       # Select Change district menu
        await client.send_message(-487653262, '\U0001F504 Змінити район', reply_to=message.id)      
        time.sleep(small_delay) 
       # Get last message: 
        async for message in client.iter_messages('test', 1):
            pass  
        
        # Get timestamp for all measurements
        timestamp = message.date
        logFile.write('\n'+str(timestamp)+'\t')
        # For loop through all districts
        for district in districtList:
           # Select district
            await client.send_message(-487653262, district, reply_to=message.id)
            time.sleep(small_delay)

            # Get previous to last message (dirty-dirty stuff)
            i = 0;
            async for message in client.iter_messages('test', 2):
                if i == 0:
                    i += 1
                    continue
                parsedDistrict = message.text.split(':')[0]
                pollutionLevel = [int(i) for i in message.text.split() if i.isdigit()]
                if parsedDistrict == district:
                    logFile.write(str(pollutionLevel[0])+'\t')
                    #print(str(timestamp)+'\t- '+district+'\t- '+str(pollutionLevel[0]))
                else:
                    logFile.write('Error\t')
                    print(str(timestamp)+'\t- '+district+'\t- Error')
                
            
           # Select Change district menu
            await client.send_message(-487653262, '\U0001F504 Змінити район', reply_to=message.id+1)       
            time.sleep(small_delay) 
           # Get last message: 
            async for message in client.iter_messages('test', 1):
                pass  
     
        
        time.sleep(600)
"""
   # Get last message: 
  #  async for message in client.iter_messages('test', 1):
   #     pass  
   # Select district
    #await client.send_message(-487653262, 'Видубичі', reply_to=message.id)

   
    # print all chats name
    #async for dialog in client.iter_dialogs():
    #    print(dialog.title)
   
   # You can print the message history of any chat:
   # async for message in client.iter_messages('test'):
   #    print(message.id, message.text)


    
