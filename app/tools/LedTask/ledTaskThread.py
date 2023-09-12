from queue import Queue
import  threading
import logging

import requests

from app.config import Config
import time

from app.tools.LedTask.lsprj_parser import genrate_image

#启动一个定时线程
# 定时从任务队列里面取出任务 并执行
# 任务里面包含一个 子任务队列，并记录当前执行到哪个子任务
class LedTaskThread(threading.Thread):
    def __init__(self,logger,activetask_everyseconds=20):
        threading.Thread.__init__(self)
        self.taskQueue = Queue(maxsize=5)    
        self.logger=logger  
        self.activetask_everyseconds= activetask_everyseconds
        self.logger.debug("TimerThread init")

    def activeTask(self,task):
        self.taskQueue.put(task)

    def handle(self,runningTask):        
        pages=len(runningTask['pngPath'])

        curPage = runningTask['loop'] %pages

        print(f"curpos:{curPage}/{pages} loop:{runningTask['loop']}")
        runningTask['loop']+=1
        #生成请求JSON
        dat={
                "ledids":runningTask['LED_id'],                
                "pgmfilepath":runningTask['pgmfilepath'],
                "park_id":runningTask['park_id'],
                "imagepath":runningTask['pngPath'][curPage]
            }
        
        response = requests.get(Config.LED_SERVER_UPDATE_WITH_IMAGE,params=dat)
        last_update_response = response.text  
        self.logger.debug(f"last_update_response:{last_update_response}") 
        print(last_update_response)     

        
    def run(self):
        runningTaskDict ={}
        t= threading.current_thread()
        icount=0
        while True:
            icount+=1
            try:
                newtask = self.taskQueue.get(block=True,timeout= self.activetask_everyseconds)
                if newtask==None:
                    break
            #把 newtask 添加到dict 中去
                print("got new task",newtask)
                newtask['loop']=0
                key = f"{newtask['park_id']}_{newtask['LED_id']}"
                
                pngPath=genrate_image(newtask['pgmfilepath'],newtask["data"],f'{Config.UPLOAD_FOLDER}/image_{key}')
                
                newtask['pngPath']=pngPath

                newtask['backGroundImage']=genrate_image(newtask['pgmfilepath'],f'{Config.UPLOAD_FOLDER}/backgournd_{key}.png')

                runningTaskDict[key]=newtask
            except:
                pass
            #print(f"{t.ident}>>I am liveing... {time.asctime(time.localtime() ) }" )
            if len(runningTaskDict)==0:
                #print("runningTaskDict is empty")
                continue
            for k,rtask in runningTaskDict.items():
                self.handle(rtask)
            

    

      