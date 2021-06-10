import requests
import json
from twilio.rest import Client

# Get env file with personal information
with open('env.json') as env_file:
    CONFIG = json.load(env_file)
    account_sid = CONFIG["account_sid"]
    auth_token = CONFIG["auth_token"]
    service_sid = CONFIG["service_sid"]
    client = Client(account_sid, auth_token)
    phone = CONFIG["phone"]

# 1) I pre-select my wanted colors
# 2) Size is my personal sizeId (from vans API):
# WARN: sizeId seams to be different between products
knownDatas = {
    '3878358': {
        'name': 'rouge',
        'size': '3878373'
    },
    '4040448': {
        'name': 'bordeau',
        'size': '4040752'
    },
    '3989932': {
        'name': 'rose',
        'size': '3990077'
    },
    '4083503': {
        'name': 'beige',
        'size': '4084027'
    },
    '3976927': {
        'name': 'bleu fonce',
        'size': '3977021'
    }
}


def checkAvailability(productId, sizeId):
    apiResponse = requests.get(
        'https://www.vans.fr/webapp/wcs/stores/servlet/VFAjaxProductAvailabilityView?storeId=10159&langId=-2&productId=' + str(
            productId) + '&requesttype=ajax')
    return apiResponse.json()['stock'][sizeId]


def sendMessage(message):
    message = client.messages.create(
        messaging_service_sid=service_sid,
        body=message,
        to=phone
    )


message = '\nVans KyleWalker (Vans.fr) : \n'

for productId in knownDatas:

    newline = ''
    amount = checkAvailability(productId, knownDatas[productId]['size'])

    if amount > 0:
        newline += '✅ Version ' + knownDatas[productId]['name'] + ' (' + str(amount) + ' en stock)' + '\n'
    else:
        newline += '❌ Version ' + knownDatas[productId]['name'] + '\n'
    message += newline

print(message)
sendMessage(message)
