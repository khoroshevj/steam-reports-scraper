import re
import base64

import json
import smtplib
import time
import imaplib
import email

def get_code_from_email():
    message = read_latest_email()

    return extract_code_from_email(message)


def read_latest_email():
    with open("./config.json", "r") as configfile:
        config = json.load(configfile)['smtp']

    conn = imaplib.IMAP4_SSL(config['server'], config['port'])
    conn.login(config['email'], config['password'])
    conn.select('inbox')

    type, data = conn.search(None, 'ALL')
    mail_ids = data[0]
    id_list = mail_ids.split()   
    latest_email_id = int(id_list[-1])

    typ, data = conn.fetch(str(latest_email_id), '(RFC822)' )
    body = data[0][1].decode('utf-8')

    return body


def extract_code_from_email(input):
    patternt = r"<span[^>]+>([A-Z0-9]+)</span>"
    match = re.search(patternt, input).group(1)

    return match
