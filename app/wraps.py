import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from ensembles import RandomForestMSE, GradientBoostingMSE, RMSE


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
        hyparams = {**hyparams, **trees_parameters}
        self.model = self.__models[ens_type](**hyparams)
        self.train_loss = None
        self.val_loss = None

    def fit(self, data_train, data_val=None):
        X_train = data_train.features
        y_train = data_train.target
        self.target_name = data_train.target_name
        if data_val is not None:
            self.train_loss, self.val_loss = self.model.fit(
                X_train, y_train, data_val.features,
                data_val.target, True, True)
        else:
            self.train_loss = self.model.fit(X_train, y_train,
                                             return_train_loss=True)[0]

    @property
    def is_fitted(self):
        return self.train_loss is not None

    def predict(self, data_test):
        y_pred = self.model.predict(data_test.features)
        return pd.DataFrame(
            y_pred,
            index=data_test.data.index,
            columns=[self.target_name]
        )

    def plot(self, loss_type='train'):
        plt.rc('font', family='serif')
        plt.rc('axes', axisbelow=True, grid=True)
        plt.rc('grid', c='grey', ls=':')
        plt.rc('mathtext', fontset='dejavuserif')
        plt.rc('savefig', facecolor='white')
        fig, ax = plt.subplots(figsize=(6, 3), dpi=500)
        ax.set_title('Ошибка во время обучения')
        lim = self.model.n_estimators
        ax.plot(np.arange(1, lim + 1), self.train_loss,
                label='train', c='b')
        if self.val_loss is not None:
            ax.plot(np.arange(1, lim + 1), self.val_loss,
                    label='validation', c='m')
            varg = self.val_loss.argmin()
            ax.scatter(varg + 1, self.val_loss[varg], c='r',
                       zorder=3, label='optimum')
        ax.set_xlabel('n_estimators')
        ax.set_ylabel('RMSE')
        ax.legend()
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        fig.tight_layout()
        return fig


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
