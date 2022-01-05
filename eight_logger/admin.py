from django.contrib import admin

from .models import AccessLog, ErrorLog, ExceptionLog, EmailRecipients

admin.site.register(AccessLog)
admin.site.register(ErrorLog)
admin.site.register(ExceptionLog)
admin.site.register(EmailRecipients)
