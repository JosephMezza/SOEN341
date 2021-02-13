from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = 'secret_key'


@app.route('/')
def index():
    return render_template('base.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/create')
def create():
    return render_template('create.html')


if __name__ == '__main__':
    app.run()
