HappyBot
============
Make people happy by sending them encouraging messages.
Inspired by the [NiceBot](https://twitter.com/thenicebot) on Twitter.

Requirements
--------------
 * Python
 * A message broker for [Celery](http://docs.celeryproject.org/en/latest/getting-started/first-steps-with-celery.html) like RabbitMQ or Redis
 * A mail server (SMTP)

Installing
---------------
 * Install the python dependencies: `pip install -r requirements`
 * Copy example.cfg to happybot.cfg and follow instructions in the file to edit settings
 * Run the install script: `python install.py <admin password>`

Running
---------------
A non-production ready web server is built into Flask and can be run with `python run.py`. The celery worker
must be started with `celery worker -A happybot.jobs` and a celery beat scheduler started with
`celery -A happybot.jobs beat`.
