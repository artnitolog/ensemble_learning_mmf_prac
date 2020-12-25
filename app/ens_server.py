from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'testkey'


@app.route('/')
def get_index():
    return '<html><center>Hello, I am your future RF & GBM API!</center></html>'
