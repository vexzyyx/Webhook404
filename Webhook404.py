import requests
from time import sleep
import os

RED = '\033[91m'
GREEN = '\033[92m'
BLUE = '\033[94m'
WHITE = '\033[0m'

webhook = None

def prompt_webhook():
    os.system('cls')
    while True:
        print(f"{BLUE}~~Webhook 404~~{WHITE}\n")
        webhook_input = input(f"{BLUE}Enter a valid webhook:{WHITE} ")
        if validate_webhook(webhook_input):
            global webhook
            webhook = webhook_input
            print(f"{GREEN}Webhook found.{WHITE}")
            sleep(1)
            menu()
            return
        else:
            print(f"{RED}Invalid or not found webhook.{WHITE}")
            sleep(1.5)
            os.system('cls')

def validate_webhook(webhook_input):
    if webhook_input.startswith("https://discord.com/api/webhooks/"):
        response = requests.get(webhook_input)
        return response.status_code == 200
    return False

def print_data():
    global webhook
    os.system('cls')
    response = requests.get(webhook)
    
    if response.status_code == 200:
        data = response.json()
        
        useful_data = [
            f"\n{BLUE}Token:{WHITE} {data.get('token', 'N/A')}",
            f"{BLUE}Channel ID:{WHITE} {data.get('channel_id', 'N/A')}",
            f"{BLUE}Guild ID:{WHITE} {data.get('guild_id', 'N/A')}",
            f"{BLUE}Webhook Name:{WHITE} {data.get('name', 'N/A')}",
            f"{BLUE}Webhook Avatar:{WHITE} {data.get('avatar', 'N/A')}",
            f"{BLUE}User:{WHITE} {data.get('user', {}).get('username', 'N/A')}#{data.get('user', {}).get('discriminator', 'N/A')}",
            f"{BLUE}Created At:{WHITE} {data.get('created_at', 'N/A')}",
            f"{BLUE}Updated At:{WHITE} {data.get('updated_at', 'N/A')}",
            f"{BLUE}URL:{WHITE} {data.get('url', 'N/A')}",
            f"{BLUE}Source:{WHITE} {data.get('source', 'N/A')}"
        ]
        
        print("\n".join(useful_data))
    else:
        print(f"{RED}Failed to retrieve data. Status code: {response.status_code}{WHITE}")
    
    sleep(0.5)
    input(f"\n{BLUE}Press ENTER to go back...{WHITE}")
    menu()

def delete_hook():
    global webhook
    os.system('cls')
    print(f"\n{BLUE}Deleting webhook...{WHITE}")
    requests.delete(webhook)
    if not validate_webhook(webhook):
        input(f"{GREEN}Webhook deleted successfully.{WHITE}\n\n{BLUE}Press ENTER to go back to the menu...{WHITE}")
        webhook = None
        prompt_webhook()
    else:
        input(f"{RED}Sorry, webhook couldn't be deleted.{WHITE}\n{BLUE}Press ENTER to go back...{WHITE}")
        menu()

def message_hook():
    global webhook
    os.system('cls')
    message = None
    spoof_name = None
    msg_amount = 1
    
    while True:
        print(f"\n{BLUE}'/exit':{WHITE} return to menu.\n{BLUE}'/amount <number>':{WHITE} how often your message should be sent.\n{BLUE}'/spoof <name>':{WHITE} spoof the username.\n{BLUE}'/unspoof':{WHITE} revert back to default username.\n")
        print(f"{BLUE}Spoof:{WHITE} {spoof_name if spoof_name else 'default'} | {BLUE}Amount:{WHITE} {msg_amount}")
        message = input(f"{BLUE}Message: {WHITE}")
        
        if message.lower() == "/exit":
            menu()
            return
        elif message.lower().startswith("/amount "):
            msg_amount = set_message_amount(message)
        elif message.lower().startswith("/spoof "):
            spoof_name = set_spoof_name(message)
        elif message.lower().strip() == "/unspoof":
            spoof_name = None
        else:
            send_message(message, spoof_name, msg_amount)
        os.system('cls')

def set_message_amount(command):
    parts = command.split()
    if len(parts) == 2:
        try:
            amount = int(parts[1])
            if 1 <= amount <= 100:
                return amount
            else:
                print(f"{RED}Number must be between 1 and 100.{WHITE}")
                sleep(1)
        except ValueError:
            print(f"{RED}Invalid number after '/amount'.{WHITE}")
            sleep(1.5)
    else:
        print(f"{RED}Invalid format.{WHITE}")
        sleep(1)
    return 1

def set_spoof_name(command):
    parts = command.split()
    if len(parts) == 2 and parts[1].strip():
        spoof_name = parts[1]
        return spoof_name
    print(f"{RED}Invalid format or username can't be empty.{WHITE}")
    sleep(1)
    return None

def send_message(message, spoof_name, msg_amount):
    global webhook
    data = {"content": message}
    if spoof_name:
        data["username"] = spoof_name
    for _ in range(msg_amount):
        requests.post(webhook, json=data)
        if msg_amount > 1:
            print(f"{BLUE}{message}{WHITE}")

def delete_message():
    global webhook
    os.system('cls')
    while True:
        print(f"\n{WHITE}Leave blank to cancel.")
        message_id = input(f"{BLUE}Enter message ID:{WHITE} ")
        if not message_id.strip():
            menu()
            return
        if message_id.isdigit():
            url = f'{webhook}/messages/{message_id}'
            response = requests.delete(url)
            if response.status_code == 204:
                print(f"{GREEN}Successfully deleted message with ID '{message_id}'.{WHITE}")
                sleep(2)
                os.system('cls')
            else:
                print(f"{RED}Message couldn't be deleted. Make sure that the message you are trying to delete was sent by the hook itself.{WHITE}")
                sleep(4)
                os.system('cls')
        else:
            print(f"{RED}Invalid ID{WHITE}")
            sleep(1)
            os.system('cls')

def menu():
    global webhook
    while True:
        os.system('cls')
        print(f"\n{BLUE}Webhook url:{WHITE} \n{webhook}\n")
        print(f"{BLUE}[1]{WHITE} Data\n{BLUE}[2] {WHITE}Delete webhook{BLUE}\n[3] {WHITE}Send messages\n{BLUE}[4] {WHITE}Delete messages")
        option = input(f"{BLUE}Option: {WHITE}")
        if option in {"1", "2", "3", "4"}:
            if option == "1":
                print_data()
            elif option == "2":
                delete_hook()
            elif option == "3":
                message_hook()
            elif option == "4":
                delete_message()
            return
        print(f"{RED}'{option}' isn't a valid option. Pick a number from the menu instead.{WHITE}")
        sleep(2.5)

prompt_webhook()
