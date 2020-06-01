import sys
import requests
import pymsteams


WEBHOOK_URL = 'https://outlook.office.com/webhook/327044bc-8860-4705-a521-48cc9bfd264e@58005ddb-3d82-4718-9e75-ec5c71cca7ec/IncomingWebhook/ce255d45adfd4d94aa803a84e86e1d6f/4b94f775-45ba-4f8d-a767-252cb12f9726'

def send_message(message):

    # message = {}
    # message['taskid'] = taskid
    # message['taskstatus'] = taskstatus
    # message['taskresult'] = taskresult

    json_payload = {'text' : 'esto es un mensaje!' }

    response = requests.post(WEBHOOK_URL, data=json_payload) 
    result = response

    if response.status_code == 200:
        print('ok!')
    
    return response.text

def send_teams_message(message):

    # You must create the connectorcard object with the Microsoft Webhook URL
    myTeamsMessage = pymsteams.connectorcard(WEBHOOK_URL)

    # Add text to the message.
    myTeamsMessage.text(message)

    # send the message.
    myTeamsMessage.send()

if __name__ == '__main__':
    print(send_teams_message(sys.argv[1]))
