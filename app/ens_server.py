import os
import io
import pandas as pd

from flask import Flask, render_template, url_for, session
from flask import request, redirect, Response
from flask import send_from_directory
from matplotlib.backends.backend_agg import FigureCanvasAgg

from forms import NewEnsembleForm, HyperParamForm
from forms import UploadForm, LearnForm, TestForm
from wraps import Ensemble, Dataset

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
    template_kwargs = {'form': form, 'name': name, 'model_type': model_type}
    return render_template('set_model.html.j2', **template_kwargs)


@app.route('/data/', methods=['GET', 'POST'])
def get_data():
    form = UploadForm()
    if form.validate_on_submit():
        data = pd.read_csv(form.features_file.data, index_col=0,
                           float_precision='round_trip')
        target_name = form.target_name.data
        if form.target_file.data is not None:
            target = pd.read_csv(form.target_file.data, index_col=0,
                                 float_precision='round_trip')
            if target_name == '':
                target_name = target.columns[0]
            data = pd.concat([data, target], axis=1)
        datasets[form.name.data] = Dataset(form.name.data, data, target_name)
        return redirect(url_for('get_data'))
    return render_template('datasets.html.j2', form=form, datasets=datasets)


@app.route('/models/<name>/plot.png')
def plot_png(name):
    fig = models[name].plot()
    output = io.BytesIO()
    FigureCanvasAgg(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


@app.route('/models/<name>/work/', methods=['GET', 'POST'])
def model_page(name):
    learn_form = LearnForm(meta={'csrf': False})
    test_form = TestForm(meta={'csrf': False})
    learn_form.train_data.choices = [d for d in datasets
                                     if datasets[d].has_target]
    learn_form.val_data.choices = ['-'] + learn_form.train_data.choices
    test_form.test_data.choices = [d for d in datasets]
    if learn_form.validate_on_submit():
        data_train = datasets[learn_form.train_data.data]
        data_val = datasets.get(learn_form.val_data.data)
        models[name].fit(data_train, data_val)
        return redirect(url_for('model_page', name=name))
    if test_form.validate_on_submit():
        data_test = datasets[test_form.test_data.data]
        preds = models[name].predict(data_test)
        fname = data_test.name + '_pred.csv'
        path = os.path.join(os.getcwd(), 'tmp/')
        if not os.path.exists(path):
            os.mkdir(path)
        preds.to_csv(os.path.join(path, fname))
        return send_from_directory(path, fname, as_attachment=True)
    template_kwargs = {
        'model': models[name],
        'learn_form': learn_form,
        'test_form': test_form,
    }
    return render_template('model_page.html.j2', **template_kwargs)
