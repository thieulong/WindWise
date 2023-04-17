import requests
import json

with open('/home/paul/Automated-Windmill/telegram_services.json') as file:
    telegram_services = json.load(file)

TOKEN = telegram_services['TOKEN']
client_id = telegram_services['client_id']

def send_notifications(client_list=client_id):
    for client in range(len(client_list)):
        client_id = client_list[client]
        message = "Test message!"
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={client_id}&text={message}"
        requests.get(url).json()
