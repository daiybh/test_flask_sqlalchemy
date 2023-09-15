import hashlib
from queue import Queue
import  threading
import logging

import requests
from app.config import Config
import time
import os
import json

from app.tools.LedTask.lsprj_parser import convert_file_to_json


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
        self.logger.debug(f"activeTask:{task}")
        self.taskQueue.put(task)

    def handle(self,runningTask):        
        pages=len(runningTask['groupTask'])

        curPage = runningTask['loop'] %pages

        #print(f"curpos:{curPage}/{pages} loop:{runningTask['loop']}")
        runningTask['loop']+=1

        curGroupTask = runningTask['groupTask'][curPage]

        for task in curGroupTask:
            if 'F_size' not in task:
                task['F_size']=15

        #生成请求JSON
        dat={
                "LED_id":runningTask['LED_id'],                
                "pgmfilepath":runningTask['pgmfilepath'],
                "park_id":runningTask['park_id'],
                "background":runningTask['backgroundImage']            ,
                "led_info":runningTask['led_info'],
                "data":curGroupTask
            }
        
        print("dat:",dat['LED_id'],curGroupTask)
        try:
            response = requests.post(self.config['LED_SERVER_UPDATE_CONTENT'],json=dat)
        
            last_update_response = response.json()
        except Exception as e:
            print("the response is not json")
            print(e)
            print(response.text)

        #self.logger.debug(f"last_update_response:{last_update_response}") 
        #print(last_update_response)     
    def loadATask(self,file_path,file_name):
        key = file_name.split('.')[0]
        #result = db.session.query(Led.ledid,Led.park_id).filter(Led.ledid==led_id).filter(Led.park_id==park_id).all() 
        #if len(result)<1:
        #    return
        with open(file_path, 'r') as file:        
            data = file.read()
            md5_hash = hashlib.md5(data.encode()).hexdigest()

            # 从文件名读出key
            if key  in  self.runningTaskDict:
                #if self.runningTaskDict[key]['last_modified'] == task_data['last_modified']:
                #    continue
                if self.runningTaskDict[key]['md5_hash'] == md5_hash:                    
                    return
                self.runningTaskDict.pop(key)

            self.logger.debug(f"load task {file_path}")
            task_data = json.loads(data)
            task_data['md5_hash'] = md5_hash
            task_data['loop']=0
            #生成背景图片
            #                     
            task_data['backgroundImage']=self.config["BACKGROUND_IMG_PATH"]
            lsprjJson = convert_file_to_json(task_data['pgmfilepath'])
            
            ledJson= lsprjJson["LEDS"]["LED"]

            task_data["led_info"]={
                        "LedType":int(ledJson['@LedType'])+1,
                        "LedWidth":int(ledJson['@LedWidth']),
                        "LedHeight":int(ledJson['@LedHeight']),
                        "LedColor":int(ledJson['@LedColor'])+1,
                        "LedGray":int(ledJson['@LedGray'])+1
                    }

            groupTask=[]
            for i in range(0,len(task_data['data']),4):
                gt =task_data['data'][i:i+4]
                for i in range(len(gt),4):
                    temp= {
                    "F_id":7,
                    "F_message":"",
                    "F_color":0xff,
                    "F_size":14
                    }
                    gt.append(temp)
                groupTask.append(gt )
            task_data['groupTask'] = groupTask

            self.runningTaskDict[key] = task_data


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
                try:
                    self.loadATask(file_path,file_name)
                except Exception as e:
                    self.logger.error(f"loadATask error {e}")
                
                    
                    

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
            print(f"{t.ident}>>I am liveing... {time.asctime(time.localtime() ) }   {len(self.runningTaskDict)}" )
            if len(self.runningTaskDict)==0:
                #print("runningTaskDict is empty")
                continue
            for k,rtask in self.runningTaskDict.items():
                try:
                    self.handle(rtask)
                except Exception as e:
                    self.logger.error(f"handle error [{k}] {e}")
            

    

      