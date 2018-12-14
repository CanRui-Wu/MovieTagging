import numpy as np
import math

def cosSimilarity(a,b):
	temp1,temp2,temp3 = 0,0,0
	for i in range(len(a)):
		temp1 += a[i]*b[i]
		temp2 += a[i]*a[i]
		temp3 += b[i]*b[i]
	return temp1/math.sqrt(temp2*temp3)

rate_matrix = np.loadtxt('mix_matrix2.txt')
final_matrix = np.zeros((rate_matrix.shape[0],rate_matrix.shape[1]))


for target in range(rate_matrix.shape[0]):
	print target
	similar_dict = dict()
	for i in range(rate_matrix.shape[0]):
		if i == target:
			continue
		else:
			similar_dict[i] = cosSimilarity(rate_matrix[target],rate_matrix[i])
	result = sorted(similar_dict.items(),key= lambda x:x[1],reverse=True)[:10]
	current = [0 for i in range(rate_matrix.shape[1])]
	for index,sim in result:
		current += sim*rate_matrix[index]
	temp = dict()
	for i in range(rate_matrix.shape[1]):
		#if rate_matrix[target][i] != 0:
		temp[i] = current[i]
		# else:
		# 	temp[i] = 0
	result = sorted(temp.items(),key= lambda x:x[1],reverse=True)[:30]
	for index,value in result:
		final_matrix[target][index] = 1

np.savetxt("final_matrix.txt",final_matrix,fmt="%d")
