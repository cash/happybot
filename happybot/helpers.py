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
