import json
from queue import Queue
from flask import Blueprint, jsonify, request
from app.models.user import User
from app.models.park import Park
from app.models.led import Led
from app import db,app

  

api_updateLed_router = Blueprint('api_updateLed_router', __name__,url_prefix='/api')

@api_updateLed_router.route('/', methods=['GET','POST'])
def api_index():    
    a = app.globalVar.ledTaskThread.getRunningTask()
    return json.dumps(a,indent=4,ensure_ascii=False)


@api_updateLed_router.route('/', methods=['GET','POST'])
def api_curruningTask():
    a = app.globalVar.ledTaskThread.getRunningTask()
    return json.dumps(a,indent=4,ensure_ascii=False)

@api_updateLed_router.route('/updates', methods=['GET','POST'])
def get_users():    
    json_template={
            "service_name":"Receive_LED",
            "park_id":"10045928",
            "sign":"",
            "order_id":"10001",
            "LED_id":"860402316010496" ,
            "data": [
                {
                    "F_id":1,
                    "F_message":"川A12345 来了",
                    "F_color":1
                },
                {
                    "F_id":2,
                    "F_message":"京A6789A 东门",
                    "F_color":1
                },
                {
                    "F_id":3,
                    "F_message":"京Aww789 西南",
                    "F_color":1
                },
                {
                    "F_id":4,
                    "F_message":"云BBBBBB 西南",
                    "F_color":1
                },
                {
                    "F_id":5,
                    "F_message":"云C6TGHU 下线",
                    "F_color":1
                }
            ]
        }
    try:        
        rjson= request.get_json()
        park_id=rjson['park_id']
        led_id = rjson['LED_id']
    except Exception as ex:
        print(ex)        
        return jsonify({'state':0,"msg":f"need json body {ex}\n{json_template}"})
        rjson = json_template

    result = db.session.query(
                Led.ledid,Led.park_id,Park.name,Park.pgmfilepath).filter(  
                          Led.ledid==led_id         ).filter(   
                                   Park.park_id==park_id     ).filter( 
                                              Park.park_id==Led.park_id ).all() 

    if len(result)==0:        
        return jsonify({'state':0,"msg":f"don't find parkid:{park_id},led_id:{led_id}"})
    
    rjson['pgmfilepath'] = result[0][3]
    #收到任务 
    # 解析
    # 把任务写入文件 目录：TASK_FOLDER
    #   直接把json 写入 TASK_FOLDER
    # 激活letaskThread  读一次 TASK_FOLDER
    taskJson=app.config["TASK_FOLDER"]+f"task@{park_id}_{led_id}.json"
    with open(taskJson,"w",encoding="utf-8") as f:
        json.dump(rjson,f,indent=4,ensure_ascii=False)

    #letaskThread 
    # 启动的时候 读一次 TASK_FOLDER
    # 等待激活事件去 读 TASK_FOLDER
    #  把 TASK_FOLDER 中的任务读入内存队列， 如果已经存在就覆盖
    # 执行 内存队列中的任务

    app.globalVar.ledTaskThread.activeTask(rjson)    
    return jsonify({'state':1,"msg":"success"})


