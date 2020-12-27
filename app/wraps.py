from ensembles import RandomForestMSE, GradientBoostingMSE, RMSE
from copy import copy
import pandas as pd


class Ensemble:
    __models = {
        'RF': RandomForestMSE,
        'GBM': GradientBoostingMSE,
    }

    __rus_types = {
        'RF': 'Случайный лес',
        'GBM': 'Градиентный бустинг'
    }

    def __init__(self, name, ens_type, form):
        self.name = name
        hyparams = form.data
        d = [('Тип ансамбля', self.__rus_types[ens_type])]
        d += [(form[param].label.text, hyparams[param]) for param in hyparams]
        self.description = pd.DataFrame(d, columns=['Параметр', 'Значение'])
        trees_parameters = hyparams.pop('trees_parameters')
        self.model = self.__models[ens_type](**{**hyparams, **trees_parameters})
        self.train_loss = None
        self.val_loss = None

    def fit(self, data_train, data_val=None):
        X_train = data_train.features
        y_train = data_train.target
        if data_val is not None:
            self.train_loss, self.val_loss = self.model.fit(X_train, y_train, data_val.features, data_val.target, True, True)
        else:
            self.train_loss = self.model.fit(X_train, y_train, return_train_loss=True)

    def predict(self, data_test):
        y_pred = self.model.predict(data_test.features)
        return pd.DataFrame(y_pred, index=data_test.data.index, columns=['prediction'])

    def __plot(self, loss):
        pass

    def plot(self, loss_type='train'):
        if loss_type == 'train':
            return self.__plot(self.train_loss)
        elif loss_type == 'val':
            return self.__plot(self.val_loss)
    

class Dataset:
    def __init__(self, name, data, target_name):
        self.name = name
        self.data = data
        self.target_name = target_name
        self.has_target = target_name != ''

    @property
    def features(self):
        if self.has_target:
            return self.data.drop(columns=self.target_name).to_numpy()
        else:
            return self.data.to_numpy()

    @property
    def target(self):
        if self.has_target:
            return self.data[self.target_name].to_numpy()
        else:
            raise ValueError(f'The target if {self.name} is unknown!')
