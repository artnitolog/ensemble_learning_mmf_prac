
from flask import Flask, render_template, request, redirect, url_for, session
from forms import NewEnsembleForm, HyperParamForm
from wraps import Ensemble

app = Flask(__name__)
app.config['SECRET_KEY'] = 'verysecretkey'
app.url_map.strict_slashes = False

models = []


@app.route('/index')
@app.route('/')
def get_index():
    return render_template('index.html')


@app.route('/models/', methods=['GET', 'POST'])
def get_models():
    form = NewEnsembleForm(csrf_enabled=False)
    if form.validate_on_submit():
        session['model_type'] = form.model_type.data
        return redirect(url_for('set_model', name=form.name.data))
    return render_template('models.html', form=form, models=models)

@app.route('/models/<name>/settings/', methods=['GET', 'POST'])
def set_model(name):
    form = HyperParamForm(csrf_enabled=False)
    if form.validate_on_submit():
        # hyparams = form_to_hyparams(form.data)
        return str(form.data)
    return render_template('set_model.html', form=form, name=name, mode_type=session['model_type'])

@app.route('/data/')
def get_datasets():
    return render_template('datasets.html')
