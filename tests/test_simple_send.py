import pytest
from django.core.mail import get_connection
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
def test_simple_email(email):
    m_email = EMail(message=email)
    m_email.send()

    assert EMail.objects.count() == 1
    assert len(mail.outbox) == 1

@pytest.mark.django_db
def test_unicode(email):
    e_mail = EMail(message=email)
    assert unicode(e_mail)

@pytest.mark.django_db
def test_simple_backend(email):
    email.send()

    assert EMail.objects.count() == 1


def test_email_backend_in_place():
    backend = get_connection()
    assert isinstance(backend, CeleryEmailBackend)