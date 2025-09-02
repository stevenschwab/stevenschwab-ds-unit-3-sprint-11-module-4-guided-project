from os import getenv
from typing import Dict

import requests
import hashlib
from dotenv import load_dotenv

load_dotenv()
URL = getenv("NOT_TWITTER_URL")


class Post:

    def __init__(self, data: Dict):
        self.full_text = ""
        self.__dict__.update(data)

    def __repr__(self):
        return "\n".join(f"{k}: {v}" for k, v in vars(self).items())

    def __str__(self):
        return self.full_text


class User:

    def __init__(self, data: Dict):
        """Initialize User with screen_name and generate consistent ID"""
        self.screen_name = data.get('screen_name')
        if not self.screen_name:
            raise ValueError("screen_name is required")
        
        # generate deterministic ID from screen_name
        # use lowercase to ensure case-insensitive consistency
        hash_object = hashlib.md5(self.screen_name.lower().encode('utf-8'))
        # convert hash to integer and map to range [1000000, 9999999]
        hash_int = int(hash_object.hexdigest(), 16)
        self.id = 1000000 + (hash_int % (9999999 - 1000000 + 1))

        # fetch additional user data from API
        user_data = requests.get(f"{URL}/user/{self.screen_name}").json()
        self.__dict__.update(user_data)

    def timeline(self, *args, **kwargs):
        return [
            Post(post)
            for post in requests.get(f"{URL}/read/{self.screen_name}").json()
        ]

    def __repr__(self):
        return "\n".join(f"{k}: {v}" for k, v in vars(self).items())

    def __str__(self):
        return self.screen_name