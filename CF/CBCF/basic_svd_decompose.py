import numpy as np
import random

def computeTwoNormSquare(vector):
	result = 0
	for i in range(len(vector)):
		result += vector[i]*vector[i]
	return result

def computeCost(rate_list,rate_matrix,b_u_list,b_i_list,u,user_matrix,item_matrix,lambda_1,lambda_2,lambda_3,lambda_4):
	total_error = 0
	for i,j in rate_list:
		ground_truth = rate_matrix[i][j]
		predict = u+b_u_list[i]+b_i_list[j]+user_matrix[i].dot(item_matrix[j])
		total_error += (ground_truth-predict)*(ground_truth-predict) + lambda_1*b_u_list[i]*b_u_list[i]+lambda_2*b_i_list[j]*b_i_list[j]+\
			lambda_3*computeTwoNormSquare(user_matrix[i])+lambda_4*computeTwoNormSquare(item_matrix[j])
	return total_error

def stochasticGradient(rate_list,rate_matrix,b_u_list,b_i_list,u,user_matrix,item_matrix,lambda_1,lambda_2,lambda_3,lambda_4):
	previous_cost = computeCost(rate_list,rate_matrix,b_u_list,b_i_list,u,user_matrix,item_matrix,lambda_1,lambda_2,lambda_3,lambda_4)
	print previous_cost
	for i in range(20000000):
		index = random.randint(0,len(rate_list)-1)
		user_index = rate_list[index][0]
		item_index = rate_list[index][1]
		ground_truth = rate_matrix[user_index][item_index]
		predict = u+b_u_list[user_index]+b_i_list[item_index]+user_matrix[user_index].dot(item_matrix[item_index])
		previous_user_vector = user_matrix[user_index]
		previous_item_vector = item_matrix[item_index]
		b_u_list[user_index] += 0.001*(ground_truth-predict-lambda_1*b_u_list[user_index])
		b_i_list[item_index] += 0.001*(ground_truth-predict-lambda_2*b_i_list[item_index])
		# user_matrix[user_index] = previous_user_vector+0.01*((ground_truth-predict)*previous_item_vector-lambda_3*previous_user_vector)
		# item_matrix[item_index] = previous_item_vector+0.01*((ground_truth-predict)*previous_user_vector-lambda_4*previous_item_vector)
		user_matrix[user_index] = previous_user_vector+0.001*((ground_truth-predict)*previous_item_vector-lambda_3*previous_user_vector)
		item_matrix[item_index] = previous_item_vector+0.001*((ground_truth-predict)*previous_user_vector-lambda_4*previous_item_vector)
		if i%1000000 == 0:
			current_cost = computeCost(rate_list,rate_matrix,b_u_list,b_i_list,u,user_matrix,item_matrix,lambda_1,lambda_2,lambda_3,lambda_4)
			print i,current_cost
		#previous_cost = current_cost
	print "Final Cost: "+str(computeCost(rate_list,rate_matrix,b_u_list,b_i_list,u,user_matrix,item_matrix,lambda_1,lambda_2,lambda_3,lambda_4))

def getFinalResult(rate_matrix,b_u_list,b_i_list,u,user_matrix,item_matrix):
	for i in range(rate_matrix.shape[0]):
		for j in range(rate_matrix.shape[1]):
			rate_matrix[i][j] = u+b_u_list[i]+b_i_list[j]+user_matrix[i].dot(item_matrix[j])
	print b_u_list
	print b_i_list
	np.savetxt('bu_last.txt',b_u_list,fmt="%.4f")
	np.savetxt('bi_last.txt',b_i_list,fmt="%.4f")
	np.savetxt('user_last.txt',user_matrix,fmt="%.4f")
	np.savetxt('item_last.txt',item_matrix,fmt="%.4f")
	# print user_matrix
	# print item_matrix
	np.savetxt('basic_svd_matrix_last.txt',rate_matrix,fmt="%.4f")


if __name__ == '__main__':
	print "Starting Load Rating Matrix"
	rate_matrix = np.loadtxt('../Data/matrix2.txt')
	#rate_matrix = np.ones((100,100))
	random.seed(0)
	# rate_matrix[0][1] = 0
	# rate_matrix[0][0] = 2
	# rate_matrix[2][2] = 0
	print "Starting Caculate Average Rating u"
	movie_count = rate_matrix.shape[0]
	tag_count = rate_matrix.shape[1]
	np.random.seed(0)
	user_matrix = np.random.random((movie_count,50))
	item_matrix = np.random.random((tag_count,50))
	b_u_list = np.random.random(movie_count)
	b_i_list = np.random.random(tag_count)
	user_matrix = user_matrix/1000
	item_matrix = item_matrix/1000
	b_u_list = b_u_list/1000
	b_i_list = b_i_list/1000
	print b_u_list

	rate_list = []
	total = 0
	for i in range(movie_count):
		for j in range(tag_count):
			if rate_matrix[i][j] != 0:
				# b_u_list[i] += rate_matrix[i][j]
				# b_i_list[j] += rate_matrix[i][j]
				rate_list.append((i,j))
				total += rate_matrix[i][j]
	u = total/float(movie_count*tag_count)
	# for i in range(movie_count):
	# 	b_u_list[i] = b_u_list[i]/tag_count
	# 	b_u_list[i] -= u
	# for i in range(tag_count):
	# 	b_i_list[i] = b_i_list[i]/movie_count
	# 	b_i_list[i] -= u
	stochasticGradient(rate_list,rate_matrix,b_u_list,b_i_list,u,user_matrix,item_matrix,0.01,1,0.01,0.01)
	getFinalResult(rate_matrix,b_u_list,b_i_list,u,user_matrix,item_matrix)
