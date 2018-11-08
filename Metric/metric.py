import sys
import os
import json

def getResult(extract_list,real_list):
	extract_set = set(extract_list)
	real_set = set(real_list)
	if len(extract_set) == 0:
		return 0,0,0
	correct_number = float(len(extract_set&real_set))
	return correct_number/len(extract_set),correct_number/len(real_set),correct_number


if __name__ == '__main__':
	if len(sys.argv) != 3:
		print "Please input correct args"
		os.exit(1)
	f = open(sys.argv[1])
	extract_tag_dict = json.load(f)
	f.close()
	f = open(sys.argv[2])
	douban_tag_dict = json.load(f)
	f.close()
	total_precision = 0
	total_recall = 0
	extract_count = 0
	real_count = 0
	total_correct = 0.0
	count = 0
	for movie in extract_tag_dict:
		if not douban_tag_dict.has_key(movie):
			continue
		if len(douban_tag_dict[movie]) == 0:
			continue
		count += 1
		precision,recall,number = getResult(extract_tag_dict[movie][:100],douban_tag_dict[movie])
		total_precision += precision
		total_recall += recall
		extract_count += len(extract_tag_dict[movie])
		real_count += len(douban_tag_dict[movie])
		total_correct += number
		print movie + " precision: " + str(precision) + ",recall: " + str(recall) 
	print "Total " + str(total_precision/count) + " " + str(total_recall/count)
	print "Micro Total" + str(total_correct/extract_count) + " " + str(total_correct/real_count)
