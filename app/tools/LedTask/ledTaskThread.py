import hashlib
from queue import Queue
import  threading
import logging

import requests

from app.config import Config
import time
import os
import json
from app.tools.LedTask.lsprj_parser import generate_backImage, genrate_image

#启动一个定时线程
# 定时从任务队列里面取出任务 并执行
# 任务里面包含一个 子任务队列，并记录当前执行到哪个子任务
class LedTaskThread(threading.Thread):
    def __init__(self,logger,config,activetask_everyseconds=20):
        threading.Thread.__init__(self)
        self.taskQueue = Queue(maxsize=5)    
        self.logger=logger  
        self.config=config
        self.activetask_everyseconds= activetask_everyseconds
        self.logger.debug("TimerThread init")

    def activeTask(self,task):
        self.taskQueue.put(task)

    def handle(self,runningTask):        
        pages=len(runningTask['groupTask'])

        curPage = runningTask['loop'] %pages

        print(f"curpos:{curPage}/{pages} loop:{runningTask['loop']}")
        runningTask['loop']+=1

        curGroupTask = runningTask['groupTask'][curPage]
        empty_plot = ",".join ([l['F_message'] for l in curGroupTask])

        #生成请求JSON
        dat={
                "ledids":runningTask['LED_id'],                
                "pgmfilepath":runningTask['pgmfilepath'],
                "park_id":runningTask['park_id'],
                #"backgroundImage":runningTask['backgroundImage'],
                "empty_plot":empty_plot,
            }
        
        response = requests.get(self.config['LED_SERVER_UPDATE_EMPTY_PLOT'],params=dat)
        last_update_response = response.text  
        self.logger.debug(f"last_update_response:{last_update_response}") 
        print(last_update_response)     

    def loadTask(self):
        print("loadTask....")
        # 遍历 TASK_FOLDER 目录
        #    taskJson=app.config["TASK_FOLDER"]+f"task@{park_id}_{led_id}.json"
        task_list = []
        task_folder = self.config['TASK_FOLDER']
        for file_name in os.listdir(task_folder):
            if file_name.startswith('task@') and file_name.endswith('.json'):
                file_path = os.path.join(task_folder, file_name)
                #task_data['last_modified'] = time.ctime(os.path.getmtime(file_path))
                
                key = file_name.split('.')[0]
                with open(file_path, 'r') as file:
                
                    data = file.read()

                    md5_hash = hashlib.md5(data.encode()).hexdigest()

                    # 从文件名读出key
                    if key  in  self.runningTaskDict:
                        if self.runningTaskDict[key]['last_modified'] == task_data['last_modified']:
                            continue
                        if self.runningTaskDict[key]['md5_hash'] == md5_hash:
                            continue

                        self.runningTaskDict.pop(key)

                
                    
                    task_data = json.loads(data)
                    task_data['md5_hash'] = md5_hash
                    task_data['loop']=0
                    #生成背景图片
                    #                     
                    task_data['backgroundImage']=generate_backImage(task_data['pgmfilepath'],f'{self.config["UPLOAD_FOLDER"]}/backgournd_{key}.png')
                    # 把task_data['data'] 分解成 group task 每个group 4个task
                    groupTask=[]
                    for i in range(0,len(task_data['data']),4):
                        groupTask.append( task_data['data'][i:i+4])
                    task_data['groupTask'] = groupTask

                    self.runningTaskDict[key] = task_data
                    
                    

    def run(self):
        self.runningTaskDict ={}
        t= threading.current_thread()
        self.loopCount=0
        while True:
            self.loopCount+=1
            try:
                if self.loopCount!=1:
                    newtask = self.taskQueue.get(block=True,timeout= self.activetask_everyseconds)
                    if newtask==None:
                        break
                self.loadTask()                
            except Exception as e:
                pass
            #print(f"{t.ident}>>I am liveing... {time.asctime(time.localtime() ) }" )
            if len(self.runningTaskDict)==0:
                #print("runningTaskDict is empty")
                continue
            for k,rtask in self.runningTaskDict.items():
                try:
                    self.handle(rtask)
                except Exception as e:
                    self.logger.error(f"handle error {e}")
            

    

      