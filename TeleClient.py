import time
from telethon import TelegramClient

# Use your own values from my.telegram.org
api_id = 1168521
api_hash = '9cc8ebf8df41a5a8d5e9c0b8dd9708fc'
client = TelegramClient('anon', api_id, api_hash)
small_delay = 5

# Pollution logger variables
districtList = ["Осокорки", "Позняки", "Оболонь"]

async def main():
    #Prepaire log-file
    logFile = open("polLog.txt", "a+", encoding='utf-8')
    
    # Fill log-file header
    logFile.write('Timestamp\t')
    for district in districtList:
        logFile.write(district +'\t')
    # Getting information about yourself
    #me = await client.get_me()

    for i in range(10):
        await client.send_message(-487653262, '/start@aqualitybot')
        time.sleep(small_delay)
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

    
with client:
    client.loop.run_until_complete(main())