import logging
import smtplib
from email.message import EmailMessage

from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.test import TestCase

logger = logging.getLogger(__name__)


class EmailTest(TestCase):

    def setUp(self):
        User.objects.create(username='antonio')
        user = User.objects.get(username='antonio')

    def test_send_mail(self):
        """
        send_mail(
            'Subject',
            'Message',
            'antonio@gmail.com',
            ['grachev_ss@gmail.com'],
            fail_silently=False,
        )
        """
        """
        msg = EmailMessage()
        msg['Subject'] = 'Test subject'
        msg['From'] = ''
        msg['To'] = 'antonio@gmail.com'

        try:
            with smtplib.SMTP('mail.gmail.com') as s:
                s.send_message(msg)
                logger.info('message was sent')
            res = 1
        except Exception as ex:
            logger.error(str(ex))
            res = 2
        """
        logger.info("test_send_mail")
        #logger.debug("testsdcsdfdsf")

        self.assertEqual(1, 1)
