import numpy as np


class Perceptron(object):
    
    
    def __init__(self, c=0.01, n_iter=100):
        self.c = c
        self.n_iter = n_iter

    
    def fit(self, X, xy):
        
        self.weights = np.zeros(1 + X.shape[1])
        self.errors_ = []

        for _ in range(self.n_iter):
            errors = 0
            for xi, target in zip(X, xy):
                update = self.c * (target - self.predict(xi))
                self.weights[1:] += update * xi
                self.weights += update
                errors += int(update != 0.0)
            self.errors_.append(errors)
        return self

    
    def net_input(self, X):
        """Calculate net input"""
        return np.dot(X, self.weights[1:]) + self.weights[0]

    
    def predict(self, X):
        """Return class label after unit step"""
        return np.where(self.net_input(X) >= 0.0, 1, -1)
