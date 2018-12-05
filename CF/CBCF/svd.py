#-*-encoding:utf-8-*-
import tensorflow as tf
import numpy as np
import random

if __name__ == '__main__':
	print "Starting Load Rating Matrix"
	#rate_matrix = np.loadtxt('../Data/matrix1.txt')
	rate_matrix = np.ones((100,100))
	random.seed(0)
	# rate_matrix[0][1] = 0
	# rate_matrix[0][0] = 2
	# rate_matrix[2][2] = 0
	print "Starting Caculate Average Rating u"
	movie_count = rate_matrix.shape[0]
	tag_count = rate_matrix.shape[1]
	rate_index_list = []
	rate_list = []
	total = 0
	for i in range(movie_count):
		for j in range(tag_count):
			if rate_matrix[i][j] != 0:
				rate_index_list.append([i,j])
				rate_list.append(rate_matrix[i][j])
				total += rate_matrix[i][j]
	u = float(total)/(movie_count*tag_count)
	x_data = np.array(rate_index_list)
	y_data = np.array(rate_list)[:,None]
	print u
	u = 0

	u = tf.constant(u,dtype=tf.float64)
	x = tf.placeholder(tf.int32,[None,2],name="X")
	y = tf.placeholder(tf.float64,[None,1],name="Y")
	# b_user = tf.Variable(tf.random.uniform([movie_count,1],-1,1,dtype=tf.float32),name="b_user")
	# b_item = tf.Variable(tf.random.uniform([tag_count,1],-1,1,dtype=tf.float32),name="b_item")
	# p = tf.Variable(tf.random.uniform([movie_count,5],-1,1,dtype=tf.float32),name="user_matrix")
	# q = tf.Variable(tf.random.uniform([tag_count,5],-1,1,dtype=tf.float32),name="item_matrix")
	b_user = tf.Variable(np.full((movie_count,1),0.001),name="b_user")
	b_item = tf.Variable(np.full((tag_count,1),0.001),name="b_item")
	p = tf.Variable(np.full((movie_count,10),0.001),name="user_matrix")
	q = tf.Variable(np.full((tag_count,10),0.001),name="item_matrix")

	

	# implicit_feedback = tf.Variable(tf.random.uniform([tag_count,tag_count],-1,1,dtype=tf.float32,name="implicit_feedback"))
	# m3_matrix = tf.constant(m3_matrix)
	# test = tf.constant([[2,3],[1]])

	# c_ui = tf.nn.embedding_lookup(b_user,x[:,0])
	# c_ui = tf.nn.embedding_lookup(tf.transpose(c_ui),x[:,1])

	target_b_user = tf.nn.embedding_lookup(b_user,x[:,0])
	target_b_item = tf.nn.embedding_lookup(b_item,x[:,1])

	target_p = tf.nn.embedding_lookup(p,x[:,0])
	target_q = tf.nn.embedding_lookup(q,x[:,1])

	target_p = tf.reshape(target_p,[-1,1,10])
	target_q = tf.reshape(target_q,[-1,10,1])
	temp = tf.matmul(target_p,target_q)
	temp = tf.reshape(temp,[-1,1])
	predict = u+target_b_user+target_b_item+temp
	print predict.shape.as_list()
	# 最小化方差
	#loss = tf.reduce_mean(tf.square(y - predict))
	loss = tf.reduce_sum(tf.square(y-predict))
	optimizer = tf.train.GradientDescentOptimizer(0.05,use_locking=True)
	train = optimizer.minimize(loss)


	# 初始化变量
	init = tf.initialize_all_variables()

	# 启动图 (graph)
	sess = tf.Session()
	with sess.as_default():
		sess.run(init)
		for step in xrange(0, 2000):
			index = random.randint(0,len(x_data)-1)
			#print index
			print sess.run(loss,feed_dict={x:x_data,y:y_data})
			sess.run(train,feed_dict={x:x_data[index:index+1],y:y_data[index:index+1]})
			
	print sess.run(b_user)
	print sess.run(b_item)
	print sess.run(p[0])
	print sess.run(q[0])
	