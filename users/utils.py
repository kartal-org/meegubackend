from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.conf import settings
import threading


class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


class Util:
    @staticmethod
    def send_email(data):
        t = get_template("authentication/activate.html")
        # email = EmailMultiAlternatives(subject=data["email_subject"], text_content=data["email_body"], from_email=settings.EMAIL_HOST_USER , to=[data["to_email"]])
        email = EmailMessage(subject=data["email_subject"], body=data["email_body"], to=[data["to_email"]])
        # email.attach_alternative(t.render(Context({})), "text/html")
        email.send()
