# import pandas as pd
# import numpy as np
# import random
# from sklearn.linear_model import LinearRegression

# def cost(x,y,theta0,theta1):
# 	total_error = 0
# 	for i in range(len(x)):
# 		total_error += (x[i]*theta1+theta0-y[i])*(x[i]*theta1+theta0-y[i])
# 	return (total_error)/(2*len(x))

# def update(x,y,theta0,theta1):

# 	i = random.randint(0,len(x)-1)
# 	temp1 = x[i]*theta1+theta0-y[i]
# 	temp2 = (x[i]*theta1+theta0-y[i])*x[i]

# 	theta0 = theta0-0.000001*temp1
# 	theta1 = theta1-0.000001*temp2
# 	print theta0,theta1
# 	return theta0,theta1


# def gradient_descent(x,y,theta0,theta1):
# 	while True:
# 		pre_cost = cost(x,y,theta0,theta1)
# 		theta0,theta1 = update(x,y,theta0,theta1)
# 		current_cost = cost(x,y,theta0,theta1)
# 		print current_cost
# 		if abs(current_cost - pre_cost) < 0.000001:
# 			print theta0
# 			print theta1
# 			return

# pga = pd.read_csv('pga.csv')
# gradient_descent(pga.distance,pga.accuracy,0,0)
# # lr = LinearRegression()
# # lr.fit(pga[['distance']],pga['accuracy'])
# # theta0 = lr.intercept_
# # thet1 = lr.coef_
# # print theta0,thet1
