import pytest
from django.core.mail import get_connection
from django.core import mail

from django_stored_email.backends import CeleryEmailBackend
from django_stored_email.models import EMail, EMailAttachment


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


@pytest.mark.django_db
def test_headers(email):
    test_headers = {'foo': 'bar'}
    email.extra_headers = test_headers
    me = EMail(message=email)
    assert me.extra_headers == test_headers
    me.save()

    me = EMail.objects.all()[0]
    assert me.extra_headers == test_headers


@pytest.mark.django_db
def test_attachment(email, test_file):
    email.attach_file(test_file)
    email.send()
    assert EMail.objects.count() == 1
    assert EMailAttachment.objects.count() == 1
