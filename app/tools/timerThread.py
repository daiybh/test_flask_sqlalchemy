from queue import Queue
import  threading
import logging

import requests

from app.config import Config
import time

#启动一个定时线程
# 定时从任务队列里面取出任务 并执行
# 任务里面包含一个 子任务队列，并记录当前执行到哪个子任务
class TimerThread(threading.Thread):
    def __init__(self,logger) :
        threading.Thread.__init__(self)
        self.taskQueue = Queue(maxsize=5)    
        self.logger=logger  
        self.logger.debug("TimerThread init")

    def activeTask(self,task):
        self.taskQueue.put(task)

    def handle(self,runningTask):        
        #self.logger.error("aaaa")
        #newtask['loop']=0
        a = len(runningTask['data'])
        pages=int((a+3)/4)
        curPos = runningTask['loop'] %pages*4
        print(f"pages:{pages} curpos:{curPos} task:{a} loop:{runningTask['loop']}")
        runningTask['loop']+=1
        showList=[]
        for i in range(curPos,min(curPos+4,a)):            
            showList.append(runningTask['data'][i])
        

        for i in range(len(showList) ,4):
            showList.append( {'F_id': 2, 'F_message': ' ', 'F_color': 1})
        #print(showList) 
        showText=""
        for a in showList:
            showText+=f"{a['F_message']},"
        showText=showText[:-1]
        print(showText)
        #生成请求JSON
        dat={
                "ledids":"860402316010496",
                "empty_plot":showText,
                "pgmfilepath":"/home/admin/cheyun/upload/123.lsprj",
                "park_id":runningTask['park_id']
                #"fontcolor":1
            }
        
        response = requests.get(Config.LED_SERVER_EMPTY_PLOT,params=dat)
        last_update_response = response.text   
        print(last_update_response)     

        
    def run(self):
        runningTaskDict ={}
        t= threading.current_thread()
        icount=0
        while True:
            icount+=1
            try:
                newtask = self.taskQueue.get(block=True,timeout=20)
                if newtask==None:
                    break
            #把 newtask 添加到dict 中去
                print("got new task",newtask)
                newtask['loop']=0
                key = f"{newtask['park_id']}_{newtask['LED_id']}"
                runningTaskDict[key]=newtask
            except:
                pass
            #print(f"{t.ident}>>I am liveing... {time.asctime(time.localtime() ) }" )
            if len(runningTaskDict)==0:
                #print("runningTaskDict is empty")
                continue
            for k,rtask in runningTaskDict.items():
                self.handle(rtask)
            

    

      