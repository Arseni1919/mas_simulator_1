from GLOBALS import *

arr = np.array([[1,2,3],[4,5,6]])
ts = arr.tostring()
str2 = str(arr)
print('[[1 2 3]\n [4 5 6]]' == str2)
print(np.fromstring(ts, dtype=int))