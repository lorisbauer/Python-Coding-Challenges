from copy import deepcopy

class Algorithms:
    def __init__(self, obj, delay=1):
        self.obj = obj
        self.progression = [deepcopy(self.obj) for _ in range(delay)]
    
    def selection_sort(self):
        for i in range(len(self.obj)):
            min_idx = i
            for j in range(i+1, len(self.obj)):
                if self.obj[min_idx] > self.obj[j]:
                    min_idx = j
            self.obj[i], self.obj[min_idx] = self.obj[min_idx], self.obj[i]
            self.progression.append(deepcopy(self.obj))
    
    def bubble_sort(self):
        n = len(self.obj)
        for i in range(n):
            for j in range(n-i):
                if j + 1 < n:
                    if self.obj[j] > self.obj[j + 1]:
                        self.obj[j], self.obj[j + 1] = self.obj[j + 1], self.obj[j]
                        self.progression.append(deepcopy(self.obj))
    
    def sort_pivot(self, low, high):
        i = low - 1
        pivot = self.obj[high]
    
        for j in range(low, high):
            if self.obj[j] <= pivot:   
                i = i+1
                self.obj[i], self.obj[j] = self.obj[j], self.obj[i]
                self.progression.append(deepcopy(self.obj))
    
        self.obj[i+1], self.obj[high] = self.obj[high], self.obj[i+1]
        self.progression.append(deepcopy(self.obj))
        return (i+1)
    
    def quick_sorting(self, low, high):
        if low < high:
            pi = self.sort_pivot(low, high)
            self.quick_sorting(low, pi-1)
            self.quick_sorting(pi+1, high)
    
    def quick_sort(self):
        self.quick_sorting(0, len(self.obj) - 1)

    def insertion_sort(self):
        for i in range(1, len(self.obj)):   
            key = self.obj[i]
            j = i-1
            while j >= 0 and key < self.obj[j] :
                self.obj[j+1] = self.obj[j]
                self.progression.append(deepcopy(self.obj))
                j -= 1
            self.obj[j+1] = key
            self.progression.append(deepcopy(self.obj))
             
    def merge(self, array, x1, y1, x2, y2):
        i = x1
        j = x2
        temp = []

        while i<= y1 and j<= y2:
            if array[i] < array[j]:
                temp.append(array[i])
                i += 1
            else:
                temp.append(array[j])
                j += 1
        
        while i<= y1:
            temp.append(array[i])
            i += 1

        while j<= y2:
            temp.append(array[j])
            j += 1

        j = 0

        for i in range(x1, y2 + 1):
            array[i] = temp[j]
            self.progression.append(deepcopy(array))
            j += 1

    def merge_sorting(self, array, l, r):
        mid = (l + r)//2
        if l<r:
            self.merge_sorting(array, l, mid)
            self.merge_sorting(array, mid + 1, r)
            self.merge(array, l, mid, mid + 1, r)
    
    def merge_sort(self):
        self.merge_sorting(self.obj, 0, len(self.obj) - 1)

    def heapify(self, n, i):
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2
    
        if l < n and self.obj[i] < self.obj[l]:
            largest = l
    
        if r < n and self.obj[largest] < self.obj[r]:
            largest = r
    
        if largest != i:
            self.obj[i], self.obj[largest] = self.obj[largest], self.obj[i]  # swap
            self.progression.append(deepcopy(self.obj))
            self.heapify(n, largest)
    
    def heap_sort(self):
        n = len(self.obj)
        for i in range(n//2 - 1, -1, -1):
            self.heapify(n, i)
    
        for i in range(n-1, 0, -1):
            self.obj[i], self.obj[0] = self.obj[0], self.obj[i]
            self.progression.append(deepcopy(self.obj))
            self.heapify(i, 0)
    
    def shell_sort(self):
        n = len(self.obj)
        gap = n//2
        while gap > 0:
            for i in range(gap, n):
                temp = self.obj[i]
                j = i
                while  j >= gap and self.obj[j-gap] >temp:
                    self.obj[j] = self.obj[j - gap]
                    self.progression.append(deepcopy(self.obj))
                    j -= gap

                self.obj[j] = temp
                self.progression.append(deepcopy(self.obj))
            gap = gap//2
    
    def counting_sort(self, exp1):    
        n = len(self.obj)
        output = [0] * (n)
        count = [0] * (10)
    
        for i in range(0, n):
            index = self.obj[i]//exp1
            count[index % 10] += 1
    
        for i in range(1, 10):
            count[i] += count[i - 1]
    
        i = n - 1
        while i >= 0:
            index = self.obj[i]//exp1
            output[count[index % 10] - 1] = self.obj[i]
            count[index % 10] -= 1
            i -= 1
    
        i = 0
        for i in range(0, len(self.obj)):
            self.obj[i] = output[i]
            self.progression.append(deepcopy(self.obj))
 
    def radix_sort(self):   
        max1 = max(self.obj)
        exp = 1
        while max1 / exp > 1:
            self.counting_sort(exp)
            exp *= 10


if __name__ == '__main__':
    test = [2, 3, 1, 5, 3, 7, 9, 4]
    algo = Algorithms(test)
    algo.shell_sort()
    print(algo.progression)