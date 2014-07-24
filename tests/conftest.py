import pytest
from django.core.mail import EmailMultiAlternatives, EmailMessage, get_connection


@pytest.fixture()
def email():
    email = EmailMessage(
        subject='Hello World',
        body='World is Great!',
        from_email='foobar@mail.net',
        to=['aaron@mail.net']
    )

    return email