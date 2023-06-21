from __future__ import print_function
import imaplib
import email
import sys
import time
import requests
from email.header import decode_header

# Set the email server's hostname, port, username, password, and sleep time
hostname = sys.argv[1]
port = int(sys.argv[2])
username = sys.argv[3]
password = sys.argv[4]

# Django user settings
user_name = sys.argv[5]
pass_word = sys.argv[6]
number_phone = sys.argv[7]
sleep_time = int(sys.argv[8])

# Set the URL web services for Django
url = f"http://192.168.100.102:7777/send_email_sms/{user_name}/{pass_word}/{number_phone}/"


def decode_text(text):
    decoded_text = ""
    if text is not None:
        if isinstance(text, str):
            decoded_text = text
        else:
            try:
                decoded_text = text.decode("utf-8")
            except UnicodeDecodeError:
                decoded_text = text.decode("iso-8859-1")
    return decoded_text


def fetch_email_body():
    # Connect to the IMAP server
    mail = imaplib.IMAP4_SSL(hostname)
    mail.login(username, password)
    mail.select('INBOX')

    # Search for new unread emails
    status, data = mail.search(None, 'UNSEEN')
    email_ids = data[0].split()

    # Initialize a variable to store the email body
    email_body = ""

    # Iterate over each new unread email
    for email_id in email_ids:
        # Fetch the email data
        status, data = mail.fetch(email_id, '(RFC822)')
        raw_email = data[0][1]

        # Parse the email content
        email_message = email.message_from_bytes(raw_email)

        # Get the email body
        body = ''
        if email_message.is_multipart():
            for part in email_message.get_payload():
                if part.get_content_type() == 'text/plain':
                    body = part.get_payload(decode=True)
                    break
        else:
            body = email_message.get_payload(decode=True)

        # Decode and store the email body
        decoded_body = decode_text(body)
        email_body += decoded_body

        # Mark the email as read (optional)
        mail.store(email_id, '+FLAGS', '\\Seen')

    # Close the connection
    mail.close()
    mail.logout()

    # Return the email body
    return email_body


while True:
    # Fetch the email body and store it in a variable
    email_body = fetch_email_body()
    # print(email_body)

    # Sent the output to the specified URL
    response = requests.get(url + email_body)

    # /////////////////////////////////////////////////////////////#
    # /////////////////////////////////////////////////////////////#

    # Trouble Shoot the scripte

    #    if response.status_code == 200:
    #        print("Output sent successfully.")
    #    else:
    #        print("Failed to send the output. Status code:", response.status_code)

    # /////////////////////////////////////////////////////////////#
    # /////////////////////////////////////////////////////////////#

    # Initialize email_body variable
    email_body = ""

    # Sleep for 30 seconds
    time.sleep(sleep_time)
