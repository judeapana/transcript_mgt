from enum import Enum

from flask_mail import Message

from transcript.ext import mail, rq


class ContentTypeEnum(Enum):
    HTML = 1
    TEXT = 2


@rq.job(description='Sending Mail', func_or_queue='ttu_default')
def send_email(emails, msg, content_type: ContentTypeEnum = ContentTypeEnum.TEXT, subject=None):
    try:
        message = Message()
        if emails:
            message.recipients = emails
        else:
            message.subject = subject or 'Transcript Manager'
        if content_type == ContentTypeEnum.TEXT:
            message.body = msg
        if content_type == ContentTypeEnum.HTML:
            message.html = msg
        mail.send(message)
    except Exception as e:
        return e
