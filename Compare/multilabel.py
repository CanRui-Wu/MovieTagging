import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cross_validation import train_test_split
from sklearn.metrics import precision_recall_fscore_support
from skmultilearn.problem_transform import BinaryRelevance
from sklearn.svm import SVC
from skmultilearn.adapt import MLkNN
from sklearn.metrics import precision_score
from skmultilearn.problem_transform import LabelPowerset
from skmultilearn.problem_transform import BinaryRelevance
from skmultilearn.problem_transform import ClassifierChain
from skmultilearn.neurofuzzy import MLARAM
from sklearn.naive_bayes import GaussianNB
from sklearn import tree
from sklearn.linear_model import SGDClassifier
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

data = pd.read_csv('new_film_embedded.csv')
test_data = pd.read_csv('top250_film_embedded.csv')

attribute_list = ["Country1","Country2","Genre1","Genre2","Genre3","Genre4"]
tag_list = []
for i in range(200):
	attribute_list.append("Summary" + str(i+1)) 
for i in range(200):
	attribute_list.append("Title" + str(i+1)) 
for i in range(2015):
	tag_list.append("Tag"+str(i+1))

X_train = np.matrix(data[attribute_list])
Y_train = np.matrix(data[tag_list])
X_test = np.matrix(test_data[attribute_list])
Y_test = np.matrix(test_data[tag_list])

top250_id_list = []
with open('top250.txt') as f:
	for line in f.readlines():
		top250_id_list.append(line[:-1].decode('utf-8'))

tag_list = []
with open('douban_tag.txt') as f:
	for line in f.readlines():
		tag_list.append(line[:-1].decode('utf-8'))


classifier = MLkNN(k=100)
#classifier = MLARAM()
#classifier = LabelPowerset(classifier = SVC(), require_dense = [False, True])
#classifier = ClassifierChain(GaussianNB())
#classifier = ClassifierChain(SGDClassifier())
#classifier = LabelPowerset(tree.DecisionTreeClassifier(),require_dense = [False, False])
#classifier = ClassifierChain(tree.DecisionTreeClassifier())
#classifier = BinaryRelevance(classifier = SVC(), require_dense = [False, True])

print "Start Training"
classifier.fit(X_train, Y_train)
y_pred = classifier.predict(X_test)

movie_tag_dict = dict()

for i in range(246):
	movie_tag_dict[top250_id_list[i]] = []
	for j in range(2015):
		if y_pred[i,j] == 1:
			movie_tag_dict[top250_id_list[i]].append(tag_list[j])

f = open('new_KNN100.json','w')
f.write(json.dumps(movie_tag_dict,ensure_ascii=False,sort_keys=True, indent=2))
f.close()
