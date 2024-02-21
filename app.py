from flask import Flask

app = Flask(__name__)
 
@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/home')
def hi():
    return 'Hi, Wordl!'

if __name__ == "__main__":
    app.run()
