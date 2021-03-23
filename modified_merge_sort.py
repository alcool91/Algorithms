from sorting.insertion_sort import insertionSort
#random import only used in the driver
#import random

def mod_merge_sort(l,sw):
    assert(sw > 0)
    if len(l) <= sw:
        insertionSort(l)
        return
    pivot = len(l)//2
    left, right = l[:pivot], l[pivot:]
    mod_merge_sort(left, sw)
    mod_merge_sort(right, sw)

    k = 0
    while len(left) > 0 and len(right) > 0:
        if left[0] < right[0]:
            l[k] = left.pop(0)
        else:
            l[k] = right.pop(0)
        k += 1

    rest = left + right
    while len(rest) > 0:
        l[k] = rest.pop(0)
        k += 1

#Driver to test the implementation
# arr = [random.randint(-1000,1000) for i in range(500)]
# mod_merge_sort(arr, 20) 
# print(arr == sorted(arr))
# for i in range(len(arr)): 
#     print ("%d" %arr[i]) 