import logging
import smtplib
from email.message import EmailMessage

from django.core.mail import mail_admins, send_mail


class SendMailHandler(logging.Handler):
    """
    Loghandler class to push logs to kafka
    """

    def emit(self, record):
        """
        """
        # msg = EmailMessage()
        # msg['Subject'] = 'Test subject123'
        # msg['From'] = ''
        # msg['To'] = 'antonio@gmail.com'
        # try:
        #    with smtplib.SMTP('mail.gmail.com') as s:
        #         s.send_message(msg)
        #         res = 1
        # except Exception as ex:
        #     res = 2
        #     self.handleError(record)

        # res = mail_admins('Subject', 'Message', fail_silently=False)
        res = send_mail('flo-backend', self.format(record), 'flo@gmail.com', ['antonio@gmail.com'], fail_silently=False)
        print(res)
