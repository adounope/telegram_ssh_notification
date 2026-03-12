import fileinput
import os
import json

pamd_ssh_script = '/etc/pam.d/sshd'
script_location = '/usr/local/bin/telegram_ssh_notification'
active_script = 'telegram_ssh_notification.py'
bot_config_file = 'bot_config.json'

def read_config():
    with open(bot_config_file, 'r') as f:
        return json.load(f)
def write_config(obj: dict):
    with open(bot_config_file, 'w') as f:
        json.dump(obj, f, indent=4)

tmp_file = 'bot_output.tmp'
def get_message(TOKEN):
    os.system(f'curl https://api.telegram.org/{TOKEN}/getUpdates > {tmp_file}')
    message = None
    with open(tmp_file, 'r') as file:
        message =  json.load(file)
    os.system(f'rm {tmp_file}')
    if not message['ok']:
        print('telegram error, check token')
        exit()
    return message

def send_message(TOKEN, chat_id, message):
    os.system(f'curl -X POST https://api.telegram.org/{TOKEN}/sendMessage -H \'Content-Type: application/json\' -d \'{{"chat_id": "{chat_id}", "text": "{message}"}}\' > /dev/null')



def unset_ssh_config():
    for line in fileinput.input(pamd_ssh_script, inplace=True):
        if "telegram_ssh_notification" not in line:
            print(line, end='')
    os.system(f'rm -r {script_location}')
def set_ssh_config():
    lines = []
    with open(pamd_ssh_script, 'r') as file:
        lines = file.readlines()
    print(lines)
    if lines[-1][-1] != '\n': # change line 
        with open(pamd_ssh_script, 'a') as file:
            file.write('\n')
    os.system(f'cat append_pamd_sshd_script.txt >> {pamd_ssh_script}')
    os.system(f'mkdir -p {script_location}')
    os.system(f'chmod 700 {active_script} {bot_config_file}')
    os.system(f'cp {bot_config_file} {script_location}')
    os.system(f'cp {active_script} {script_location}')