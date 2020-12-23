import numpy as np
from sklearn.tree import DecisionTreeRegressor
from scipy.optimize import minimize_scalar
from .utils import RMSE


class RandomForestMSE:
    def __init__(self, n_estimators, max_depth=None,
                 feature_subsample_size=None,
                 random_state=None,
                 **trees_parameters):
        """
        n_estimators : int
            The number of trees in the forest.

        max_depth : int
            The maximum depth of the tree.
            If None then there is no limits.

        feature_subsample_size : float
            The size of feature set for each tree.
            If None then use recommendations.

        random_state : int
            The seed to initialize random generator.
        """
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.max_features = feature_subsample_size
        self.trees_parameters = trees_parameters
        self.seed = random_state
        self.models = []

    def fit(self, X, y, X_val=None, y_val=None,
            return_train_loss=False,
            return_val_loss=False):
        """
        X : numpy ndarray
            Array of size n_objects, n_features

        y : numpy ndarray
            Array of size n_objects

        X_val : numpy ndarray, optional
            Array of size n_val_objects, n_features

        y_val : numpy ndarray, optional
            Array of size n_val_objects

        return_train_loss : bool
            Specifies if RMSE on train after each
            iteration should be returned.

        return_val_loss : bool
            Specifies if RMSE on validation after each
            iteration should be returned (X_val and y_val
            must be provided!)

        Returns
        -------
        train_loss : numpy ndarray,  optional
            Return iterative RMSE on the train set. Only
            provided if return_train_loss is True.

        val_loss : numpy ndarray,  optional
            Return iterative RMSE on the validation set. Only
            provided if return_val_loss is True.
        """
        if self.max_features is None:
            max_features = max(1, X.shape[1] // 3)
        else:
            max_features = self.max_features
        rng = np.random.default_rng(seed=self.seed)
        for _ in range(self.n_estimators):
            idx = rng.choice(len(y), len(y))
            model = DecisionTreeRegressor(max_depth=self.max_depth,
                                          max_features=max_features,
                                          random_state=rng.integers(1e5),
                                          **self.trees_parameters)
            model.fit(X[idx], y[idx])
            self.models.append(model)
        return_values = []
        if return_train_loss:
            return_values.append(self.loss_iter(X, y))
        if return_val_loss:
            return_values.append(self.loss_iter(X_val, y_val))
        if return_values:
            return tuple(return_values)

    def predict(self, X):
        """
        X : numpy ndarray
            Array of size n_objects, n_features

        Returns
        -------
        y : numpy ndarray
            Array of size n_objects
        """
        return np.mean([model.predict(X) for model in self.models], axis=0)

    def loss_iter(self, X, y):
        """
        X : numpy ndarray
            Array of size n_objects, n_features

        y : numpy ndarray
            Array of size n_objects

        Returns
        -------
        iter_rmse : numpy ndarray
            Array of size n_objects, iter_rmse[i] is
            the RandomForest RMSE of the first (i + 1) models.
        """
        preds_pm = [model.predict(X) for model in self.models]
        preds = (np.cumsum(preds_pm, axis=0)
                 / (np.arange(self.n_estimators) + 1)[:, None])
        return RMSE(y, preds)


class GradientBoostingMSE:
    def __init__(self, n_estimators, learning_rate=0.1, max_depth=5,
                 feature_subsample_size=None, random_state=None,
                 **trees_parameters):
        """
        n_estimators : int
            The number of trees in the forest.

        learning_rate : float
            Use learning_rate * gamma instead of gamma
        max_depth : int
            The maximum depth of the tree. If None then there is no limits.

        feature_subsample_size : float
            The size of feature set for each tree.
            If None then use recommendations.

        random_state : int
            The seed to initialize random generator.
        """
        self.n_estimators = n_estimators
        self.lr = learning_rate
        self.max_depth = max_depth
        self.max_features = feature_subsample_size
        self.seed = random_state
        self.trees_parameters = trees_parameters
        self.models = []

    def fit(self, X, y, X_val=None, y_val=None,
            return_train_loss=False,
            return_val_loss=False):
        """
        X : numpy ndarray
            Array of size n_objects, n_features

        y : numpy ndarray
            Array of size n_objects

        X_val : numpy ndarray, optional
            Array of size n_val_objects, n_features

        y_val : numpy ndarray, optional
            Array of size n_val_objects

        return_train_loss : bool
            Specifies if RMSE on train after each
            iteration should be returned.

        return_val_loss : bool
            Specifies if RMSE on validation after each
            iteration should be returned (X_val and y_val
            must be provided!)

        Returns
        -------
        train_loss : numpy ndarray,  optional
            Return iterative RMSE on the train set. Only
            provided if return_train_loss is True.

        val_loss : numpy ndarray,  optional
            Return iterative RMSE on the validation set. Only
            provided if return_val_loss is True.
        """
        if self.max_features is None:
            max_features = max(1, X.shape[1] // 3)
        else:
            max_features = self.max_features
        rng = np.random.default_rng(seed=self.seed)
        prev_pred = 0
        if return_train_loss:
            train_loss = np.empty(self.n_estimators)
        if return_val_loss:
            prev_val_pred = 0
            val_loss = np.empty(self.n_estimators)
        self.alphas = np.empty(self.n_estimators)

        def loss(alpha, y, prev_pred, corr):
            return ((prev_pred + alpha * corr - y) ** 2).sum()

        for i in range(self.n_estimators):
            model = DecisionTreeRegressor(max_depth=self.max_depth,
                                          max_features=max_features,
                                          random_state=rng.integers(1e5),
                                          **self.trees_parameters)
            model.fit(X, y - prev_pred)
            corr = model.predict(X)
            self.models.append(model)
            alpha = minimize_scalar(loss, args=(y, prev_pred, corr)).x
            prev_pred += alpha * self.lr * corr
            if return_train_loss:
                train_loss[i] = RMSE(y, prev_pred)
            if return_val_loss:
                prev_val_pred += alpha * self.lr * model.predict(X_val)
                val_loss[i] = RMSE(y_val, prev_val_pred)
            self.alphas[i] = alpha
        return_values = []
        if return_train_loss:
            return_values.append(train_loss)
        if return_val_loss:
            return_values.append(val_loss)
        if return_values:
            return tuple(return_values)

    def predict(self, X):
        """
        X : numpy ndarray
            Array of size n_objects, n_features

        Returns
        -------
        y : numpy ndarray
            Array of size n_objects
        """
        preds = np.array([model.predict(X) for model in self.models])
        return (preds * self.alphas[:, None]).sum(axis=0) * self.lr
