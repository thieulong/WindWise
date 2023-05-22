import requests
import json

with open('/home/paul/WindWise/telegram_services.json') as file:
    telegram_services = json.load(file)

TOKEN = telegram_services['TOKEN']
client_id = telegram_services['client_id']

def send_notifications(client_list=client_id):
    with open("angles.txt", 'r') as file:
        lines = file.readlines()
    current_angle = int(lines[0].strip())
    new_angle = int(lines[1].strip())
    for client in range(len(client_list)):
        client_id = client_list[client]
        message = "[INFO] Windmill 1 has just changed its direction. From {}° to {}°.".format(current_angle, new_angle)
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={client_id}&text={message}"
        requests.get(url).json()

