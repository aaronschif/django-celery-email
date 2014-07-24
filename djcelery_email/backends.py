from django.core.mail.backends.base import BaseEmailBackend

from djcelery_email import tasks
from djcelery_email.models import EMail

from logging import getLogger

log = getLogger(__name__)


class CeleryEmailBackend(BaseEmailBackend):
    def __init__(self, fail_silently=False, **kwargs):
        super(CeleryEmailBackend, self).__init__(fail_silently)
        self.init_kwargs = kwargs

    def send_messages(self, email_messages, **kwargs):
        kwargs['_backend_init_kwargs'] = self.init_kwargs
        for msg in email_messages:
            x = EMail(message=msg)
            x.save()

        tasks.send_emails.delay()