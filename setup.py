import src.utils as utils

bot_config = utils.read_config()
TOKEN = bot_config['TOKEN']

def obtain_chat_id():
    username = input('input your username on telegram (eg: @name):')
    message = utils.get_message(TOKEN)
    if len(message['result']) == 0:
        print('send a message to the bot then restart this code')
        exit()
    for result in message['result']:
        if result['message']['from']['username'] == username:
            return result['message']['from']['id']
    print('send a message to the bot then restart this code')
    exit()

bot_config['chat_id'] = obtain_chat_id()
utils.write_config(bot_config)
print('done')