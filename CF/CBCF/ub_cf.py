import numpy as np
import math

def cosSimilarity(a,b):
	return np.vdot(a,b)/(np.linalg.norm(a)*np.linalg.norm(b))

rate_matrix = np.loadtxt('../Data/hot_matrix.txt')
final_matrix = np.zeros((rate_matrix.shape[0],rate_matrix.shape[1]))
similar_matrix = np.zeros((rate_matrix.shape[0],rate_matrix.shape[0]))

print "Caculating Similar_matrix"
for i in range(rate_matrix.shape[0]):
	print i
	for j in range(i+1,rate_matrix.shape[0]):
		result = cosSimilarity(rate_matrix[i],rate_matrix[j])
		similar_matrix[i][j] = result
		similar_matrix[j][i] = result

print "Collecting result"
for target in range(rate_matrix.shape[0]):
	print target
	similar_dict = dict()
	for i in range(rate_matrix.shape[0]):
		if i == target:
			continue
		else:
			similar_dict[i] = similar_matrix[target][i]
	result = sorted(similar_dict.items(),key= lambda x:x[1],reverse=True)[:10]
	current = [0 for i in range(rate_matrix.shape[1])]
	for index,sim in result:
		current += sim*rate_matrix[index]
	temp = dict()
	for i in range(rate_matrix.shape[1]):
		temp[i] = current[i]

	result = sorted(temp.items(),key= lambda x:x[1],reverse=True)[:30]
	for index,value in result:
		final_matrix[target][index] = 1

np.savetxt("ub_matrix.txt",final_matrix,fmt="%d")
