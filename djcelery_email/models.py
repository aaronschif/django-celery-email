from django.db import models
from django.core.mail import EmailMultiAlternatives

from fields import EmailsListField


class EMail(models.Model):
    def __init__(self, message=None):
        super(EMail, self).__init__()

        if message:
            self.subject = message.subject
            self.body = message.body

            self.to_emails = message.to
            self.cc_emails = message.cc
            self.bcc_emails = message.bcc

            self.from_email = message.from_email

            for alt in message.alternatives:
                EMailAlternative(self, **alt).save()

    def message(self):
        m = EmailMultiAlternatives(self.subject, self.body)
        m.to = self.to_emails
        m.cc = self.cc_emails
        m.bcc = self.bcc_emails
        m.from_email = self.from_email

        m.alternatives = [(att.content, att.mimetype) for att in self.attachments()]

        #m.extra_headers = self.headers

    def attachments(self):
        raise NotImplemented()

    def alternatives(self):
        return EMailAlternative.objects.filter(message=self)
    
    subject = models.CharField(max_length=250)
    body = models.TextField()

    to_emails = EmailsListField()
    cc_emails = EmailsListField()
    bcc_emails = EmailsListField()

    from_email = models.EmailField()

    #headers = models.TextField()

    # connection = None

    sent = models.BooleanField()


# Long term plan

class EMailAlternative(models.Model):
    def __init__(self, **info):#message, content, mime_type):
        super(EMail, self).__init__()
        self.message = info[0]
        self.content = info[1]
        self.mimetype = info[2]

    message = models.ForeignKey(EMail)

    content = None
    mimetype = None


# class EMailAttachment(models.Model):
#     message = models.ForeignKey(EMail)
#
#     filename = None
#     content = None
#     mimetype = None
