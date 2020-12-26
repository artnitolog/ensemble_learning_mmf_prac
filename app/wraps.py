from ensembles import RandomForestMSE, GradientBoostingMSE, RMSE
from copy import copy

class Ensemble:
    __models = {
        'RF': RandomForestMSE,
        'GBM': GradientBoostingMSE,
    }

    def __init__(self, name, ens_type, hyparams):
        self.name = name
        self.ens_type = ens_type
        self.hyparams = copy(hyparams)
        trees_parameters = hyparams.pop('trees_parameters')
        self.model = self.__models[ens_type](**{**hyparams, **trees_parameters})


# class Dataset:
#     def __init__(self, features, target=None, index_col=None):
        # self.features = features
