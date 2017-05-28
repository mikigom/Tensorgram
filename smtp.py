#!/usr/bin/python
# -*- coding:utf-8 -*-

import smtplib  
from email.MIMEMultipart import MIMEMultipart  
from email.MIMEBase import MIMEBase  
from email.MIMEText import MIMEText  
from email import Encoders  
from email import Utils  
from email.header import Header  
import os

smtp_server  = r"smtp.gmail.com"
port = 587  
userid = r"xxxxxxxxxxxxx"
passwd = r"xxxxxxxxxxxx"

def send_mail(from_user, to_user, cc_users, subject, text, attach):  
        COMMASPACE = ", "
        msg = MIMEMultipart("alternative")
        msg["From"] = from_user
        msg["To"] = to_user
        msg["Cc"] = COMMASPACE.join(cc_users)
        msg["Subject"] = Header(s=subject, charset="utf-8")
        msg["Date"] = Utils.formatdate(localtime = 1)
        msg.attach(MIMEText(text, "html", _charset="utf-8"))

        if (attach != None):
                part = MIMEBase("application", "octet-stream")
                part.set_payload(open(attach, "rb").read())
                Encoders.encode_base64(part)
                part.add_header("Content-Disposition", "attachment; filename=\"%s\"" % os.path.basename(attach))
                msg.attach(part)

        smtp = smtplib.SMTP(smtp_server, port)
        smtp.ehlo()
        smtp.starttls()
        smtp.login(userid, passwd)
        smtp.sendmail(from_user, cc_users, msg.as_string())
        smtp.close()
