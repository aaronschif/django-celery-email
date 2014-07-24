import pytest
from django.core.mail import EmailMultiAlternatives, EmailMessage, get_connection


@pytest.fixture()
def email():
    email = EmailMessage(
        subject='Hello World',
        body='World is Great!',
        from_email='foobar@mail.net',
        to=['frank@mail.net']
    )

    return email


@pytest.fixture()
def html_email():
    email = EmailMultiAlternatives(
        subject='Hello World',
        body='World is Great!',
        from_email='foobar@mail.net',
        to=['bill@mail.net']
    )
    email.attach_alternative('World is <b>SUPER</b> Great!', 'text/html')
    return email


@pytest.fixture(autouse=True)
def patch_email(settings):
    settings.EMAIL_BACKEND = 'djcelery_email.backends.CeleryEmailBackend'
    settings.CELERY_EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
    settings.CELERY_ALWAYS_EAGER = True
    settings.CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
    settings.BROKER_BACKEND = 'memory'