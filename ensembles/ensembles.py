import numpy as np
from sklearn.tree import DecisionTreeRegressor
from scipy.optimize import minimize_scalar


class RandomForestMSE:
    def __init__(self, n_estimators, max_depth=None,
                 feature_subsample_size=None, random_state=0,
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
        """
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.max_features = feature_subsample_size
        self.trees_parameters = trees_parameters
        self.models = []

    def fit(self, X, y, X_val=None, y_val=None):
        """
        X : numpy ndarray
            Array of size n_objects, n_features

        y : numpy ndarray
            Array of size n_objects

        X_val : numpy ndarray
            Array of size n_val_objects, n_features

        y_val : numpy ndarray
            Array of size n_val_objects           
        """
        if self.max_features is None:
            self.max_features = max(1, X.shape[1] // 3)
        rng = np.random.default_rng()
        for _ in range(self.n_estimators):
            idx = rng.choice(len(y), len(y))
            model = DecisionTreeRegressor(max_depth=self.max_depth,
                                          max_features=self.max_features,
                                          **self.trees_parameters)
            model.fit(X[idx], y[idx])
            self.models.append(model)

    def predict(self, X):
        """
        X : numpy ndarray
            Array of size n_objects, n_features

        Returns
        -------
        y : numpy ndarray
            Array of size n_objects
        """
        y = np.zeros(shape=X.shape[0], dtype=float)
        for model in self.models:
            y += model.predict(X)
        y /= X.shape[0]


class GradientBoostingMSE:
    def __init__(self, n_estimators, learning_rate=0.1, max_depth=5, feature_subsample_size=None,
                 **trees_parameters):
        """
        n_estimators : int
            The number of trees in the forest.
        
        learning_rate : float
            Use learning_rate * gamma instead of gamma
        max_depth : int
            The maximum depth of the tree. If None then there is no limits.
        
        feature_subsample_size : float
            The size of feature set for each tree. If None then use recommendations.
        """
        pass
        
    def fit(self, X, y, X_val=None, y_val=None):
        """
        X : numpy ndarray
            Array of size n_objects, n_features
            
        y : numpy ndarray
            Array of size n_objects
        """
        pass

    def predict(self, X):
        """
        X : numpy ndarray
            Array of size n_objects, n_features
            
        Returns
        -------
        y : numpy ndarray
            Array of size n_objects
        """
        pass
