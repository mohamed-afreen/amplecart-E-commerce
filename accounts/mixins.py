
from django.conf import settings
from twilio.rest import Client
import random


class MessageHandler:
    phone_number = None
    otp = None

    def __init__(self, phone_number, otp) -> None:
        self.phone_number = phone_number
        self.otp = otp

    def sent_otp_on_phone(self):
        client = Client(settings.ACCOUNT_SID, settings.AUTH_TOKEN)
        verification = client.verify \
            .v2 \
            .services('VAdf499a94df5acebff43ad1e8cc092d34') \
            .verifications \
            .create(to=self.phone_number, channel='sms')

    def validate(self):
        client = Client(settings.ACCOUNT_SID, settings.AUTH_TOKEN)
        verification_check = client.verify.v2.services(
            'VAdf499a94df5acebff43ad1e8cc092d34'
        ).verification_checks.create(to=self.phone_number, code=self.otp)
        validation = verification_check.status
        print(validation)
        return validation
