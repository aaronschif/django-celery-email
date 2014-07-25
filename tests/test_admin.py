import pytest
from django.core.mail import get_connection
from django.core import mail

from djcelery_email.backends import CeleryEmailBackend
from djcelery_email.models import EMail


@pytest.mark.django_db
def test_admin(html_email, admin_client):
    admin_client.get('/admin/djcelery_email/email/')
    admin_client.get('/admin/djcelery_email/email/1/')

