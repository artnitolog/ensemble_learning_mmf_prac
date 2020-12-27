import os
from flask import Flask, render_template, request, redirect, url_for, session
from forms import NewEnsembleForm, HyperParamForm, UploadForm
from wraps import Ensemble
from werkzeug.utils import secure_filename
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = 'verysecretkey'
# app.config['UPLOAD_FOLDER'] = os.path.join('')
app.url_map.strict_slashes = False

models = {}
datasets = {}


@app.route('/index')
@app.route('/')
def get_index():
    return render_template('index.html')


@app.route('/models/', methods=['GET', 'POST'])
def get_models():
    form = NewEnsembleForm(meta={'csrf': False})
    if form.validate_on_submit():
        session['model_type'] = form.model_type.data
        return redirect(url_for('set_model', name=form.name.data))
    return render_template('models.html', form=form, models=models)

@app.route('/models/<name>/settings/', methods=['GET', 'POST'])
def set_model(name):
    model_type = session['model_type']
    form = HyperParamForm(meta={'csrf': False})
    if form.validate_on_submit():
        models[name] = Ensemble(name, model_type, form.data)
        return redirect(url_for('get_models'))
    return render_template('set_model.html', form=form, name=name, model_type=model_type)

@app.route('/data/', methods=['GET', 'POST'])
def get_data():
    form = UploadForm()
    if form.validate_on_submit():
        data = pd.read_csv(form.upload_file.data, index_col=0)
        datasets[form.name.data] = data
        return redirect(url_for('get_data'))
    return render_template('datasets.html', form=form, datasets=datasets)
