from telethon import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import (PeerFloodError, UserNotMutualContactError ,
                                          UserPrivacyRestrictedError, UserChannelsTooMuchError,
                                          UserBotError, InputUserDeactivatedError)
from telethon.tl.functions.channels import InviteToChannelRequest
import time, os, sys, json

COLORS = {
    "re": "\u001b[31;1m",
    "gr": "\u001b[32m",
    "ye": "\u001b[33;1m",
}
re = "\u001b[31;1m"
gr = "\u001b[32m"
ye = "\u001b[33;1m"

def colorText(text):
    for color in COLORS:
        text = text.replace("[[" + color + "]]", COLORS[color])
    return text

clear = lambda:os.system('clear')
telet = lambda :os.system('pip3 install -U telethon')
telet()
clear()

if os.path.isfile('getmem_log.txt'):
    with open('getmem_log.txt', 'r') as r:
        data = r.readlines()
    api_id = data[0]
    api_hash = data[1]

else:
    api_id = input('Enter api_id: ')
    api_hash = input('Enter api_hash: ')
    with open('getmem_log.txt', 'w') as a:
        a.write(api_id + '\n' + api_hash)

client = TelegramClient('anon', api_id, api_hash)

async def main():
    chats = []
    channel = []
    result = await client(GetDialogsRequest(
        offset_date=None,
        offset_id=0,
        offset_peer=InputPeerEmpty(),
        limit=200,
        hash=0
    ))
    chats.extend(result.chats)
    for a in chats:
        try:
            if True:
                channel.append(a)
        except:
            continue

    a = 0
    print('')
    for i in channel:
        if i.title == "CAS Diablerets - Last minute":
            print("Channel found")
            break
        a += 1
    opt = a
    print('')
    print(ye+'[+] Fetching Members...')
    time.sleep(1)
    target_group = channel[opt]
    all_participants = []
    mem_details = []
    all_participants = await client.get_participants(target_group)
    for user in all_participants:
        try:
            if user.username:
                username = user.username
            else:
                username = ""
            if user.first_name:
                firstname = user.first_name
            else:
                firstname = ""
            if user.last_name:
                lastname = user.last_name
            else:
                lastname = ""

            new_mem = {
                'uid': user.id,
                'username': username,
                'firstname': firstname,
                'lastname': lastname,
                'access_hash': user.access_hash
            }
            mem_details.append(new_mem)
        except ValueError:
            continue
        
    with open("members.txt", "r") as f:
        old_members = json.load(f)

    for mem in mem_details:
        if mem not in old_members:
            print(gr + "[+] New member detected: " + mem["firstname"] + " " + mem["lastname"])

    with open('members.txt', 'w') as w:
        json.dump(mem_details, w)
    time.sleep(1)
    print(ye+'Please wait.....')
    time.sleep(3)
    print(gr+'[+] Members loaded successfully.')
    await client.disconnect()

with client:
    client.loop.run_until_complete(main())
