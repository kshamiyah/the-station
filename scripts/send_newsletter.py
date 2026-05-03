#!/usr/bin/env python3
"""
Send Obs and Gynae Newsletter via Email
Sends the generated newsletter HTML to specified email addresses
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import os
import getpass
import sys
import argparse

def send_newsletter_email(recipient_email, sender_email, app_password, subject=None):
    """
    Send the newsletter HTML file via Gmail SMTP
    
    Args:
        recipient_email: Email address to send to
        sender_email: Gmail address sending from
        app_password: Gmail app password (not regular password)
        subject: Email subject line (optional)
    """
    
    # Read the HTML newsletter
    html_file = "../build/newsletter.html"
    if not os.path.exists(html_file):
        print(f"Error: {html_file} not found. Please run generate_newsletter.py first.")
        return False
    
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Create message
    msg = MIMEMultipart('alternative')
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject or "Obs and Gynae Monthly Wrap-Up Newsletter"
    
    # Create HTML part
    html_part = MIMEText(html_content, 'html', 'utf-8')
    msg.attach(html_part)
    
    try:
        # Connect to Gmail SMTP server
        print("Connecting to Gmail SMTP server...")
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        
        # Login
        print("Logging in...")
        server.login(sender_email, app_password)
        
        # Send email
        print(f"Sending newsletter to {recipient_email}...")
        text = server.send_message(msg)
        server.quit()
        
        print(f"✓ Newsletter sent successfully to {recipient_email}!")
        return True
        
    except smtplib.SMTPAuthenticationError:
        print("Error: Authentication failed. Please check your app password.")
        print("\nTo get a Gmail app password:")
        print("1. Go to your Google Account settings")
        print("2. Security → 2-Step Verification → App passwords")
        print("3. Generate a new app password for 'Mail'")
        return False
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(description='Send Obs and Gynae Newsletter via Email')
    parser.add_argument('--sender', '-s', help='Gmail address to send from')
    parser.add_argument('--password', '-p', help='Gmail App Password')
    parser.add_argument('--subject', help='Email subject line')
    parser.add_argument('--recipient', '-r', default='k.shamiyah@gmail.com', help='Recipient email address')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("Obs and Gynae Newsletter Email Sender")
    print("=" * 60)
    print()
    
    # Configuration
    recipient_email = args.recipient
    
    # Get sender email
    if args.sender:
        sender_email = args.sender
    else:
        try:
            sender_email = input("Enter your Gmail address: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nError: Gmail address is required. Use --sender or run interactively.")
            return
    
    if not sender_email:
        print("Error: Gmail address is required.")
        return
    
    # Get app password
    if args.password:
        app_password = args.password
    else:
        try:
            print("\nNote: You need a Gmail App Password (not your regular password).")
            print("If you don't have one, get it from:")
            print("Google Account → Security → 2-Step Verification → App passwords")
            print()
            app_password = getpass.getpass("Enter your Gmail App Password: ")
        except (EOFError, KeyboardInterrupt):
            print("\nError: App password is required. Use --password or run interactively.")
            return
    
    if not app_password:
        print("Error: App password is required.")
        return
    
    # Get subject
    if args.subject:
        subject = args.subject
    else:
        try:
            subject_input = input("\nEmail subject (press Enter for default): ").strip()
            subject = subject_input if subject_input else "Obs and Gynae Monthly Wrap-Up Newsletter"
        except (EOFError, KeyboardInterrupt):
            subject = "Obs and Gynae Monthly Wrap-Up Newsletter"
    
    print()
    print("-" * 60)
    
    # Send the email
    success = send_newsletter_email(
        recipient_email=recipient_email,
        sender_email=sender_email,
        app_password=app_password,
        subject=subject
    )
    
    if success:
        print("-" * 60)
        print("Newsletter sent successfully!")
    else:
        print("-" * 60)
        print("Failed to send newsletter. Please check the error messages above.")


if __name__ == "__main__":
    main()
