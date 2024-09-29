#!/bin/env python3
# (c) @AbirHasan2005
# Telegram Group: http://t.me/linux_repo
# Please give me credits if you use any codes from here.

import sys
import csv
import traceback
import time
import random
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest

api_id = 26792352   # Enter Your 7 Digit Telegram API ID.
api_hash = '4c1b674907450ca4f7b57d75b36f6b7c'  # Enter Your 32 Character API Hash
phone = '+9647516466395'  # Enter Your Mobile Number With Country Code.
client = TelegramClient(phone, api_id, api_hash)
SLEEP_TIME_1 = 100
SLEEP_TIME_2 = 100

async def main():
    await client.connect()
    if not await client.is_user_authorized():
        await client.send_code_request(phone)
        code = input('Enter the code you received: ')
        await client.sign_in(phone, code)

    # Ask for channel URL
    channel_url = input("Enter the Telegram channel URL: ")

    try:
        # Get channel entity using the provided URL
        target_channel = await client.get_entity(channel_url)
        print(f"Successfully identified the channel: {target_channel.title}")
    except Exception as e:
        print(f"Error fetching channel: {str(e)}")
        sys.exit("Invalid URL or access denied.")

    users = []
    with open(r"members.csv", encoding='UTF-8') as f:  # Enter your file name
        rows = csv.reader(f, delimiter=",", lineterminator="\n")
        next(rows, None)  # Skip the header row
        for row in rows:
            user = {
                'username': row[0],
                'id': int(row[1]),
                'access_hash': int(row[2]),
                'name': row[3],
            }
            users.append(user)

    mode = int(input("Enter 1 to add by username or 2 to add by ID: "))

    n = 0

    for user in users:
        n += 1
        if n % 80 == 0:
            print(f"Sleeping for {SLEEP_TIME_1} seconds ...")
            time.sleep(SLEEP_TIME_1)

        try:
            print(f"Adding {user['id']}")
            if mode == 1:
                if user['username'] == "":
                    print("No username, skipping...")
                    continue
                user_to_add = await client.get_input_entity(user['username'])
            elif mode == 2:
                user_to_add = InputPeerUser(user['id'], user['access_hash'])
            else:
                print("Invalid mode selected. Exiting...")
                sys.exit()

            await client(InviteToChannelRequest(target_channel, [user_to_add]))
            print("Waiting for 60-180 seconds ...")
            time.sleep(random.randrange(60, 180))

        except PeerFloodError:
            print("Getting Flood Error from Telegram. Script is stopping now. Please try again after some time.")
            print(f"Waiting {SLEEP_TIME_2} seconds")
            time.sleep(SLEEP_TIME_2)
            break
        except UserPrivacyRestrictedError:
            print("The user's privacy settings do not allow you to do this. Skipping...")
            time.sleep(random.randrange(0, 5))
        except Exception as e:
            traceback.print_exc()
            print(f"Unexpected error: {str(e)}")
            continue

with client:
    client.loop.run_until_complete(main())