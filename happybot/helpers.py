import hashlib
import random
import datetime


def create_hash(email, secret):
    return hashlib.md5(email + secret).hexdigest()


def hash_password(password, salt):
    return hashlib.sha256(password + salt).hexdigest()


def create_schedule_time(start, stop):
    start_minutes = int(start * 60)
    stop_minutes = int(stop * 60)
    time = random.randint(start_minutes, stop_minutes)
    return datetime.time(hour=time / 60, minute=time % 60)


class Personality(object):
    def __init__(self, name, filename):
        self.name = name
        self.filename = filename
        self.messages = self._load()

    def _load(self):
        messages = []
        with open(self.filename, 'r') as f:
            for line in f.readlines():
                if line[0] == '#':
                    continue
                if len(line) == 0:
                    continue
                messages.append(line)
        return messages

    def get_message(self):
        return random.choice(self.messages)