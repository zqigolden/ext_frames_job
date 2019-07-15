"""
Author: ykliu@aibee.com
Date: 2018/9/25-15:01
"""

# -*- coding: utf-8 -*-
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib


class SendEmail(object):
    def __init__(self, receiver, subject, text):
        self.receiver = receiver
        self.subject = subject
        self.text = text

    def send(self):
        def _format_addr(s):
            name, addr = parseaddr(s)
            return formataddr((Header(name, 'utf-8').encode(), addr.encode('utf-8') if isinstance(addr, unicode) else addr))

        from_addr = '15110401917@163.com'
        password = 'qiaojinwei521*'
        smtp_server = 'smtp.163.com'

        msg = MIMEText(self.text, 'plain', 'utf-8')
        msg['From'] = _format_addr(from_addr)
        msg['To'] = _format_addr(self.receiver)
        msg['Subject'] = Header(self.subject, 'utf-8').encode()

        server = smtplib.SMTP(smtp_server, 25)
        server.set_debuglevel(0)
        server.login(from_addr, password)
        server.sendmail(from_addr, self.receiver.split(','), msg.as_string())
        server.quit()


if __name__ == '__main__':
    SendEmail(receiver='ykliu@aibee.com', subject='test', text='just a test').send()
