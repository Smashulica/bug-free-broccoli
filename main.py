import os
import time
import datetime

import pyrogram

user_session_string = os.environ.get("user_session_string")
bots = [i.strip() for i in os.environ.get("bots").split(' ')]
bot_owner = os.environ.get("bot_owner")
update_channel = os.environ.get("update_channel")
status_message_id = int(os.environ.get("status_message_id"))
api_id = int(os.environ.get("api_id"))
api_hash = os.environ.get("api_hash")

user_client = pyrogram.Client(
    user_session_string, api_id=api_id, api_hash=api_hash)


def main():
    with user_client:
        while True:
            print("[INFO] starting to check uptime..")
            edit_text = f"**Our Bot's 🤖 Status 📈 :**\n(Updating Every 30 Minutes)\n\n"
            for bot in bots:
                print(f"[INFO] checking @{bot}")
                snt = user_client.send_message(bot, '/start')

                time.sleep(15)

                msg = user_client.get_history(bot, 1)[0]
                if snt.message_id == msg.message_id:
                    print(f"[WARNING] @{bot} is down")
                    edit_text += f"🤖 @{bot}\n📊 Status: `DOWN` ❌\n\n"
                    user_client.send_message(bot_owner,
                                             f"🤖 @{bot} is Down!")
                else:
                    print(f"[INFO] all good with @{bot}")
                    edit_text += f"🤖 @{bot} \n📊 Status: `UP` ✅\n\n"
                user_client.read_history(bot)

            utc_now = datetime.datetime.utcnow()
            ist_now = utc_now + datetime.timedelta(minutes=30, hours=5)

            edit_text += f"Last Checked ⏳ On :\n`{str(utc_now)} UTC`\n`{ist_now} IST`"

            user_client.edit_message_text(update_channel, status_message_id,
                                         edit_text)
            print(f"[INFO] everything done! sleeping for 30 mins...")

            time.sleep(30 * 60)


main()
