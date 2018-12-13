import logging
import smtplib
import unittest
from email.message import EmailMessage

logger = logging.getLogger(__name__)


class MyTestCase(unittest.TestCase):

    def test_logger(self):

        logger.info('test_loggertest_loggertest_logger')
        self.assertEqual(True, True)


    def test_smtp(self):

        msg = EmailMessage()
        msg['Subject'] = 'Test subject'
        msg['From'] = ''
        msg['To'] = 'grachev_ss@gmail.com'

        try:
            with smtplib.SMTP('mail.gmail.com') as s:
                s.send_message(msg)
                logger.info('message was sent')

        except Exception as ex:
            logger.error(str(ex))

        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
