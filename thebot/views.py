from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from thebot import *
from twilio.rest import Client
import random
from .quotes import get_quote
from .jokes import get_joke
from dotenv import load_dotenv
import os

##implementing the DRY Method
# def send_message(twilio_number,user_number,message):
#     client.messages.create(

#     )
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
        #print(message)
        Name = message["ProfileName"]
        the_number = message["From"]
        the_Message = message["Body"]

        if the_Message.lower() in ['hey','hello','hi','hy','hei']:
            client.messages.create(
                from_= f'whatsapp:{TWILID_PHONE_NUMBER}',
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

        elif "joke" in the_Message.lower():

            limit = the_Message[5: ].strip()
            the_joke = get_joke(limit)
            
            if isinstance(the_joke,int):
                client.messages.create(
                    from_= TWILID_PHONE_NUMBER,
                    body = the_joke,
                    to = the_number
                )
            else:
                result_joke = the_joke[0].get('joke')
                client.messages.create(
                    from_ = TWILID_PHONE_NUMBER,
                    body = f"The Joke: \n{result_joke}\n😂 😂 😂 😂 😂",
                    to = the_number
                )
            
        else:
            client.messages.create(
                from_=TWILID_PHONE_NUMBER,
                body="Only trained to response to greetings in english to provide a quote",
                to=the_number
            )
        
        

    return render(request, 'home.html')












