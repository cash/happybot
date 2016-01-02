from flask import Flask, flash, render_template, request
from flask_bootstrap import Bootstrap
from forms import SignupForm

app = Flask(__name__)
Bootstrap(app)
app.secret_key = 's3cr3t'


@app.route('/', methods=['GET', 'POST'])
def serve_index():
    form = SignupForm()
    return render_template('index.html', form=form)

@app.route('/submit', methods=['POST'])
def serve_submit():
    return render_template('message.html', msg='Submission complete')

@app.route('/confirm')
def serve_confirm():
    return render_template('message.html', msg='Subscription confirmed')

@app.route('/admin')
def serve_admin():
    return render_template('admin.html')

if __name__ == '__main__':
    app.run(debug=True)
