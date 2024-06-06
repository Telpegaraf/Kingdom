import random
import string
from google.oauth2 import id_token
from google.auth.transport import requests


class Google:
    @staticmethod
    def validate(auth_token):
        try:
            id_info = id_token.verify_oauth2_token(auth_token, requests.Request())

            if 'accounts.google.com' in id_info['iss']:
                return id_info

        except Exception as e:
            return f"{e} invalid token"


def generate_random_password(length=12):
    """ generate random password """
    characters = string.ascii_letters + string.digits + string.punctuation
    password = "".join(random.choice(characters) for _ in range(length))

    return password
