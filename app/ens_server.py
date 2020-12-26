from flask import Flask, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = 'testkey'


@app.route('/')
def get_index():
    return render_template('index.html')


@app.route('/models/')
def get_models():
    return render_template('models.html')


@app.route('/data/')
def get_datasets():
    return render_template('datasets.html')
