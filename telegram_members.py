#!/usr/bin/env python3

from telethon import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import os, json, sys

colors = {
    "re": "\u001b[31;1m",
    "gr": "\u001b[32m",
    "ye": "\u001b[33;1m",
}
re = "\u001b[31;1m"
gr = "\u001b[32m"
ye = "\u001b[33;1m"

def colorText(text):
    for color in colors:
        text = text.replace("[[" + color + "]]", colors[color])
    return text

clear = lambda:os.system('clear')
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

    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} [channel_name]")
        sys.exit()

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
        if i.title == sys.argv[1]:
            print(ye + "[+] Channel found")
            break
        a += 1
    opt = a
    print(ye+'[+] Fetching participants ...')
    target_group = channel[opt]
    all_participants = []
    mem_details = []
    all_participants = await client.get_participants(target_group)

    print(gr+ f'[+] Found {len(all_participants)} participants')
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
    
    try:
        with open("members.txt", "r") as f:
            old_members = json.load(f)
    except FileNotFoundError:
        old_members = []
    
    for mem in mem_details:
        if mem not in old_members:
            print(gr + "[+] New member detected: " + mem["firstname"] + " " + mem["lastname"])

    with open('members.txt', 'w') as w:
        json.dump(mem_details, w)
    print(gr+'[+] Members loaded successfully.')
    await client.disconnect()

with client:
    client.loop.run_until_complete(main())
