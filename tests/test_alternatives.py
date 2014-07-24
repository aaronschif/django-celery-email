import pytest
from django.core.mail import EmailMultiAlternatives, EmailMessage, get_connection
from django.core import mail

from djcelery_email.backends import CeleryEmailBackend
from djcelery_email.models import EMail


@pytest.mark.django_db
def test_html(html_email):
    me = EMail(message=html_email)
    me.send()
