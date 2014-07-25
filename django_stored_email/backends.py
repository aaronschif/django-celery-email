from django.core.mail.backends.base import BaseEmailBackend

from django_stored_email import tasks
from django_stored_email.models import EMail


class SimpleStorageEmailBackend(BaseEmailBackend):
    def __init__(self, fail_silently=False, queue='default'):
        super(SimpleStorageEmailBackend, self).__init__(fail_silently=False)
        self.queue = 'default'

    def send_messages(self, email_messages):
        to_send = []
        for msg in email_messages:
            x = EMail(message=msg, queue=self.queue)
            x.save()
            to_send.append(x.id)

        return to_send


class CeleryEmailBackend(SimpleStorageEmailBackend):
    def send_messages(self, email_messages):
        to_send = super(CeleryEmailBackend, self).send_messages(email_messages)

        tasks.send_emails.delay(to_send)



