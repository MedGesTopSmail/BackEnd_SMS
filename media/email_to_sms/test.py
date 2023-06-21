import sys
import time

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
url = f"http://192.168.100.102:7777/send_link_sms/{user_name}/{pass_word}/{number_phone}/message"
list = f"hostname:{hostname}, port:{port}, username:{username}, password:{password}, user_name:{user_name}, pass_word:{pass_word}, number_phone:{number_phone}, sleep_time: {sleep_time}."

print(url)
print(list)


time.sleep(sleep_time)