from datetime import timedelta, datetime
import time as tm
from twilio.rest import Client


def sent_text_message(message):
    twilio_account_sid = "ACc416905d4eea04a741d1ac212aea8c12"
    twilio_account_token = "d41297ba4512219c2f3046901393a3fb"
    twilio_phone_num = "+12565677456"
    your_phone_number = "+14165565725"
    client = Client(twilio_account_sid, twilio_account_token)

    client.messages.create( 
        to=your_phone_number,
        from_=twilio_phone_num,
        body=message
    )

def get_Todo(input):
    input = input.strip().split("+")
    message = input[0]
    date = get_date(input[1])
    return message,date

def get_date(date):
    date = date.strip().split("/")
    formatted_date = datetime(int(date[0]), int(date[1]), int(date[2]), int(date[3]), int(date[4]), 0 )
    return formatted_date

def compare_time(other_time):
    current_time = datetime.now()
    time_difference = current_time - other_time
    if abs(time_difference) <= timedelta(minutes=10):
        return True
    else:
        return False

def check_time(date):
    valid_time = compare_time(get_date(date))
    return valid_time


