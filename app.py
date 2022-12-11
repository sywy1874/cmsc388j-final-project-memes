from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>ITS TIME TO MAKE SOME MEMES</h1>'

    # Test commit vs code to github