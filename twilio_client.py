import os

from twilio.rest import Client


class TwilioClient(object):
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)
    messaging_service = 'whatsapp'
    from_number = '+14155238886'

    def send_whats_app_message(self, to_number, message):
        res = self.client.messages.create(
            to=f'{self.messaging_service}:{to_number}',
            body=message,
            from_=f'{self.messaging_service}:{self.from_number}'
        )
        return res.sid
