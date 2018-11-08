import numpy as np
import pandas as pd
from sklearn.svm import SVR
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics
from sklearn.model_selection import cross_val_predict
from sklearn.tree import DecisionTreeRegressor
from sklearn.naive_bayes import GaussianNB
from sklearn import linear_model

data = pd.read_csv('pure_20tags.csv')
X = data[['Title','Genre','Summary','Year']]
Y = data[['Tag']]


X_train,X_test,Y_train,Y_test = train_test_split(X,Y,test_size=0.2,random_state=1)


#Linear model
linear_regression = LinearRegression()
linear_regression.fit(X_train,Y_train)

print linear_regression.intercept_
print linear_regression.coef_


y_pred = linear_regression.predict(X_test)


#reg = linear_model.BayesianRidge()
#reg.fit(X_train,Y_train)
#y_pred = reg.predict(X_test)
# SVR model
# svr_regression = SVR(C=16,epsilon=0.2,gamma=0.125)
# svr_regression.fit(X_train,Y_train)
# y_pred = svr_regression.predict(X_test)
# y_pred = cross_val_predict(svr_regression,X,Y,cv=10)

# DTR model
#dtr_regression = DecisionTreeRegressor(random_state=0)
# y_pred = cross_val_predict(dtr_regression,X,Y,cv=10)
#dtr_regression.fit(X_train,Y_train)
#y_pred = dtr_regression.predict(X_test)

# GNB model
#gnb_regression = GaussianNB()
#gnb_regression.fit(X_train,Y_train)
#y_pred = gnb_regression.predict(X_test)

print "MSE:",metrics.mean_squared_error(Y_test,y_pred)
print "MAE:",metrics.mean_absolute_error(Y_test,y_pred)
