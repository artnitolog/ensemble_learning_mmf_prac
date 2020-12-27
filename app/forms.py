import json
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DecimalField, IntegerField
from wtforms.validators import DataRequired, Optional
from flask_wtf.file import FileField, FileAllowed, FileRequired

model_types = [
    ('RF', 'Случайный лес'),
    ('GBM', 'Градиентный бустинг'),
]

def json_field_filter(str_):
    try:
        dict_ = json.loads(str_)
    except Exception:
        dict_ = {}
    return dict_

class NewEnsembleForm(FlaskForm):
    name = StringField('Название модели', validators=[DataRequired()])
    model_type = SelectField('Тип ансамбля', choices=model_types)


class HyperParamForm(FlaskForm):
    n_estimators = IntegerField('Количество деревьев', default=100)
    learning_rate = DecimalField('Темп обучения', default=0.1)
    max_depth = IntegerField('Максимальная глубина', validators=[Optional()])
    feature_subsample_size = IntegerField('Размерность подвыборки признаков для одного дерева',
        validators=[Optional()])
    random_state = IntegerField('Сид', default=0)
    trees_parameters = StringField('Дополнительные параметры для дерева JSON!', validators=[Optional()], filters=[json_field_filter])


# class NewData(FlaskForm):
#     path = StringField('Абсолютный к файлу', )

class UploadForm(FlaskForm):
    name = StringField('Имя датасета', validators=[DataRequired()])
    upload_file = FileField('Датасет (csv)', validators=[
        FileRequired(),
        # FileAllowed(['csv'], 'CSV only!')
    ])
