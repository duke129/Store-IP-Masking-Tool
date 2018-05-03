#!/usr/bin/python3
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
import os
import csv

def mail(filename):
    msg = MIMEMultipart()
    msg['Subject'] = 'Audit records'
    emailfrom = "xyz" 
    emailto = ['abc'] 
    msg['From'] = emailfrom
    msg['To'] = ','.join(emailto)
    msg.preamble = 'List of  audit records '
    csvfiles = [filename]
    try:
        for csv in csvfiles:
            print("filename is "+csv)
            with open(csv) as fp:
                record = MIMEBase('application', 'octet-stream')
                record.set_payload(fp.read())
                encoders.encode_base64(record)
                record.add_header('Content-Disposition', 'attachment',
                                      filename=os.path.basename(csv))
                msg.attach(record)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(emailfrom, 'password')
        server.sendmail(emailfrom, emailto, msg.as_string())
        print("Mail sent")
        server.quit()
    except Exception as e:
        print("error in sending mail" + str(e))