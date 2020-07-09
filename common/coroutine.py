import grequests
import time
import asyncio,aiohttp
from multiprocessing import Process,cpu_count,Pool
import os

def runTime(func):
    def func1(*args, **kwargs):
        s = time.time()
        res = func(*args, **kwargs)
        print('--> RUN TIME: <%s> ' % ( time.time() - s))
    return  func1

@runTime
def use_grequests(num=100):
    print(1)
    task = []
    urls = ["http://101.200.123.214/time" for i in range(num)]
    while urls:
        url = urls.pop(0)
        rs = grequests.request("GET", url,timeout=5)
        task.append(rs)
    resp = grequests.map(task, size=100)
    print('task  (pid={}) is running '.format(os.getpid()))


async def fetch_async(url,semaphore):
    async with semaphore:  # 这里进行执行asyncio.Semaphore，
        conn = aiohttp.TCPConnector(limit=0)  # 同时最大进行连接的连接数为30，默认是100，limit=0的时候是无限制
        async with aiohttp.ClientSession(connector=conn) as session:
            async with session.get(url,headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}) as resp:
                if resp.status != 200:
                    print(str(resp.status)+('task  (pid={}) is running '.format(os.getpid())) )
                #time.sleep(1)


def run(num=1000):
    loop = asyncio.get_event_loop()
    tasks_only = [ ]
    #while True:
    semaphore = asyncio.Semaphore(500)
    for _ in range(num):
        tasks_only.append(fetch_async(url='http://101.200.123.214/time',semaphore=semaphore))  #http://49.235.160.132:8000/login
    #http://192.168.7.120:8889/time   本地
    #阿里 http://101.200.123.214/time  ali
    #while True:
        #tasks_only.append(fetch_async(url='http://101.200.123.214/time'))
    loop.run_until_complete(asyncio.wait(tasks_only))
    loop.close()

@runTime
def main():
    process_list = []
    #cpuNum = cpu_count()
    for _ in range(3):
        process_list.append(Process(target=run))
    for _ in process_list:
        _.start()
    for _ in process_list:
        _.join()

if __name__ == '__main__':
    #  p=Pool(processes=3) #进程池
    #  for i in range(3): #线程
    #      p.apply_async(run)  # annotation 3
    #  print('waiting for all processes end')
    # # # close the pool
    #  p.close()  # p.close() to excute the pool
    #  # block the main process
    #  p.join()

    main()

    # Process(target=run(100)).start()


    #print(1)
    #p1.join()
    #p2.join()
    #use_grequests(100)
    #run()
