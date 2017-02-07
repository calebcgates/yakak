#! python3
# textMyself.py - Defines the textmyself() function that texts a message
# passed to it as a string.

# Preset values:
accountSID = 'ACc3c112cda7ca1f5e4308f3ae042d3b30'
authToken = 'f87d7009f08d484492b8cf9b2d007bc2'
myNumber = '+18607547121'
twilioNumber = '+18608566944'

from twilio.rest import TwilioRestClient

def send(message):
    twilioCli = TwilioRestClient(accountSID, authToken)
    twilioCli.messages.create(body=message, from_=twilioNumber, to=myNumber)
