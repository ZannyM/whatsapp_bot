from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from thebot import *
from twilio.rest import Client
import random
from .quotes import get_quote
#import the env
from dotenv import load_dotenv
import os

'''[{'quote': 'All architecture is great architecture after sunset perhaps architecture is really a nocturnal art, like the art of fireworks.',
         'author': 'Gilbert K. Chesterton', 'category': 'art'}]'''
# # Create your views here.
@csrf_exempt
def home(request):
    load_dotenv()
    account_sid = os.environ.get("ACCOUNT_SID")
    auth_token = os.environ.get("AUTH_TOKEN")
    TWILID_PHONE_NUMBER = os.environ.get("TWILID_PHONE_NUMBER")

    client = Client(account_sid, auth_token)

    if request.method == "POST":
        message = request.POST
        Name = message["ProfileName"]
        the_number = message["From"]
        the_Message = message["Body"]

        if the_Message.lower() in ['hey','hello','hi','hy','hei']:
            client.messages.create(
                from_= TWILID_PHONE_NUMBER,
                body= f"Hey  {Name}",
                to=the_number
            )
        
        elif "quote" in the_Message.lower():

            category = the_Message[5: ].strip()
            user_quote = get_quote(category)
            if isinstance(user_quote,str):
                client.messages.create(
                    from_=TWILID_PHONE_NUMBER,
                    body= user_quote,
                    to= the_number
                )
            else:
                output_quote = user_quote[0].get('quote')
                quote_author = user_quote[0].get('author')
                client.messages.create(
                    from_= TWILID_PHONE_NUMBER,
                    body = f"Quote: {output_quote} \n Authors: {quote_author}",
                    to= the_number

                )

        elif "Cars" in the_Message.lower():
            " "
        else:
            client.messages.create(
                from_=TWILID_PHONE_NUMBER,
                body="Only trained to response to greetings in english to provide a quote",
                to=the_number
            )
        
        

    return render(request, 'home.html')






'''<QueryDict: {'SmsMessageSid': ['SM08cb5c43c59b20eec72619809b850441'], 'NumMedia': ['0'], 'ProfileName': ['🎀Zanny🎀'], 
'MessageType': ['text'], 'SmsSid': ['SM08cb5c43c59b20eec72619809b850441'], 'WaId': ['27714470844'], 'SmsStatus': ['received'],
 'Body': ['hi'], 'To': ['whatsapp:+14155238886'], 'NumSegments': ['1'], 'ReferralNumMedia': ['0'], 'MessageSid': 
 ['SM08cb5c43c59b20eec72619809b850441'], 'AccountSid': 
['AC50e8612329ed35ea990f820b8a823ad6'], 'From': ['whatsapp:+27714470844'], 'ApiVersion': ['2010-04-01']}> '''







