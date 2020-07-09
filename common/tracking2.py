import threading
import queue
from functools import wraps
import time
import requests


SHARE_Q = queue.Queue()  #构造一个不限制大小的的队列
threadnb= 40 #设置线程个数


def func_timer(function):
    @wraps(function)
    def function_timer(*args, **kwargs):
        print('[Function: {name} start...]'.format(name = function.__name__))
        t0 = time.time()
        result = function(*args, **kwargs)
        t1 = time.time()
        print ('[Function: {name} finished, spent time: {time:.2f}s]'.format(name = function.__name__,time = t1 - t0))
        return result
    return function_timer

class MyThread(threading.Thread) :

    def __init__(self,i):
        super(MyThread, self).__init__()
        self.i = i

    def run(self):
        while not SHARE_Q.empty():
            url1 = 'http://sales.17feia.com/operation/v1/aviationOrder/catchOrderTrackInfo/order/'
            headers = {"Content-Type": "application/json"}
            item = SHARE_Q.get()  # 获得任务
            fire_Path_New = url1 + item
            result = requests.get(url=fire_Path_New, headers=headers)
            print(str(result.json()) + str(self.i))
            time.sleep(1)
            SHARE_Q.task_done()



@func_timer
def main() :
    threads=[]
    with open('D:\\PycharmProjects\\test\config\\insiderNumber1') as f:
        for i in f.readlines():
            SHARE_Q.put(i.strip(), timeout=5)
        print(SHARE_Q.qsize())
    for i in range(threadnb):
        thread = MyThread(i)
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    SHARE_Q.join()
    print(SHARE_Q.qsize())


if __name__ == '__main__':
    main()