from django.conf import settings
from django.core.mail import get_connection

from celery import shared_task

from djcelery_email.models import EMail


@shared_task()
def send_emails():
    conn = get_connection(
        backend=getattr(settings, 'CELERY_EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend'))
    try:
        conn.open()
        emails = EMail.objects.filter(sent=False)[:5]

        for email in emails:
            email.send(connection=conn)

    finally:
        conn.close()

@shared_task()
def clean_old():
    pass
    # EMail.objects.filter()
