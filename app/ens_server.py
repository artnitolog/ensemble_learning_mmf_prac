import os
from flask import Flask, render_template, request, redirect, url_for, session
from forms import NewEnsembleForm, HyperParamForm, UploadForm, LearnForm, TestForm
from wraps import Ensemble, Dataset
from werkzeug.utils import secure_filename
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = 'verysecretkey'
app.url_map.strict_slashes = False

models = {}
datasets = {}


@app.route('/index')
@app.route('/')
def get_index():
    return render_template('index.html.j2')


@app.route('/models/', methods=['GET', 'POST'])
def get_models():
    form = NewEnsembleForm(meta={'csrf': False})
    if form.validate_on_submit():
        session['model_type'] = form.model_type.data
        return redirect(url_for('set_model', name=form.name.data))
    return render_template('models.html.j2', form=form, models=models)


@app.route('/models/<name>/settings/', methods=['GET', 'POST'])
def set_model(name):
    model_type = session['model_type']
    form = HyperParamForm(meta={'csrf': False})
    if form.validate_on_submit():
        if model_type == 'RF':
            del form.learning_rate
        models[name] = Ensemble(name, model_type, form)
        return redirect(url_for('get_models'))
    return render_template('set_model.html.j2', form=form, name=name, model_type=model_type)


@app.route('/data/', methods=['GET', 'POST'])
def get_data():
    form = UploadForm()
    if form.validate_on_submit():
        data = pd.read_csv(form.features_file.data, index_col=0)
        target_name = form.target_name.data
        if form.target_file.data is not None:
            target = pd.read_csv(form.target_file.data, index_col=0)
            if target_name == '':
                target_name = target.columns[0]
            data = pd.concat([data, target], axis=1)
        datasets[form.name.data] = Dataset(form.name.data, data, target_name)
        return redirect(url_for('get_data'))
    return render_template('datasets.html.j2', form=form, datasets=datasets)


@app.route('/models/<name>/work/', methods=['GET', 'POST'])
def model_page(name):
    learn_form = LearnForm(meta={'csrf': False})
    test_form = TestForm(meta={'csrf': False})
    learn_form.train_data.choices = [(d, d) for d in datasets if datasets[d].has_target]
    learn_form.val_data.choices = [(None, '-')] + learn_form.train_data.choices
    test_form.test_data.choices = [(d, d) for d in datasets]
    if learn_form.validate_on_submit():
        print('I am learning?')
        models[name].train_loss = True  # REMOVE
        return redirect(url_for('model_page', name=name))
    if test_form.validate_on_submit():
        print('I am predicted??')
        return redirect(url_for('model_page', name=name))
    return render_template('model_page.html.j2', model=models[name], learn_form=learn_form, test_form=test_form)
