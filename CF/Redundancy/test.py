import numpy as np
import os

def cosSimilarity(a,b):
	return np.vdot(a,b)/(np.linalg.norm(a)*np.linalg.norm(b))



print "Loading rating matrix"
rate_matrix = np.loadtxt('../Data/hot_matrix.txt')
similar_matrix = np.zeros((rate_matrix.shape[0],rate_matrix.shape[0]))

if os.path.exists("similar_matrix.txt"):
	print "Loading similar matrix"
	with open('similar_matrix.txt') as f:
		for i,line in enumerate(f.readlines()):
			print i
			for j,value in enumerate(line.split(' ')):
				similar_matrix[i][j] = float(value)
else:
	print "Caculating Similar_matrix"
	for i in range(rate_matrix.shape[0]):
		print i
		for j in range(i+1,rate_matrix.shape[0]):
			result = cosSimilarity(rate_matrix[i],rate_matrix[j])
			similar_matrix[i][j] = result
			similar_matrix[j][i] = result
	np.savetxt("similar_matrix.txt",similar_matrix,fmt="%.4f")

print "Calculating result"
iteration = 1

for n in range(iteration):
	for j in range(rate_matrix.shape[1]):
		print j
		rate_matrix[:,j] = np.dot(similar_matrix,rate_matrix[:,j].reshape(-1,1)).reshape(-1)
		# max_val,min_val = rate_matrix[:,j].max(),rate_matrix[:,j].min()
		# rate_matrix[:,j] = (rate_matrix[:,j]-min_val)/(max_val-min_val)

np.savetxt('redundancy_matrix.txt',rate_matrix,fmt="%.4f")
