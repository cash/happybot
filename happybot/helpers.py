import hashlib


def create_hash(email, secret):
    return hashlib.md5(email + secret).hexdigest()


def hash_password(password, salt):
    return hashlib.sha256(password + salt).hexdigest()
