import discord
import re
import time
import asyncio
from discordBotToken import Key
client = discord.Client()

@client.event
async def on_ready():
    print('Bot is ready')


atList = {}

# a list of users who cannot kill bots
# use discriminator
botinators = [2584,5475]

# propegate out @'s to channels
async def sendAt():
    
    global atList
    TIMEOUT = 60

    await client.wait_until_ready()
    while not client.is_closed():
        try:
            for chan,users in atList.items():
                for user in users:
                    await chan.send(f"Hey {user} ")
            await asyncio.sleep(TIMEOUT)

        # like all bad hangovers, sleep errors out
        except Exception as e:
            print(str(e))
            await asyncio.sleep(TIMEOUT)

@client.event
async def on_message(message):
    global atList
    global botinators
     #guild = client.get_guild(235114936529846272) #greg sex monkies
    print(f"{message.channel}:{message.author}: {message.author.name}: {message.content}")

    if "kill the bot" == message.content.lower() and message.author.discriminator not in botinators:
        await message.channel.send("You bastard")
        await client.close()

    if "kill the bot" == message.content.lower() and int(message.author.discriminator) in botinators:
        await message.channel.send("Bots cant kill bots!")

    if "pls senpai stop" in message.content.lower():
        await remove_user(message.author, client)

    pattern = r"[<]{1}[@]{1}[!&]{1}[0-9]+[>]{1}"
        
    users = re.findall(pattern,message.content)

    if len(users)>0 and "where is" in message.content.lower():

        # add atted users
        for user in users:

            #choose what channel to add to
            if atList.get(message.channel,False):

                #dont add users twice
                if user not in atList[message.channel]:
                    atList[message.channel].append(user)
            else: 
                atList[message.channel] = [user]

async def remove_user(author, client):

    global atList

    print("roles:", author.roles)

    for role in author.roles:
        for chan,users in atList.items():
            newusers = users
            for user in users:
                remove = False
                
                print('role:',role.id,' | user:',user)
                if str(role.id) in user:
                    newusers.remove(user)
                    remove = True
                
                print('role:',author.id,' | user:',user)
                if str(author.id) in user:
                    newusers.remove(user)
                    remove = True

                if remove:
                    await chan.send(f"Very well {user} I accept your submission")

            users = newusers


   
client.loop.create_task(sendAt())

#use your own token here
client.run(Key.value)