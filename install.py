import sys
from happybot import db, app
from happybot.models import Admin
from happybot.helpers import hash_password

if len(sys.argv) != 2:
    print('Usage: python install.py [password]')
    quit()

db.create_all()

if len(Admin.query.all()) != 0:
    print('Database already exists. Quitting...')
    quit()

password = sys.argv[1]
admin = Admin(hash_password(password, app.secret_key))
db.session.add(admin)
db.session.commit()

print("Success")
