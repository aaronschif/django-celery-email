from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail import get_connection
from django.conf import settings

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
            to_send.append(x)

        return to_send


class StoreSendEmailBackend(BaseEmailBackend):
    def send_messages(self, email_messages):
        to_send = super(StoreSendEmailBackend, self).send_messages(email_messages)
        conn = get_connection(
            backend=getattr(settings, 'STORED_EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend'))

        try:
            conn.open()
            for m in to_send:
                m.send(connection=conn)
        finally:
            conn.close()


class CeleryEmailBackend(SimpleStorageEmailBackend):
    def send_messages(self, email_messages):
        to_send = super(CeleryEmailBackend, self).send_messages(email_messages)

        tasks.send_emails.delay([m.id for m in to_send])



