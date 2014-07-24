from django.db import models
from django.core.mail import EmailMultiAlternatives, get_connection
from django.conf import settings

from fields import EmailsListField


class EMail(models.Model):
    def __init__(self, *args, **kwargs):
        message = kwargs.pop('message', None)
        super(EMail, self).__init__(*args, **kwargs)

        if message:
            self.subject = message.subject
            self.body = message.body

            self.to_emails = message.to
            self.cc_emails = message.cc
            self.bcc_emails = message.bcc

            self.from_email = message.from_email

            self.save()
            if hasattr(message, 'alternatives'):
                for c in message.alternatives:
                    alt = EMailAlternative()
                    alt.message = self
                    alt.content = c[0]
                    alt.mimetype = c[1]
                    alt.save()

    def __unicode__(self):
        return "{m.subject} <From: {m.from_email}> To: {m.to_emails}".format(m=self)

    def message(self):
        m = EmailMultiAlternatives(self.subject, self.body)
        m.to = self.to_emails
        m.cc = self.cc_emails
        m.bcc = self.bcc_emails
        m.from_email = self.from_email

        m.alternatives = [(att.content, att.mimetype) for att in self.alternatives()]

        #m.extra_headers = self.headers

        return m

    def send(self, connection=None):
        if not connection:
            connection = get_connection(
                backend=getattr(settings, 'CELERY_EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend'))
        print connection
        connection.send_messages([self.message()])
        self.sent = True
        self.save()

    def attachments(self):
        raise NotImplemented()

    def alternatives(self):
        return EMailAlternative.objects.filter(message=self)
    
    subject = models.CharField(max_length=250)
    body = models.TextField()

    to_emails = EmailsListField()
    cc_emails = EmailsListField(blank=True)
    bcc_emails = EmailsListField(blank=True)

    from_email = models.EmailField()

    #headers = models.TextField()

    # connection = None

    sent = models.BooleanField(default=False)
    queued = models.DateField(auto_now=True)


# Long term plan

class EMailAlternative(models.Model):
    def __init__(self, *args, **kwargs):#message, content, mime_type):
        super(EMailAlternative, self).__init__(*args, **kwargs)

    message = models.ForeignKey(EMail)

    content = models.TextField()
    mimetype = models.CharField(max_length=200, default= 'text/html')

# class EMailAttachment(models.Model):
#     message = models.ForeignKey(EMail)
#
#     filename = None
#     content = None
#     mimetype = None
