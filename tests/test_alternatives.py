import pytest
from django.core.mail import EmailMultiAlternatives, EmailMessage, get_connection
from django.core import mail

from djcelery_email.backends import CeleryEmailBackend
from djcelery_email.models import EMail


@pytest.fixture(autouse=True)
def patch_email(settings):
    settings.EMAIL_BACKEND = 'djcelery_email.backends.CeleryEmailBackend'
    settings.CELERY_EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
    settings.CELERY_ALWAYS_EAGER = True
    settings.CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
    settings.BROKER_BACKEND = 'memory'


@pytest.mark.django_db
def test_html(html_email):
    me = EMail(message=html_email)
    me.send()
