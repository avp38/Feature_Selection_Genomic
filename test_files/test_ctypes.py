import sys
sys.path.append('/afs/cad.njit.edu/courses/ccs/f15/cs/675/001/avp38/course_project/ctypes/ctypes') 
sys.path.append('feature_seln') 
from ctypes import *

# To create C data-type
a = c_double(12.5)
print(a)
b = c_int(1)
print(b)

# To create pointer
i = c_int(2)
pi = pointer(i)
print(i)
print(pi)

a1 = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]
arr = (c_double*len(a1[0]))*len(a1)
arr_instance = arr()
for i in range(0,len(a1)):
	for j in range(0,len(a1[0])):
		arr_instance[i][j] = a1[i][j]
		print(arr_instance[i][j])


# Call to C Function
print('Call to C Function')
lib = 'test_func.so'
dll = cdll.LoadLibrary(lib)

dll.custom_change_array.argtypes=[POINTER(c_int)]
#                ^^^^^^^^^^^^^^^^
#         One argument of type `int *̀

dll.custom_change_array.restype=c_int
# return type 

res =dll.custom_change_array(pi)
#            ^^^^^^^^^
#       cast to an array of 5 int

print(res)


k = c_int(2)
nS = c_int(5)
nF = c_int(4)

a3 = [[1,1,2,1],[2,3,4,4],[10,12,12,13],[7,7,8,7],[5,5,4,6]]
arr = (c_double*len(a3[0]))*len(a3)
arr_instance = arr()
for i in range(0,len(a3)):
	for j in range(0,len(a3[0])):
		arr_instance[i][j] = a3[i][j]
		print(arr_instance[i][j])
fM = pointer(arr_instance)

a4 = [0,0,1,1,1]
arr1 = c_double*len(a4)
arr_instance1 = arr1()
for i in range(0,len(a4)):
	arr_instance1[i] = a4[i]
cC = pointer(arr_instance1)

a5 = [0,0]
arr2 = c_double*len(a5)
arr_instance2 = arr2()
for i in range(0,len(a5)):
	arr_instance2[i] = a5[i]
oF = pointer(arr_instance2)

# To create the .so file combine the .o files of folder FEST and MIToolbox to a single folder (folder name) --> (feature_seln).
# Then use command (to create shared libraries) --> gcc -shared -o f_sel.so feature_seln/*.o  

# Call to C Function
print('Call to C Function')
lib = 'f_sel.so'
dll = cdll.LoadLibrary(lib)

# To fix this include the array definition for all the POINTER arguments
# dll.mRMR_D.argtypes=[c_int,c_int,c_int,POINTER(c_double),POINTER(c_double),POINTER(c_double)]
#                ^^^^^^^^^^^^^^^^
#         One argument of type `int *̀

dll.mRMR_D.restype=POINTER(c_double*2)
# return type 

oF =dll.mRMR_D(k,nS,nF,fM,cC,oF)
#            ^^^^^^^^^
#       cast to an array of 5 int

print(oF)
a6 = oF.contents
# print(a6)
print(a6[0])
print(a6[1])

