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
def send_message(twilio_number,user_number,message):
    account_sid = os.environ.get("ACCOUNT_SID")
    auth_token = os.environ.get("AUTH_TOKEN")
    client = Client(account_sid, auth_token)

    client.messages.create(
        from_=user_number,
        to=twilio_number,
        body=message
    )

# # Create your views here.
@csrf_exempt
def home(request):
    load_dotenv()
    # account_sid = os.environ.get("ACCOUNT_SID")
    # auth_token = os.environ.get("AUTH_TOKEN")
    TWILID_PHONE_NUMBER = os.environ.get("TWILID_PHONE_NUMBER")

    # client = Client(account_sid, auth_token)

    if request.method == "POST":
        message = request.POST
        #print(message)
        Name = message["ProfileName"]
        the_number = message["From"]
        the_Message = message["Body"]

        if the_Message.lower() in ['hey','hello','hi','hy','hei']:
            send_message(f'whatsapp:{TWILID_PHONE_NUMBER}',the_number, f"Hey  {Name}")
        
        elif "quote" in the_Message.lower():

            category = the_Message[5: ].strip()
            user_quote = get_quote(category)
            if isinstance(user_quote,str):
                send_message(f'whatsapp:{TWILID_PHONE_NUMBER}',the_number, user_quote)
                    
              
            else:
                output_quote = user_quote[0].get('quote')
                quote_author = user_quote[0].get('author')
                send_message(f'whatsapp:{TWILID_PHONE_NUMBER}',the_number ,f"Quote: {output_quote} \n Authors: {quote_author}")
              
        elif "joke" in the_Message.lower():

            limit = the_Message[5: ].strip()
            the_joke = get_joke(limit)
            
            if isinstance(the_joke,int):
                send_message(f'whatsapp:{TWILID_PHONE_NUMBER}',the_number,the_joke)
              
              
            else:
                result_joke = the_joke[0].get('joke')
                send_message(f'whatsapp:{TWILID_PHONE_NUMBER}',the_number,f"The Joke: \n{result_joke}\n😂 😂 😂 😂 😂")
                 
        else:
            send_message(f'whatsapp:{TWILID_PHONE_NUMBER}',the_number,"Only trained to response to greetings in english to provide a quote")
            
            

    return render(request, 'home.html')












