#!/usr/local/bin/python3.2.1

# Feature Selection Project -- Ajit Puthenputhussery
# Input -->  main_project.py traindata trainlabels testdata


import sys # For command line arguments
sys.path.append('libsvm/python') # Append path for python interface to LibSVM 
from svmutil import *
import math # For math operations
sys.path.append('ctypes/ctypes') # For C data-type 
sys.path.append('feature_seln') # For feature selection method
from ctypes import *

# Read data

# Note : sys.argv[0] is the script name

trainfile = sys.argv[1]
trainlabels_file = sys.argv[2]
testfile = sys.argv[3]

DEBUG = 0
CROSS_VALIDATION = 1

print('Reading Data')
print('-- Reading Train File')
# Read trainfile
f = open(trainfile)
traindata = []
l = f.readline()
line_num =1;
while(l!=''):
    a = l.split()
    l2 = []
    for j in range(0,len(a),1):
        l2.append(int(a[j]))
    traindata.append(l2)
    l = f.readline()
    # print(line_num)
    # line_num = line_num + 1
f.close()

print('-- Reading Train Labels')
# Read trainlabels
f = open(trainlabels_file)
trainlabels = []
l = f.readline()
line_num =1;

while(l!=''):
    a = l.split()
    l2 = []
    for j in range(0,len(a),1):
        l2.append(int(a[j]))
    trainlabels.append(l2)
    l = f.readline()
    # print(line_num)
    # line_num = line_num + 1
f.close()

print('-- Reading Test File')
# Read testdata ----------

f = open(testfile)
testdata = []
l = f.readline()
line_num = 1

while(l!=''):
    a = l.split()
    l2 = []
    for j in range(0,len(a),1):
        l2.append(int(a[j]))
    testdata.append(l2)
    l = f.readline()
    # print(line_num)
    # line_num = line_num + 1
f.close()

if(DEBUG==1):
    print("\n Train Data")
    print(len(traindata),len(traindata[0]))
    print("Train Labels")
    print(len(trainlabels[0]))
    # print("Test Data")
    # print(len(testdata),len(testdata[0]))
	

# Feature Selection
print('\nStarting Feature Selection (mRMR)')
# Call to C Function
# Convert data to C data-type
print('-- Converting data to C array')

num_feat = 10

k = c_int(num_feat) # k -- No. of features to be selected
nS = c_int(len(traindata)) # nS -- No. of Samples
nF = c_int(len(traindata[0])) # nF -- No. of Features

# Convert traindata to C array --- column major array (each observation is column vector)
tr_arr = (c_double*len(traindata))*len(traindata[0])
tr_arr_instance = tr_arr()
for i in range(0,len(traindata)):
	for j in range(0,len(traindata[0])):
		tr_arr_instance[j][i] = traindata[i][j]
fM = pointer(tr_arr_instance) # fM -- Feature Matrix

# Convert trainlabels to C array
trl_arr = (c_double*len(trainlabels))
trl_arr_instance = trl_arr()
for i in range(0,len(trainlabels)):
	trl_arr_instance[i] = trainlabels[i][0]
cC = pointer(trl_arr_instance) # cC -- Class Column

# Create empty array for output features
a5 = [0.0]*num_feat
arr2 = c_double*len(a5)
arr_instance2 = arr2()
for i in range(0,len(a5)):
	arr_instance2[i] = a5[i]
oF = pointer(arr_instance2) # oF -- Output Features

# Call to C Function
print('-- Calling C Function')
lib = 'f_sel.so'
dll = cdll.LoadLibrary(lib)	

dll.mRMR_D.restype=POINTER(c_double*num_feat) # return type -- Pointer to Output Feature Array 

oF =dll.mRMR_D(k,nS,nF,fM,cC,oF) # Call to C Function

sel_features_d = oF.contents
sel_features = [int(y) for y in sel_features_d]
print("No. of Features selected: %d" %(num_feat) )
print('Selected Features:')
print(sel_features)
print('(Please note that the feature index starts from 0)')

# Create traindata based on selected features for SVM
sf_traindata = []
for i in range(0,len(traindata)):
	list1 = []
	for j in range(0,len(sel_features)):
		list1.extend([traindata[i][sel_features[j]]])
	sf_traindata.append(list1)

# Create trainlabels for SVM
sf_trainlabels = []
for i in range(0,len(trainlabels)):
	sf_trainlabels.extend([trainlabels[i][0]])
	
# Create testdata based on selected features for SVM	
sf_testdata = []
for i in range(0,len(testdata)):
	list2 = []
	for j in range(0,len(sel_features)):
		list2.extend([testdata[i][sel_features[j]]])
	sf_testdata.append(list2)

# Create dummy test labels for SVM 
dummy_testlabels = []
for i in range(0,2000):
	if i<1000:
		dummy_testlabels.extend([0])
	else:
		dummy_testlabels.extend([1])
	

	
# # Cross Validation Script -- 10 folds
if CROSS_VALIDATION==1:	
	print('\nStarting Cross Validation')
	# Read folds
	f = open('cross_folds')
	folds = []
	l = f.readline()

	while(l!=''):
		a = l.split()
		l2 = []
		for j in range(0,len(a),1):
			l2.append(int(a[j]))
		folds.append(l2)
		l = f.readline()
	f.close()

	accuracy = []

	for i in range(1,11,1):
		c_traindata = []
		c_tr = 0
		c_testdata = []
		c_te = 0
		c_trainlabels = []
		c_testlabels = []
		
		print('Fold %d'%i)
		
		for j in range(0,len(sf_traindata),1):
			if (folds[j][0] == i):
				c1 = sf_traindata[j][:]
				c_testdata.append(c1)
				c_testlabels.extend([trainlabels[j][0]])
			else:
				c2 = sf_traindata[j][:]
				c_traindata.append(c2)
				c_trainlabels.extend([trainlabels[j][0]])
		
		if DEBUG==1:
			print("Traindata %d %d"%(len(c_traindata),len(c_traindata[0])))
			print("Trainlabels %d %d"%(len(c_trainlabels),len(c_trainlabels[0])))
			print("Testdata %d %d"%(len(c_testdata),len(c_testdata[0])))
			print("Testlabels %d %d"%(len(c_testlabels),len(c_testlabels[0])))
		
		m = svm_train(c_trainlabels, c_traindata, '-t 0 -c 4 -q')
		p_label, p_acc, p_val = svm_predict(c_testlabels, c_testdata, m)
		accuracy.extend([p_acc[0]])

	print('Mean Accuracy = %.3f%%'%(sum(accuracy)/float(len(accuracy))))



# # Classification using SVM on complete traindata
# print('\nStarting classification using linear SVM')
# model = svm_train(sf_trainlabels, sf_traindata, '-t 0 -c 4 -q')
# p_label, p_acc, p_val = svm_predict(dummy_testlabels, sf_testdata, model, '-q')

# # Print predicted labels to output file
# filename = "output.prediction"
# f = open(filename,'w+')
# for i in range(0,len(p_label),1):
    # if (i == len(p_label)-1):
        # f.write(str(int(p_label[i]))+" "+str(i))
    # else:
        # f.write(str(int(p_label[i]))+" "+str(i)+"\n")
# f.close()

# print('Completed. Output file is: output.prediction')




	
	
		
			

