import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pandas as pd


class LinearRegression(object):
    def __init__(self, learning_rate, n_iter):
        self.mu = learning_rate
        self.n_iter = n_iter

        self.W = None
        self.C = []

    def fit(self, X, y):
        self.W = np.random.RandomState().normal(loc=0, scale=0.01, size=(X.shape[1], 1))
        self.C.append(self.cost(X, y))

        for _ in range(0, self.n_iter):
            self.W = self.W - self.mu * (np.matmul(np.transpose(X), np.dot(X, self.W) - y))
            self.C.append(self.cost(X, y))

        return self.C

    def cost(self, X, y):
        return sum((1/y.shape[0])*np.square(np.dot(X, self.W) - y))

    def predict(self, X):
        return np.round(np.dot(X, self.W))


df = pd.read_csv('https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv', sep=';')

X = np.hstack((df.iloc[:, 0:11].values, np.ones((df.shape[0], 1))))
y = df.iloc[:, 11].values.reshape((df.shape[0], 1))

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, stratify=y)

lr = LinearRegression(learning_rate=0.0000001, n_iter=100)
# lr = LinearRegression(learning_rate=0.0001, n_iter=50)
costs = lr.fit(X_train, y_train)
plt.scatter(x=range(0, 101), y=costs)
plt.show()

print('Accuracy = ', 100 * np.sum(lr.predict(X_test) == y_test)/y_test.shape[0], '%')
print('Average Error = ', np.average(np.abs(lr.predict(X_test) - y_test)))
