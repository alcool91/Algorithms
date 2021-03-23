# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 20:13:27 2021

@author: Allen
"""

import sorting.merge_sort
import sorting.insertion_sort
import timeit
import random
import math
from scipy.stats import truncnorm
import numpy as np
import matplotlib.pyplot as plt

RADIUS = 1000 
MAX_LIST_SIZE = 125
ITERATIONS = 5
NUMBER = 10

size_time_ins = []
size_time_mrg = []

def worstCaseArrayOfSize(n):
    """ Generate an array as bad as possible for merge sort
    Algorithm from Morgan Wilde
    https://stackoverflow.com/a/33409294
    """
    if n == 1:
        return [1]
    else:
        top = worstCaseArrayOfSize(int(math.floor(float(n) / 2)))
        bottom = worstCaseArrayOfSize(int(math.ceil(float(n) / 2)))
        return list(map(lambda x: x * 2, top)) + list(map(lambda x: x * 2 - 1, bottom))


def createLists(size, radius=RADIUS):
    ins_arr = [random.randint(-radius, radius) for i in range(size)]
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
        temp = worstCaseArrayOfSize(size)
        ins_arr = [math.floor(truncnorm.rvs((myclip_a - (int(round(((2*RADIUS)/(size-1))))*temp[i]-RADIUS))/my_std,(myclip_b - (int(round(((2*RADIUS)/(size-1))))*temp[i]-RADIUS))/my_std,loc=(int(round(((2*RADIUS)/(size-1))))*temp[i]-RADIUS), scale=my_std)[0]) for i in range(size)]
        mrg_arr = ins_arr.copy()
    return (ins_arr, mrg_arr)

def test_insertion_sort(arr):
    sorting.insertion_sort.insertionSort(arr)
    #print("insertion test: ", len(arr), " complete")
    
def test_merge_sort(arr):
    sorting.merge_sort.merge_sort(arr)
    #print("merge test: ", len(arr), " complete")

t_vals = [0, 0.000001, 0.001, 0.002, 0.0035, 0.005, 0.01, 0.1, 0.25, 0.5, 0.75, 0.99, 0.9999]
d_vals = [('sorted', ' (Ascending)'), ('reversesorted', ' (Descending)'), ('worstcasemerge', ' (Worst for Merge)')]

for d in d_vals:    
    for t in t_vals:
        for list_size in range(5, MAX_LIST_SIZE, 5):
            #ins_arr, mrg_arr = createLists(list_size)
            ins_arr, mrg_arr = createListsTruncatedNormal(list_size, t, limit = d[0])
            size_time_mrg.append((list_size, min(timeit.repeat('test_merge_sort(mrg_arr.copy())', 'from __main__ import RADIUS, ITERATIONS, mrg_arr, createLists, test_merge_sort', number=NUMBER, repeat=ITERATIONS))/NUMBER))
            size_time_ins.append((list_size, min(timeit.repeat('test_insertion_sort(ins_arr.copy())', 'from __main__ import RADIUS, ITERATIONS, ins_arr, createLists, test_insertion_sort', number=NUMBER, repeat=ITERATIONS))/NUMBER))
        
        
        plt.plot([size_time_ins[i][0] for i in range(len(size_time_ins))], [size_time_ins[i][1] for i in range(len(size_time_ins))], 'b-',
                 [size_time_mrg[i][0] for i in range(len(size_time_mrg))], [size_time_mrg[i][1] for i in range(len(size_time_mrg))], 'r-')
        plt.title("Insertion Sort vs Merge Sort: t=" + str(t) + d[1])
        plt.xlabel("Size of List")
        plt.ylabel("Time (seconds)")
        plt.legend(['Insertion Sort', 'Merge Sort'])
        plt.show()
        plt.clf()
        size_time_ins = []
        size_time_mrg = []
        print("done for t=", t)