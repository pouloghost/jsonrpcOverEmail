'''
    a heap class
    an initial array of data and a cmp function can be passed in
    by changing cmp
    this heap can fit different objects
    and be either a max heap or a min one

    functions are:
    build heap
    insert
    delete
    get extremum
    pop extremum
    show(4 debug)
'''

class PriorQueue:      
    def __init__(self, arr = [], cmp = lambda a, b: a - b):
        import copy
        self.__heap = copy.deepcopy(arr)
        self.__cmp = cmp
        self.heapify()

    def __del__(self):
        pass

    def _fix_up(self, i):
        me = self.__heap[i]
        while(i > 0):
            p = (i + 1)//2 - 1
            if(self.__cmp(self.__heap[p], me) > 0):
                self.__heap[i] = self.__heap[p]
                i = p
            else:
                break
        self.__heap[i] = me
        
    def _fix_down(self, i):
        me = self.__heap[i]
        size = len(self.__heap)
        while(i < size):
            c = 2 * (i + 1) - 1
            if(c >= size):
                break
            if(c + 1 < size and \
               self.__cmp(self.__heap[c], self.__heap[c + 1]) > 0):
                c = c + 1
            if(self.__cmp(me , self.__heap[c]) > 0):
                self.__heap[i] = self.__heap[c]
                i = c
            else:
                break
        self.__heap[i] = me 

    def heapify(self):
        size = len(self.__heap)
        for i in reversed(range(size//2)):
            self._fix_down(i)
            
    def insert(self, v):
        self.__heap.append(v)
        i = len(self.__heap) - 1
        self._fix_up(i)
        
    def delete(self, i):
        self.__heap[i] = self.__heap[-1]
        del self.__heap[-1]
        self._fix_down(i)
        
    def get_extremum(self):
        extremum = None
        if(0 != self.size()):
            extremum = self.__heap[0]
        return extremum
    
    def pop_extremum(self):
        m = self.get_extremum()
        if(m != None):
            self.delete(0)
        return m

    def size(self):
        return len(self.__heap)

    def clear(self):
        size = self.size()
        for i in range(size):
            del self.__heap[0]
    
    def show(self):
        print(self.__heap)
        
if __name__ == '__main__':
    arr = [0,3,2,4,1,5,7,8,6]
    queue = PriorQueue(arr = arr)
    queue.show()
    queue.insert(-1)
    queue.show()
    print(queue.pop_extremum())
    queue.show()
        
