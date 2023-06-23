import poplib
import email
import quopri
import requests
import time
import sys

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

# Create a POP3 client object
client = poplib.POP3_SSL(hostname, port)

# Try to login to the email server
try:
    client.user(username)
    client.pass_(password)
except poplib.error_proto as e:
    print("Error logging in:", e)
    exit(1)

# Initialize email_body variable
email_body = ""

# Get the number of total emails and the list of unique identifiers (UIDs)
response, msg_count, octet_count = client.list()
msg_count_decoded = [line.decode() for line in msg_count]

# Loop through the message numbers and their corresponding UIDs
for msg_info in msg_count_decoded:
    msg_num, uid = msg_info.split()

    # Check if the email is marked as unseen (not seen)
    response, flags, octets = client.top(int(msg_num), 0)
    flags = [flag.lower() for flag in flags]
    if b"seen" not in flags:
        # Get the email message
        response, lines, octets = client.retr(int(msg_num))

        # Join the lines into a single bytes object
        message = b"\r\n".join(lines)

        # Parse the email message
        msg = email.message_from_bytes(message)

        # Get the email's body content
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                if content_type == "text/plain":
                    payload = part.get_payload(decode=True)
                    charset = part.get_content_charset()
                    if charset:
                        body = payload.decode(charset)
                    else:
                        body = payload.decode()
                    break
        else:
            payload = msg.get_payload(decode=True)
            charset = msg.get_content_charset()
            if charset:
                body = payload.decode(charset)
            else:
                body = payload.decode()

        # Set email body in a variable
        email_body = body

        # Delete the email from the inbox
        client.dele(int(msg_num))

if email_body:
    # Send the output to the specified URL
    response = requests.get(url + email_body)

# Close the connection to the email server (will never be reached in this script)
client.quit()
