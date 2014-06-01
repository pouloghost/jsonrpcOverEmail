'''
    a timer that can executes repeating tasks
    can specify the start @time, @interval, @delay when creating a task
'''
import priorQueue as queue
import sched, threading, time
class Task:
    def __init__(self, run, time = time.time(), params = None, interval = -1, delay = 0):
        self.__run = run
        self.time = time + delay
        self.__params = params
        self.__interval = interval

    def run(self):
        if(None != self.__params):
            self.__run(self.__params)
        else:
            self.__run()
        self._update_time()
        
    def _update_time(self):
        if(self.__interval > 0):
            self.time += self.__interval

    def repeatable(self):
        return self.__interval > 0
        
class Timer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.__queue = queue.PriorQueue(cmp = lambda a, b: a.time - b.time)
        self.__cur = None #current task
        self.__event = threading.Event()
        self.__event.clear()
        self.__lock = threading.Lock()
        self.__stop = False
        self.start()
        
    def run(self):
        while(not self.__stop):
            if(self.__cur == None):
                self.__lock.acquire()
                self.__cur = self.__queue.get_extremum()
                self.__lock.release()
                if(self.__cur == None): #empty queue wait for new task added
                    self.__event.wait()
                    self.__event.clear()
            else: #an existing task
                diff = self.__cur.time - time.time()
                if(diff <= 0): #need to be execute
                    self.__cur.run()
                    self.__lock.acquire()
                    #update queue
                    if(self.__cur.repeatable()):
                        self.__queue._fix_down(0)
                    else:
                        self.__queue.pop_extremum()
                    self.__lock.release()
                    #no task to execute
                    self.__cur = None
                else: #time is not up
                    self.__lock.acquire()
                    if(self.__cur != self.__queue.get_extremum()):
                        self.__cur = None
                    self.__lock.release()
                    if(self.__cur == None):
                        continue
                    self.__event.wait(diff)
                    self.__event.clear()
            
    def cancel(self):
        self.__stop = True
        self.__event.set()
        
    def add(self, task):
        self.__lock.acquire()
        self.__queue.insert(task)
        self.__lock.release()
        self.__event.set()

def run(params = None):
    if(params == None):
        params = ''
    print(time.time(), params)
    
if __name__ == '__main__':
    timer = Timer()
    task = Task(run, interval = 1)
    timer.add(task)
    time.sleep(3)
    t = Task(run, time = time.time() + 1, params = 'ddd')
    timer.add(t)
    time.sleep(3)
    timer.cancel()
