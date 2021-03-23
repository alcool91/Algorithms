# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 00:15:34 2021

@author: Allen
"""

from scipy.stats import truncnorm
import statistics
import matplotlib.pyplot as plt 
import numpy as np
import math


# Python3 program to count  
# inversions in an array 
  
def getInvCount(arr): 
  
    n = len(arr)
    inv_count = 0
    for i in range(n): 
        for j in range(i + 1, n): 
            if (arr[i] > arr[j]): 
                inv_count += 1
  
    return inv_count 
  
# # Driver Code 
# arr = [1, 20, 6, 4, 5] 
# n = len(arr) 
# print("Number of inversions are", 
#               getInvCount(arr, n)) 
  
# This code is contributed by Smitha Dinesh Semwal 

def toStd(t):
    return((1/t)-1)

#fig, ax = plt.subplots(1,1)

myclip_a = -1000
myclip_b = 1000
my_mean = -800
t       = 0.000001   # 0<t<=1
my_std = (1/t)-1
t_vals = [0.002, 0.01, 0.1, 0.35,0.5, 0.75, 0.99]


a, b = (myclip_a - my_mean) / my_std, (myclip_b - my_mean) / my_std

mean, var, skew, kurt = truncnorm.stats(a, b, moments='mvsk')

#x = np.linspace(truncnorm.ppf(0.01, a, b, loc=my_mean, scale=my_std), truncnorm.ppf(0.99,a,b, loc=my_mean, scale=my_std), 100)
x = np.linspace(-1000, 1000, 50000)
#ax.set_ylim([0,1])
# plt.plot(x, truncnorm.pdf(x,a,b, loc=my_mean, scale=toStd(t_vals[0])), 'r-', x, truncnorm.pdf(x,a,b, loc=my_mean, scale=toStd(t_vals[1])), 'b-', 
#         x, truncnorm.pdf(x,a,b, loc=my_mean, scale=toStd(t_vals[2])), 'g-', x, truncnorm.pdf(x,a,b, loc=my_mean, scale=toStd(t_vals[3])), 'y-',
#         x, truncnorm.pdf(x,a,b, loc=my_mean, scale=toStd(t_vals[4])), 'c-', x, truncnorm.pdf(x,a,b, loc=my_mean, scale=toStd(t_vals[5])), 'k-', lw=1, alpha=0.6, label='truncnorm.pdf')
colors = ['r-', 'b-', 'g-', 'y-', 'c-', 'k-']
plt.ylim(0,.01)
#for i in range(len(t_vals)):
for i in range(1):
    a, b = (myclip_a - my_mean) / toStd(t_vals[i]), (myclip_b - my_mean) / toStd(t_vals[i])
    plt.plot(x, truncnorm.pdf(x,a,b, loc=my_mean, scale=toStd(t_vals[i])), colors[i], lw=1, alpha=0.6)

# a, b = (myclip_a - my_mean) / toStd(t_vals[0]), (myclip_b - my_mean) / toStd(t_vals[0])
# plt.plot(x, truncnorm.pdf(x,a,b, loc=my_mean, scale=toStd(t_vals[0])), colors[0], lw=1, alpha=0.6, label='truncnorm.pdf')
plt.title('Truncated Normal Distribution with Mean -800 on [-1000,1000]')
plt.xlabel("x")
plt.ylabel('f(x)')
plt.legend(['t='+str(t_vals[i]) for i in range(len(t_vals))])
plt.show()


RANGE = 20
# #print(truncnorm.rvs(a,b, loc=my_mean, scale=my_std, size = 10))
print([int(round(((2000)/(RANGE-1))))*i-1000 for i in range(RANGE)])
# #nums = [math.floor(truncnorm.rvs((myclip_a - (int(round(((2000)/(RANGE-1))))*i-1000))/my_std,(myclip_b - (int(round(((2000)/(RANGE-1))))*i-1000))/my_std,loc=(int(round(((2000)/(RANGE-1))))*i-1000), scale=my_std)[0]) for i in range(RANGE)]
# means = [(int(round(((-2000)/(RANGE-1))))*i+1000) for i in range(RANGE)]
# print(means)
# nums = [math.floor(truncnorm.rvs((myclip_a - (int(round(((-2000)/(RANGE-1))))*i+1000))/my_std, (myclip_b - (int(round(((-2000)/(RANGE-1))))*i+1000))/my_std, loc=(int(round(((-2000)/(RANGE-1))))*i+1000), scale=my_std)[0]) for i in range(RANGE)]
# print("*"*20)
# print("t: ", t)
# print('Avg: ', statistics.mean(nums))
# print('Min: ', min(nums))
# print('Max: ', max(nums))
# print('Inversions: ', getInvCount(nums))
# print("*"*20)
# #print(nums)