import pjconfig
import os
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import  datetime
import re


def isEmail(str_arg):
    regex = r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if re.search(regex,str_arg) != None:
        return True
        return False


def getReceiverEmailList():
    emails_file = open("receiver-email")
    receiver_email_list = [line.strip() for line in emails_file if isEmail(line.strip())]
    return receiver_email_list


def loginEmail():
    sender_email = pjconfig.SENDER_EMAIL
    password = pjconfig.SENDER_EMAIL_PASSWORD
    smtp_server = pjconfig.SMTP_SERVER
    context = ssl.create_default_context()
    try:
        server = smtplib.SMTP(smtp_server, 587)
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        print('Start login', sender_email)
        server.login(sender_email, password)
        print('Login successfully.')
        return server
    except Exception as e:
        print(e)


def logoutEmail(serverMail):
    try:
        serverMail.quit()
        print('Logout successfully.')
    except Exception as e:
        print(e)


def createMess(name_, sender_email, receiver_email):
    subject = name_ + " đã đến lúc " + str(datetime.now())
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email
    mail_content = subject + '.'
    mail_content = MIMEText(mail_content, "plain")
    message.attach(mail_content)
    return message


def sendMail(server, sender_email, receiver_email, message):
    try:
        print('Start send mail from', sender_email, "to", receiver_email)
        server.sendmail(sender_email, receiver_email, message.as_string())
        print('Successfully send mail from', sender_email, "to", receiver_email + '.')
    except Exception as e:
        print(e)


def createCheckinDict():
    classname = {}
    for _, clsdirs, _ in os.walk('./datasets/nccfaces/train/'):
        for index, clsdir in enumerate(clsdirs):
            classname[clsdir] = False
    return classname


def isNewDay(saved_day):
    if datetime.now().date != saved_day:
        return True
    return False
