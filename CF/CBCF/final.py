import numpy as np
import random
import json

def computeTwoNormSquare(vector):
	result = 0
	for i in range(len(vector)):
		result += vector[i]*vector[i]
	return result

def computeCost(rate_list,rate_matrix,b_u_list,b_i_list,u,user_matrix,item_matrix,feedback_latent_matrix,feedback_dict,implict_latent_matrix,implict_dict,lambda_1):
	total_error = 0
	for i,j in rate_list:
		ground_truth = rate_matrix[i][j]
		final_item_embedding = item_matrix[j]
		for k,index in enumerate(implict_dict[i][0]):
			final_item_embedding += implict_dict[i][1][k]*implict_latent_matrix[index]
		predict = u+b_u_list[i]+b_i_list[j]+user_matrix[i].dot(final_item_embedding)
		for index in feedback_dict[i]:
			predict += feedback_latent_matrix[j][index]
			total_error += lambda_1*feedback_latent_matrix[j][index]*feedback_latent_matrix[j][index]
		total_error += (ground_truth-predict)*(ground_truth-predict) + lambda_1*(b_u_list[i]*b_u_list[i]+b_i_list[j]*b_i_list[j]+\
			computeTwoNormSquare(user_matrix[i])+computeTwoNormSquare(item_matrix[j])+computeTwoNormSquare(final_item_embedding-item_matrix[j]))
	return total_error

def stochasticGradient(rate_list,rate_matrix,b_u_list,b_i_list,u,user_matrix,item_matrix,feedback_latent_matrix,feedback_dict,implict_latent_matrix,implict_dict,lambda_1):
	for i in range(2000000):
		index = random.randint(0,len(rate_list)-1)
		user_index = rate_list[index][0]
		item_index = rate_list[index][1]
		ground_truth = rate_matrix[user_index][item_index]
		final_item_embedding = item_matrix[j]
		for k,index in enumerate(implict_dict[i][0]):
			final_item_embedding += implict_dict[i][1][k]*implict_latent_matrix[index]
		predict = u+b_u_list[i]+b_i_list[j]+user_matrix[i].dot(final_item_embedding)
		for feedback_latent_index in feedback_dict[user_index]:
			predict += feedback_latent_matrix[item_index][feedback_latent_index]
		for feedback_latent_index in feedback_dict[user_index]:
			feedback_latent_matrix[item_index][feedback_latent_index] += 0.01*(ground_truth-predict-lambda_1*feedback_latent_matrix[item_index][feedback_latent_index])
		previous_user_vector = user_matrix[user_index]
		previous_item_vector = item_matrix[item_index]
		b_u_list[user_index] += 0.01*(ground_truth-predict-lambda_1*b_u_list[user_index])
		b_i_list[item_index] += 0.01*(ground_truth-predict-lambda_1*b_i_list[item_index])
		user_matrix[user_index] = previous_user_vector+0.01*((ground_truth-predict)*previous_item_vector-lambda_1*previous_user_vector)
		item_matrix[item_index] = previous_item_vector+0.01*((ground_truth-predict)*previous_user_vector-lambda_1*previous_item_vector)
		if i%100000 == 0:
			current_cost = computeCost(rate_list,rate_matrix,b_u_list,b_i_list,u,user_matrix,item_matrix,feedback_latent_matrix,feedback_dict,lambda_1)
			print i,current_cost
		previous_cost = current_cost

def getFinalResult(rate_matrix,b_u_list,b_i_list,u,user_matrix,item_matrix,feedback_latent_matrix,feedback_dict,implict_latent_matrix,implict_dict):
	result_matrix = np.ones(rate_matrix.shape)
	for i in range(result_matrix.shape[0]):
		for j in range(result_matrix.shape[1]):
			final_item_embedding = item_matrix[j]
			for k,index in enumerate(implict_dict[i][0]):
				final_item_embedding += implict_dict[i][1][k]*implict_latent_matrix[index]
			result_matrix[i][j] = u+b_u_list[i]+b_i_list[j]+user_matrix[i].dot(final_item_embedding)
			for index in feedback_dict[i]:
				result_matrix[i][j] += feedback_latent_matrix[j][index]

	np.savetxt('cbcf_matrix.txt',result_matrix,fmt="%.4f")


if __name__ == '__main__':
	print "Starting Load Rating Matrix"
	rate_matrix = np.loadtxt('../Data/matrix1.txt')
	#rate_matrix = np.ones((3,3))
	print "Starting Load Feedback Matrix"
	#feedback_matrix = np.ones((3,3))
	feedback_matrix = np.loadtxt('../Data/matrix3.txt')
	print "Starting Build R(u)"
	feedback_dict = dict()
	for i in range(feedback_matrix.shape[0]):
		feedback_dict[i] = []
		for j in range(feedback_matrix.shape[1]):
			if feedback_matrix[i][j] != 0:
				feedback_dict[i].append(j)
	print "Starting Load Similar Relation"
	with open('../xx.json') as f:
		implict_dict = json.load(f)

	random.seed(0)
	print "Starting Caculate Average Rating u"
	movie_count = rate_matrix.shape[0]
	tag_count = rate_matrix.shape[1]
	user_matrix = np.random.random((movie_count,100))
	item_matrix = np.random.random((tag_count,100))
	implict_latent_matrix = np.random.random((tag_count,100))
	feedback_latent_matrix = np.random.random((tag_count,tag_count))
	b_u_list = np.random.random(movie_count)
	b_i_list = np.random.random(tag_count)
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
	stochasticGradient(rate_list,rate_matrix,b_u_list,b_i_list,u,user_matrix,item_matrix,feedback_latent_matrix,feedback_dict,implict_latent_matrix,implict_dict,0.1)
	getFinalResult(rate_matrix,b_u_list,b_i_list,u,user_matrix,item_matrix,feedback_latent_matrix,feedback_dict,implict_latent_matrix,implict_dict)
