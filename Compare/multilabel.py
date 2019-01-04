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

train_data = pd.read_csv('../Similarity/train_film_embedded.csv')
test_data = pd.read_csv('../Similarity/test_film_embedded.csv')

attribute_list = []
tag_list = []
# for i in range(477):
# 	attribute_list.append("Country" + str(i+1)) 
# for i in range(50):
# 	attribute_list.append("Genre" + str(i+1))
for i in range(200):
	attribute_list.append("Summary" + str(i+1))
for i in range(200):
	attribute_list.append("Title" + str(i+1)) 
for i in range(2015):
	tag_list.append("Tag"+str(i+1))

X_train = np.matrix(train_data[attribute_list])
Y_train = np.matrix(train_data[tag_list])
X_test = np.matrix(test_data[attribute_list])
Y_test = np.matrix(test_data[tag_list])
train_id = train_data["Id"]
test_id = test_data["Id"]


tag_list = []
with open('../Crawler/allow_tag.txt') as f:
	for line in f.readlines():
		tag_list.append(line[:-1].decode('utf-8'))


#classifier = MLkNN(k=100)
#classifier = MLARAM()
#classifier = LabelPowerset(classifier = SVC(), require_dense = [False, True])
#classifier = ClassifierChain(GaussianNB())
#classifier = ClassifierChain(SGDClassifier())
classifier = LabelPowerset(tree.DecisionTreeClassifier(),require_dense = [False, False])
#classifier = ClassifierChain(tree.DecisionTreeClassifier())
#classifier = BinaryRelevance(classifier = SVC(), require_dense = [False, True])

print "Start Training"
classifier.fit(X_train, Y_train)
y_train_pred = classifier.predict(X_train)
y_test_pred = classifier.predict(X_test)

movie_tag_dict = dict()

for i in range(len(train_id)):
	movie_tag_dict[train_id[i]] = []
	for j in range(2015):
		if y_train_pred[i,j] == 1:
			movie_tag_dict[train_id[i]].append(tag_list[j])

for i in range(len(test_id)):
	movie_tag_dict[test_id[i]] = []
	for j in range(2015):
		if y_test_pred[i,j] == 1:
			movie_tag_dict[test_id[i]].append(tag_list[j]) 

f = open('LT.json','w')
f.write(json.dumps(movie_tag_dict,ensure_ascii=False,sort_keys=True, indent=2))
f.close()
