#!/usr/bin/env python
import sys
import time
import datetime
import smtplib

import requests

from requests.exceptions import Timeout, HTTPError

from threading import Timer


class Checker(object):
    URL_TO_CHECK = 'http://bmwlog.pp.ua/'
    CHECK_INTERVAL = 3
    ALERT_INTERVAL = 60 * 60 * 60  # mail send interval in seconds
    MAIL_USERNAME = 'misha.behersky@example.com'
    MAIL_PASSWORD = ''
    ALERT_MAIL = 'bmwant@gmail.com'

    def __init__(self, username=None, password=None):
        self.username = username or self.MAIL_USERNAME
        self.password = password or self.MAIL_PASSWORD

        self.server = smtplib.SMTP_SSL('smtp.example.com', 465)
        try:
            self.server.login(self.username, self.password)
        except smtplib.SMTPAuthenticationError as e:
            sys.stderr.write('Authentication failed. '
                             'Invalid username/password\n')
            sys.exit(1)

        self.last_alert_stamp = 0

    def send_mail(self, mail_text, subject_text=None):
        from_addr = 'monitoring@bmwlog.pp.ua'
        to_addr = self.ALERT_MAIL
        subject = subject_text or 'Alerting for {host}'.format(
            host=self.URL_TO_CHECK)

        msg = ('From: {from_addr}\r\n'
               'To: {to_addr}\r\n'
               'Subject: {subject}\r\n\r\n'
               '{mail_text}'.format(from_addr=from_addr,
                                    to_addr=to_addr,
                                    subject=subject,
                                    mail_text=mail_text))

        self.server.sendmail(self.MAIL_USERNAME, self.ALERT_MAIL, msg)

    def _periodic_alert(self, alert_message):
        now = time.time()
        display_time = datetime.datetime.now().strftime('%d/%m/%y %H:%M')
        if now - self.last_alert_stamp > self.ALERT_INTERVAL:
            sys.stderr.write('{time}: sending alert\n'.format(
                time=display_time))
            self.send_mail(alert_message)
            self.last_alert_stamp = now

    def check(self):
        t = Timer(self.CHECK_INTERVAL, self.check)
        t.start()
        try:
            r = requests.get(self.URL_TO_CHECK, timeout=1)
        except (HTTPError, Timeout) as e:
            message = 'Remote is down.\nReason:\n%s' % e
            self._periodic_alert(message)

        except Exception as e:
            message = 'Checker got into trouble itself.\nReason:\n%s' % e
            self._periodic_alert(message)


if __name__ == '__main__':
    checker = Checker()
    try:
        checker.check()
    except KeyboardInterrupt:
        pass
