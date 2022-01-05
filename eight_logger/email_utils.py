from django.core.mail import EmailMessage
from django.core.mail.backends.smtp import EmailBackend
from django.template.loader import get_template

from eight_logger.models import EmailRecipients
from eight_logger.settings import api_settings

def send_email(body: dict, template: str) -> None:
    HOST = api_settings.EMAIL_CONFIG.get('HOST', None)
    HOST_USER = api_settings.EMAIL_CONFIG.get('HOST_USER', None)
    HOST_PASSWORD = api_settings.EMAIL_CONFIG.get('HOST_PASSWORD', None)
    PORT = api_settings.EMAIL_CONFIG.get('PORT', None)
    EMAIL_FAIL_SILENTLY = api_settings.EMAIL_CONFIG.get('EMAIL_FAIL_SILENTLY', True)
    EMAIL_USE_TLS = api_settings.EMAIL_CONFIG.get('EMAIL_USE_TLS', True)
    SEND_MAIL = api_settings.EMAIL_CONFIG.get('SEND_MAIL', False)
    EMAIL_USE_PASSWORD = api_settings.EMAIL_CONFIG.get('EMAIL_USE_PASSWORD', True)
    EMAIL_CONTEXT = "html"
    EMAIL_SENDER = api_settings.EMAIL_CONFIG.get('EMAIL_SENDER', None)

    print(SEND_MAIL)

    if SEND_MAIL:

        if EMAIL_USE_PASSWORD:
            email_backend = EmailBackend(
                host=HOST,
                port=PORT,
                username=HOST_USER,
                password=HOST_PASSWORD,
                use_tls=EMAIL_USE_TLS,
                fail_silently=EMAIL_FAIL_SILENTLY
            )
        else:
            email_backend = EmailBackend(
                host=HOST,
                port=PORT,
                username=HOST_USER,
                use_tls=EMAIL_USE_TLS,
                fail_silently=EMAIL_FAIL_SILENTLY
            )
        emails = list(EmailRecipients.objects.filter(active=True).values_list("email", flat=True))
        subject = body.get("subject", "N/A")

        # get template path for email
        email_template_path = template
        email_template = get_template(email_template_path).render(body)
        
        # setup for email message
        email_msg = EmailMessage(
            subject,
            email_template,
            EMAIL_SENDER,
            emails,
            cc=None,
            reply_to=[EMAIL_SENDER],
            connection=email_backend
        )
        email_msg.content_subtype = EMAIL_CONTEXT
        email_msg.send()
