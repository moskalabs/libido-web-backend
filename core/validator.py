import re

from django.core.exceptions     import ValidationError

REGEX_EMAIL = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-_]+$'
REGEX_PASSWORD = '^(?=.*[a-zA-Z])(?=.*[0-9])(?=.*[~₩!@#$%^&*()\-_=+])[a-zA-Z0-9~!@#$%^&*()_\-+=]{8,17}$'
REGEX_NICKNAME = '^[a-zA-Z0-9+-_.!#$%^&*]{0,12}$|^[a-zA-Z0-9+-_.!#$%^&*가-힣]{1,7}$'

def validates_email(email):
    if not re.match(REGEX_EMAIL, email) or email is None:
        raise ValidationError('INVALID_EMAIL')

def validates_password(password):
    if not re.match(REGEX_PASSWORD, password) or password is None:
        raise ValidationError('INVALID_PASSWORD')

def validates_nickname(nickname):
    if not re.match(REGEX_NICKNAME, nickname) or nickname is None:
        raise ValidationError('INVALID_NICKNAME')