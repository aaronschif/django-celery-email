from django.core.mail.backends.base import BaseEmailBackend

from django_stored_email import tasks
from django_stored_email.models import EMail


class CeleryEmailBackend(BaseEmailBackend):
    def __init__(self, fail_silently=False, **kwargs):
        super(CeleryEmailBackend, self).__init__(fail_silently)
        self.init_kwargs = kwargs

    def send_messages(self, email_messages, **kwargs):
        to_send = []
        for msg in email_messages:
            x = EMail(message=msg)
            x.save()
            to_send.append(x.id)

        tasks.send_emails.delay(to_send)