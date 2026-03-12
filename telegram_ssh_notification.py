#!/usr/bin/python3
import os
if os.environ.get('PAM_TYPE') != 'open_session':
    exit()
import json

bot_config = None
with open(f'/usr/local/bin/telegram_ssh_notification/bot_config.json', 'r') as file:
    bot_config = json.load(file)


user = os.getenv("PAM_USER", 'unkown')
ip = os.getenv("PAM_RHOST", 'unkown')

TOKEN = bot_config['TOKEN']
chat_id = bot_config['chat_id']
message = f'SSH Login by {user} from {ip}'
os.system(f'curl -X POST https://api.telegram.org/{TOKEN}/sendMessage -H \'Content-Type: application/json\' -d \'{{"chat_id": "{chat_id}", "text": "{message}"}}\' > /dev/null')