from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
import smtplib
import os
import sys

kindle_email = 'KINDLE EMAIL'  # the email that is associated with your Kindle device
gmail = 'YOUR GMAIL USERNAME'
gmail_password = 'YOUR GMAIL PASSWORD'


def send_email(file_path):

    #  code used from http://robertwdempsey.com/python3-email-with-attachments-using-gmail/
    recipients = [kindle_email]

    # Create the enclosing (outer) message
    outer = MIMEMultipart()
    outer['Subject'] = 'EMAIL SUBJECT'
    outer['To'] = kindle_email
    outer['From'] = gmail
    outer.preamble = 'You will not see this in a MIME-aware mail reader.\n'
    if type(file_path) is list:
        attachments = file_path
    else:
        attachments = [file_path]

    for file in attachments:
        try:
            with open(file, 'rb') as fp:
                msg = MIMEBase('application', "octet-stream")
                msg.set_payload(fp.read())
            encoders.encode_base64(msg)
            msg.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file))
            outer.attach(msg)
        except:
            print("Unable to open one of the attachments. Error: ", sys.exc_info()[0])
            raise

    composed = outer.as_string()

    # Send the email
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as s:
            s.ehlo()
            s.starttls()
            s.ehlo()
            s.login(gmail, gmail_password)
            s.sendmail(gmail, recipients, composed)
            s.close()
        print("Email sent!")
    except:
        print("Unable to send the email. Error: ", sys.exc_info()[0])
        raise

file_path = ""

if len(sys.argv) > 1:
    if not os.path.isfile(sys.argv[1]):
        print("Your input doesn't appear to be a valid path, try again")
    else:
        file_path = str(sys.argv[1])
        file_path = file_path.replace('"', "")
        send_email(file_path)
else:
    files = []
    while True:
        file_path = input("path to file (enter 'stop' to halt program): ")
        file_path = file_path.replace('"', "")
        if str(file_path).lower() == 'stop':
            break
        elif not os.path.isfile(file_path):
            print("Your input doesn't appear to be a valid path, try again")
        else:
            files.append(file_path)

    send_email(files)
