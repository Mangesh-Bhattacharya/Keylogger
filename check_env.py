import os

email = os.getenv("KEYLOGGER_EMAIL")
password = os.getenv("KEYLOGGER_PASSWORD")

if email:
    print(f"KEYLOGGER_EMAIL is set to: {email}")
else:
    print("KEYLOGGER_EMAIL is NOT set.")

if password:
    print(f"KEYLOGGER_PASSWORD is set to: {'*' * len(password)} (hidden for security)")
else:
    print("KEYLOGGER_PASSWORD is NOT set.")