from sklearn.svm import SVR
import pandas as pd
import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn import metrics
data = pd.read_csv('raw_tag.csv')
attribute_list = ["MovieID"]
for i in range(2015): #May chanege here
	attribute_list.append("Tag"+str(i))

X = data[attribute_list]
y = data["Rate"]
X_train,X_test,y_train,y_test = train_test_split(X, y, test_size=0.1, random_state=42)

linear_svr = SVR(kernel='linear')
linear_svr.fit(X_train, y_train)
y_pred = linear_svr.predict(X_test)

print "MSE:",metrics.mean_squared_error(y_test,y_pred)
print "MAE:",metrics.mean_absolute_error(y_test,y_pred)