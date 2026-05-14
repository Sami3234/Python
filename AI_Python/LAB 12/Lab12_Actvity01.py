import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# Importing the dataset
dataset = pd.read_csv(r"C:\Users\SamiKhan\Documents\GitHub\Python\AI_Python\LAB 12\Salary_Data.csv")
X = dataset.iloc[:, :-1].values
y = dataset.iloc[:, -1].values

# Splitting the dataset into the Training set and Test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=1/3, random_state=0)

# Training the Simple Linear Regression model on the Training set
regressor = LinearRegression()
regressor.fit(X_train, y_train)

# Predicting the Test set results
y_pred = regressor.predict(X_test)

# Visualising the Training set results
plt.scatter(X_train, y_train, color='red')
plt.plot(X_train, regressor.predict(X_train), color='blue')
plt.title('Salary vs Experience (Training set)')
plt.xlabel('Years of Experience')
plt.ylabel('Salary')
plt.show()

# Visualising the Test set results
plt.scatter(X_test, y_test, color='red')
plt.plot(X_train, regressor.predict(X_train), color='blue')
plt.title('Salary vs Experience (Test set)')
plt.xlabel('Years of Experience')
plt.ylabel('Salary')
plt.show()

# Visualising Test Results using X_test and y_pred
plt.scatter(X_test, y_test, color='red')
plt.plot(X_test, y_pred, color='blue')
plt.title('Salary vs Experience (Test set)')
plt.xlabel('Years of Experience')
plt.ylabel('Salary')
plt.show()

# Making a single prediction (for example: 12 years of experience)
single_prediction = regressor.predict([[12]])
print("Prediction for 12 years experience:", single_prediction)

# Coefficient and Intercept
coefficient = regressor.coef_
intercept = regressor.intercept_
print("Coefficient:", coefficient)
print("Intercept:", intercept)

# Extra Practice: Manual vs Auto prediction for 15 years
manual_prediction = intercept + coefficient[0] * 15
print("Manual prediction (15 years):", manual_prediction)

auto_prediction = regressor.predict([[15]])
print("Auto prediction (15 years):", auto_prediction)
