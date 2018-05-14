import sys
sys.path.append('libsvm/python') # Append path for python interface to LibSVM 
from svmutil import *

# Read data in LIBSVM format
y, x = svm_read_problem('libsvm/heart_scale') # This will still be from the outer directory
print(type(y))
print(y)
print('----------------------------------')
print(type(x[0]))
print(x)
m = svm_train(y[:200], x[:200], '-c 4')
p_label, p_acc, p_val = svm_predict(y[200:], x[200:], m)
