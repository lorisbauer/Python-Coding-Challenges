import random
import numpy as np
from time import perf_counter


def binarySearch(array, num):
    split = len(array) // 2
    if array[split] == num:
        return split
    if array[split] > num:
        return binarySearch(array[:split], num)
    elif array[split] < num:
        return binarySearch(array[split + 1:], num) + split + 1


if __name__ == '__main__':
    length = 1000000
    array = np.sort(np.random.choice(range(length * 5), replace=False, size=(1, length)))[-1]
    num = random.choice(array)
    start = perf_counter()
    index = binarySearch(array, num)
    search_time = perf_counter() - start

    print(f'Length of array: {len(array)}')
    print(f'Index of {num}: {index}')
    print(f'Search Time: {search_time}s')
