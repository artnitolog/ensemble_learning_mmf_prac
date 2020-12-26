from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, DecimalField, IntegerField
from wtforms.validators import DataRequired

model_types = [
    ('RF', 'Случайный лес'),
    ('GBM', 'Градиентный бустинг'),
]


class NewEnsembleForm(FlaskForm):
    name = StringField('Название модели', validators=[DataRequired()])
    model_type = SelectField('Тип ансамбля', choices=model_types)
    submit = SubmitField('Продолжить')


class HyperParamForm(FlaskForm):
    n_estimators = IntegerField('Количество деревьев')
    learning_rate = DecimalField('Темп обучения')
    max_depth = IntegerField('Максимальная глубина')
    feature_subsample_size = IntegerField('Размерность подвыборки признаков для одного дерева')
    random_state = IntegerField('Сид')
