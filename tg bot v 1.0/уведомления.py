import imaplib
import email
from email.header import decode_header
from telegram import Bot
import asyncio
import time

async def process_email_and_send_message(telegram_token, chat_id, sender, subject, body):
    # Отправка сообщения в Telegram
    bot = Bot(token=telegram_token)

    decoded_sender = decode_header(sender)[0][0]
    if isinstance(decoded_sender, bytes):
        decoded_sender = decoded_sender.decode('utf-8')

    decoded_sub = decode_header(subject)[0][0]
    if isinstance(decoded_sub, bytes):
        decoded_sub = decoded_sub.decode('utf-8')

    formatted_message = f"📧 *From:* {decoded_sender}\n📌 *Subject:* {decoded_sub}\n\n{body}"
    await bot.send_message(chat_id=chat_id, text=formatted_message, parse_mode='Markdown')

async def main():
    username = YOUR_GMAIL
    password = YOUR_PASSWORD_PRIL_GMAIL
    imap_server = "imap.gmail.com"
    imap_port = 993
    mailbox = "INBOX"
    telegram_token = "YOUR_TELEGRAM_TOKEN"
    chat_id = YOUR_USER_ID

    while True:
        mail = imaplib.IMAP4_SSL(imap_server, imap_port)
        mail.login(username, password)
        mail.select(mailbox)

        status, data = mail.search(None, 'UNSEEN')
        for num in data[0].split():
            status, message_data = mail.fetch(num, '(RFC822)')
            email_message = email.message_from_bytes(message_data[0][1])

            sender = email_message['From']
            subject = email_message['Subject']
            body = ""

            for part in email_message.walk():
                if part.get_content_type() == 'text/plain':
                    body = part.get_payload(decode=True).decode()

            await process_email_and_send_message(telegram_token, chat_id, sender, subject, body)

        mail.close()
        mail.logout()
        time.sleep(10)  # Пауза в 10 секунд между итерациями

if __name__ == '__main__':
    asyncio.run(main())