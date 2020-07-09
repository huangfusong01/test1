import threading
import queue
from functools import wraps
import time
import requests

SHARE_Q = queue.Queue()  #构造一个不限制大小的的队列
threadnb= 30 #设置线程个数


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

    def __init__(self, func, i):
        super(MyThread, self).__init__()
        self.func = func
        self.i = i

    def run(self):
        self.func()
        print("执行的线程"+str(self.i))


def worker():
    while not SHARE_Q.empty():
        url1 = 'http://sales.weaship.com.cn/operation/v1/aviationOrder/catchOrderTrackInfo/order/'
        headers = {"Content-Type": "application/json"}
        item = SHARE_Q.get() #获得任务
        fire_Path_New = url1 + item
        result = requests.get(url=fire_Path_New, headers=headers)
        #print(str(result.json()) + item)
        print(result.json)

        time.sleep(1)
        SHARE_Q.task_done()

@func_timer
def main() :
    threads=[]
    with open('D:\\PycharmProjects\\test\config\\orderId',encoding="utf-8") as f:
        for i in f.readlines():
            SHARE_Q.put(i.strip(), timeout=10)
    for i in range(threadnb):
        thread = MyThread(target=worker,name=i)
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    print(SHARE_Q.qsize())
    SHARE_Q.join()

if __name__ == '__main__':
    main()