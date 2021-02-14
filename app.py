from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = 'secret_key'


@app.route('/')

def index():
    return render_template('main.html')
@app.route('/home')

def home():
    return render_template('main.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')
    


if __name__ == '__main__':
    app.run()
