import pjconfig
import os
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import  datetime, date
import re

class Notification():
    def __init__(self, config):
        self.config = config
        password = config.sender_passwd
        self.smtp_server = pjconfig.server
        context = ssl.create_default_context()
        try:
            self.smtp = smtplib.SMTP(smtp_server, 587)
            self.smtp.ehlo()
            self.smtp.starttls(context=context)
            self.smtp.ehlo()
            print('Start login', sender_email)
            self.smtp.login(sender_email, password)
            print('Login successfully.')
        except Exception as e:
            print(e)

    def is_email(self, str_arg):
        regex = r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        if re.search(regex,str_arg) != None:
            return True
        return False

    def logout(self):
        try:
            self.smtp.quit()
            print('Logout successfully.')
        except Exception as e:
            print(e)


    def create_mess_with_attachment(self, frame, cls, prob):
        subject = cls + " đã đến lúc " + str(datetime.now())
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = self.config.sender_email
        message["To"] = ','.join(self.config.receiver_email)
        mail_content = subject + '.'
        mail_content = MIMEText(mail_content, "plain")
        message.attach(mail_content)
        return message


    def send_mail(sender_email, receiver_email, message):
        try:
            print('Start send mail from', sender_email, "to", receiver_email)
            self.smtp.sendmail(sender_email, receiver_email, message.as_string())
            print('Successfully send mail from', sender_email, "to", receiver_email + '.')
        except Exception as e:
            print(e)


    def create_checkin_dict():
        classname = {}
        for _, clsdirs, _ in os.walk('./datasets/nccfaces/train/'):
            for index, clsdir in enumerate(clsdirs):
                classname[clsdir] = False
        return classname


    def is_new_day(self, saved_day):
        if date.today() != saved_day:
            return True
        return False

    def send(self, frame, pred_clsname):
        message = emailNotification.createMess(pred_clsname, sender_email, receiver_email)
        emailNotification.sendMail(serverMail, sender_email, receiver_email, message)    
