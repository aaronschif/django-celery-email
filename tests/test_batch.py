import pytest
from django.core.mail import get_connection
from django.core import mail

from djcelery_email.backends import CeleryEmailBackend
from djcelery_email.models import EMail
from djcelery_email.tasks import send_email_batch


@pytest.mark.django_db
def test_batch(email):
    EMail(message=email).save()

    send_email_batch.delay()
    assert len(mail.outbox) == 1


@pytest.mark.django_db
def test_batch_html(html_email):
    EMail(message=html_email).save()

    send_email_batch.delay()
    assert len(mail.outbox) == 1


@pytest.mark.django_db
def test_number_batch(email):
    EMail(message=email).save()

    send_email_batch.delay(2)
    assert len(mail.outbox) == 1
