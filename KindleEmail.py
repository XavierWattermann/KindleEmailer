from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
import smtplib
import os
import sys


kindle_email = "KINDLE EMAIL"  # the email that is associated with your Kindle device

sender = 'YOUR GMAIL USERNAME'
gmail_password = 'YOUR GMAIL PASSWORD'


def send_email(file_path):
    #  code used from http://robertwdempsey.com/python3-email-with-attachments-using-gmail/
    recipients = [kindle_email]

    # Create the enclosing (outer) message
    outer = MIMEMultipart()
    outer['Subject'] = 'EMAIL SUBJECT'
    outer['To'] = kindle_email
    outer['From'] = sender
    outer.preamble = 'You will not see this in a MIME-aware mail reader.\n'
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
            s.login(sender, gmail_password)
            s.sendmail(sender, recipients, composed)
            s.close()
        print("Email sent!")
    except:
        print("Unable to send the email. Error: ", sys.exc_info()[0])
        raise


print('''From Amazon: The Kindle Personal Document Service can convert and deliver the following types of documents:
Microsoft Word (.doc, .docx), Rich Text Format (.rtf)
HTML (.htm, .html), Text (.txt) documents

Archived documents (zip , x-zip) and compressed archived documents, Mobi book

Images that are of type JPEGs (.jpg), GIFs (.gif), Bitmaps (.bmp), and PNG images (.png).
Adobe PDF (.pdf) documents are delivered without conversion to Kindle DX, Second Generation and Latest Generation Kindles.

Adobe PDF (.pdf) can be converted to Kindle format and delivered on an experimental basis.''')


while True:
    file_path = input("path to file(Windows: shift+right-click->copy as path): ")
    file_path = file_path.replace('"', "")
    if not os.path.isfile(file_path):
        print("Your input doesn't appear to be a valid path, try again")
    else:
        send_email(file_path)
        break
