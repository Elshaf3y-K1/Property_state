from django.core.mail import EmailMessage
from django.template.loader import get_template
import os



class Util:
    @staticmethod
    def send_email(data):
        html_tpl_path = 'mail.html'
        context_data =  data
        email_html_template = get_template(html_tpl_path).render(context_data)
        email_msg = EmailMessage(data['title'],email_html_template,os.environ['EMAIL_HOST_USER'] ,[data['to_email']],reply_to=[os.environ['EMAIL_HOST_USER']])
        email_msg.content_subtype = 'html'
        email_msg.send(fail_silently=False)