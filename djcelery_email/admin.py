from django.contrib import admin
from djcelery_email.models import EMail

@admin.register(EMail)
class EMailAdmin(admin.ModelAdmin):
    fields = ('subject', 'to_emails')