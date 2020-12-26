
from flask import Flask, render_template, request, redirect, url_for
from forms import NewEnsembleForm

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
    form = NewEnsembleForm()
    if form.validate_on_submit():
        models.append(form.model_type.data)
        print(models)
        return redirect(url_for('get_models'))
    return render_template('models.html', form=form, models=models)

@app.route('/models/settings/')

@app.route('/data/')
def get_datasets():
    return render_template('datasets.html')
