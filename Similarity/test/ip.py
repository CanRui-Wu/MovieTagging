#-*-encoding:utf-8-*-
import json
import random
import math
import copy
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def calCost(solution,compare):
	cost = 0
	for tag_index_list,value in compare:
		temp = 0
		for tag_index in tag_index_list:
			temp += solution[tag_index] #0,1相乘，只要都为1的那部分
		cal_similarity = 0
		if temp != 0:
			cal_similarity = 1.0/(float(100+len(tag_index_list))/temp-1)
		cost += abs(value-cal_similarity)
	return cost

def variation(solution):
	while True:
		random_index1 = random.randint(0,len(solution)-1)
		random_index2 = random.randint(0,len(solution)-1)
		if solution[random_index1] != solution[random_index2]:
			solution[random_index1],solution[random_index2] = solution[random_index2],solution[random_index1] #变异，随机替换一个标签
			break

def cross(solution1,solution2):
	random_index1 = random.randint(0,len(solution1)-1)
	random_index2 = random.randint(random_index1,len(solution1)-1)
	if random_index1 == random_index2:
		return
	solution1_index_list = list()
	solution2_index_list = list()
	for i in range(random_index1,random_index2+1):
		if solution1[i] == 1:
			solution1_index_list.append(i)
		if solution2[i] == 1:
			solution2_index_list.append(i)
	if len(solution1_index_list) == len(solution2_index_list):
		for i in range(random_index1,random_index2+1):
			solution1[i],solution2[i] = solution2[i],solution1[i]
	elif len(solution1_index_list) < len(solution2_index_list):
		for i in range(random_index1,random_index2+1):
			solution1[i] = 0
		for i in random.sample(solution2_index_list,len(solution1_index_list)):
			solution1[i] = 1
	else:
		for i in range(random_index1,random_index2+1):
			solution2[i] = 0
		for i in random.sample(solution1_index_list,len(solution2_index_list)):
			solution2[i] = 1

def validate(solution):
	total = 0
	for i in range(len(solution)):
		total += solution[i]
	print total 


f = open('similar_film_1000')
similar_film_dict = json.load(f)
f.close()


# f = open('douban_tag.txt')
# tag_list = []
# tag_index_map = dict()
# for i,line in enumerate(f.readlines()):
# 	tag_index_map[line[:-1].decode('utf-8')] = i
# 	tag_list.append(line[:-1])
# f.close()

f = open('combine_tag.json')
movie_tag_dict = json.load(f)
f.close()

result = dict() #final_result

for movie_id in similar_film_dict:
	similar_film_list = similar_film_dict[movie_id]

	tag_index_map = dict()
	tag_list = []
	count = 0

	compare = []
	for each in similar_film_list:
		film_id = each[0]
		similarity = each[1]
		temp = []
		for tag in movie_tag_dict[film_id]:
			if not tag_index_map.has_key(tag):
				tag_index_map[tag] = count
				tag_list.append(tag)
				count += 1
			temp.append(tag_index_map[tag])
		compare.append((temp,similarity))

	solution_list = []
	solution_number = 50
	for i in range(solution_number):
		solution = [0 for i in range(len(tag_index_map))]
		index = range(len(tag_index_map))
		random_index = index
		random.shuffle(random_index)
		random_index = random_index[:100]
		for index in random_index:
			solution[index] = 1
		solution_list.append(solution)

	best_value = 1000
	best_solution = None
	for n in range(500):
		solution_cost_dict = dict()	
		for i,solution in enumerate(solution_list):
			value = calCost(solution,compare)
			solution_cost_dict[i] = value
			if value < best_value:
				best_value = value
				best_solution = solution
		sorted_result = sorted(solution_cost_dict.items(),key=lambda x:x[1])
		new_solution_list = []
		for i,value in sorted_result[:len(sorted_result)/2]:
			new_solution_list.append(copy.deepcopy(solution_list[i]))
			new_solution_list.append(copy.deepcopy(solution_list[i]))
		solution_list = new_solution_list
		for i in range(len(solution_list)):
			random_index1 = random.randint(0,len(solution_list)-1)
			random_index2 = random.randint(0,len(solution_list)-1)
			if random_index1 == random_index2:
				continue
			cross(solution_list[random_index1],solution_list[random_index2])
		for solution in solution_list:
			variation(solution)
		print best_value

	temp = []
	for i in range(len(best_solution)):
		if best_solution[i] == 1:
			temp.append(tag_list[i])
	result[movie_id] = temp

f = open('ga_all_result.json','w')
f.write(json.dumps(result,ensure_ascii=False,sort_keys=True, indent=2))
f.close()
 
