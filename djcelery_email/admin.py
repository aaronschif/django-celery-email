from django.contrib import admin
from djcelery_email.models import EMail

class EMailAdmin(admin.ModelAdmin):
    fields = ('subject',)

admin.site.register(EMail, EMailAdmin)