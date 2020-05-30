import os
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import  datetime, date
import re

class Notification():
    def __init__(self, config):
        self.config = config
        sender_email = config.sender_email
        password = config.sender_passwd
        self.smtp_server = config.server
        context = ssl.create_default_context()
        self.smtp = smtplib.SMTP(self.smtp_server, 587)
        self.smtp.ehlo()
        self.smtp.starttls(context=context)
        self.smtp.ehlo()
        print('Start login', sender_email)
        self.smtp.login(sender_email, password)
        print('Login successfully.')

    def is_email(self, str_arg):
        regex = r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        if re.search(regex,str_arg) != None:
            return True
        return False

    def logout(self):
        self.smtp.quit()

    def create_mess_with_attachment(self, frame, clsname, prob):
        subject = clsname + " đã đến lúc " + str(datetime.now())
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = self.config.sender_email
        message["To"] = ','.join(self.config.receiver_email)
        mail_content = subject + '.'
        mail_content = MIMEText(mail_content, "plain")
        message.attach(mail_content)
        return message


    def send_mail(self, frame, clsname, prob):
        print('Start send mail from', self.config.sender_email, "to", self.config.receiver_email)
        message = self.create_mess_with_attachment(frame, clsname, prob)
        self.smtp.sendmail(self.config.sender_email, self.config.receiver_email, message.as_string())
        print('Successfully send mail from', self.config.sender_email, "to", self.config.receiver_email + '.')

    def is_new_day(self, saved_day):
        if date.today() != saved_day:
            return True
        return False
