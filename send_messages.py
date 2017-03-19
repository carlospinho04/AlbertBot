from twilio.rest import TwilioRestClient
def send_message(phone_number, message):
    account_sid = '' # Your Account SID from www.twilio.com/console
    auth_token  = '' # Your Auth Token from www.twilio.com/console
    client = TwilioRestClient(account_sid, auth_token)
    message = client.messages.create(body=message,
                                 to='+351'+str(phone_number),    # Replace with your phone number
                                 from_='') # Replace with your Twilio number
