import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

dataset = pd.read_csv("Position_Salaries.csv")

X = dataset.iloc[:, 1:-1].values
y = dataset.iloc[:, -1].values

linear_regressor = LinearRegression()
linear_regressor.fit(X, y)

poly_regressor = PolynomialFeatures(degree=4)
X_poly = poly_regressor.fit_transform(X)

linear_regressor_2 = LinearRegression()
linear_regressor_2.fit(X_poly, y)

linear_prediction = linear_regressor.predict([[6.5]])
polynomial_prediction = linear_regressor_2.predict(poly_regressor.transform([[6.5]]))

print("Linear Regression Prediction:", linear_prediction)
print("Polynomial Regression Prediction:", polynomial_prediction)

plt.scatter(X, y)
plt.plot(X, linear_regressor.predict(X))
plt.title("Linear Regression")
plt.xlabel("Position Level")
plt.ylabel("Salary")
plt.show()

plt.scatter(X, y)
plt.plot(X, linear_regressor_2.predict(X_poly))
plt.title("Polynomial Regression")
plt.xlabel("Position Level")
plt.ylabel("Salary")
plt.show()