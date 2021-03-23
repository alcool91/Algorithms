# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 22:05:21 2021

@author: Allen
"""

import PythonTrees.Dictionary as PT
import random
import math 
from scipy.stats import truncnorm
import timeit
import matplotlib.pyplot as plt

RADIUS = 1000 

default_dict_times_insert = []
tree_dict_times_insert = []


default_dict = {}
tree_dict    = PT.Dictionary()

def createLists(size, radius=RADIUS):
    ins_arr = [i for i in range(size)]
    random.shuffle(ins_arr)
    mrg_arr = ins_arr.copy()
    return (ins_arr, mrg_arr)

def createListsTruncatedNormal(size, t, radius=RADIUS, limit='sorted'):
    """
    Creates list pulling each element from a truncated normal distribution where the mean (of the normal distribution the TND is derived from) for the element at index i
    is (i-RADIUS) * 2*RADIUS/(size-1). As t approaches 1 the list will approach a sorted list, and as t approaches 0 the list approaches a uniformly random list.
    
    If descending is true, the mean of the distributions will be chosen in reverse order, the list will range from uniformly random (t=0) to reverse sorted (t->1)

    t is a scale parameter in the interval (0,1)
    as t->0 the distribution approaches a uniform distribution
    as t->1 the distribution approaches a degenerate distribution at the mean
    """
    assert(0 <= t < 1)
    if t == 0:
        return createLists(size)
    myclip_a = -radius
    myclip_b = radius
    #my_mean = mean
    my_std = (1/t)-1
    
    #a, b = (myclip_a - my_mean) / my_std, (myclip_b - my_mean) / my_std
    #ins_arr = [math.floor(truncnorm.rvs(a,b, loc=my_mean, scale=my_std, size = size))]
    if limit == 'reversesorted':
        ins_arr = [math.floor(truncnorm.rvs((myclip_a - (int(round(((-2*RADIUS)/(size-1))))*i+RADIUS))/my_std,(myclip_b - (int(round(((-2*RADIUS)/(size-1))))*i+RADIUS))/my_std,loc=(int(round(((-2*RADIUS)/(size-1))))*i+RADIUS), scale=my_std)[0]) for i in range(size)]
        mrg_arr = ins_arr.copy()
    elif limit == 'sorted':
        ins_arr = [math.floor(truncnorm.rvs((myclip_a - (int(round(((2*RADIUS)/(size-1))))*i-RADIUS))/my_std,(myclip_b - (int(round(((2*RADIUS)/(size-1))))*i-RADIUS))/my_std,loc=(int(round(((2*RADIUS)/(size-1))))*i-RADIUS), scale=my_std)[0]) for i in range(size)]
        mrg_arr = ins_arr.copy()
    else:
        ins_arr = [math.floor(truncnorm.rvs(myclip_a, myclip_b, loc=0, scale=my_std)) for i in range(size)]
        mrg_arr = ins_arr.copy()
    return (ins_arr, mrg_arr)
    

def test_default_dict_insert(arr):
    for i in range(len(arr)):
        default_dict[arr[i]] = i
    #print(default_dict)
    #print("insertion test: ", len(arr), " complete")
    
def test_tree_dict_insert(arr):
    for i in range(len(arr)):
        tree_dict.insert((arr[i], i))
    #print(tree_dict)

recent_times_d, recent_times_t = 0, 0
i = 5
while recent_times_d < 3 and recent_times_t < 3:

    default_dict = {}
    tree_dict    = PT.Dictionary()
    l1, l2 = createLists(i)
    default_dict_times_insert.append((i, timeit.timeit('test_default_dict_insert(l1)', 'from __main__ import l1, l2, test_default_dict_insert, default_dict', number=1)))
    tree_dict_times_insert.append((i, timeit.timeit('test_tree_dict_insert(l2)', 'from __main__ import l1, l2, test_tree_dict_insert, tree_dict', number=1)))
    recent_times_d = default_dict_times_insert[-1][1]
    recent_times_t = tree_dict_times_insert[-1][1]
    i += 250_000
    
plt.plot([default_dict_times_insert[i][0] for i in range(len(default_dict_times_insert))], [default_dict_times_insert[i][1] for i in range(len(default_dict_times_insert))], 'b-',
                 [tree_dict_times_insert[i][0] for i in range(len(tree_dict_times_insert))], [tree_dict_times_insert[i][1] for i in range(len(tree_dict_times_insert))], 'r-')
plt.title("Tree vs Hash Table based Dictionary Insertion")
plt.xlabel("Size of List")
plt.ylabel("Time (seconds)")
plt.legend(['Hash Table', 'Tree'])
plt.show()
    
print('i: ', i)
print('d: ', recent_times_d)
print('t: ', recent_times_t)