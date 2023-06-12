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

print(f"khadam_imap/{hostname}/{port}/{username}/{password}/{user_name}/{pass_word}/{number_phone}/{sleep_time}/")