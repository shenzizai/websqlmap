# coding=UTF-8

from flask import Flask,request
from flask import render_template
import requests
import json
import sqlite3
import datetime
import time
import threading

#sqlmapapi -s
api_server='http://127.0.0.1:8775'

def db_init():
    conn=sqlite3.connect('websqlmap.db')
    query='''create table IF NOT EXISTS scan(
        date VARCHAR,
        taskid VARCHAR,
        url VARCHAR,
        scan_status VARCHAR,
        data VARCHAR        
    );'''
    conn.execute(query)
    conn.commit()
db_init()

#数据库操作函数
def db_exec(sql):
    conn = sqlite3.connect('websqlmap.db')
    c = conn.cursor()
    cursor = c.execute(sql)
    conn.commit()
    return cursor

def write_status(taskid,scan_status):
    conn = sqlite3.connect('websqlmap.db')
    c = conn.cursor()
    sql="update scan set scan_status='%s' where taskid='%s'" %(scan_status,taskid)
    cursor = c.execute(sql)
    conn.commit()
    return True

def write_data(taskid,data):
    conn = sqlite3.connect('websqlmap.db')
    c = conn.cursor()
    #for sqlite,"'"->"''"
    sql = "update scan set data='%s' where taskid='%s'" % (data.replace('\'','\'\''), taskid)
    cursor = c.execute(sql)
    conn.commit()
    return True

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

#用户方法

#获取taskid
def get_taskid():
    url=api_server+'/task/new'
    r=requests.get(url=url)
    taskid=json.loads(r.content).get('taskid')
    return taskid

#sqlmapapi的删除任务,但是并没有使用
# @app.route('/task/<taskid>/delete/')
# def task_delete(taskid):
#     url=api_server+'/task/%s/delete' %taskid
#     r=requests.get(url=url)
#     return  r.content

#sqlmap 核心函数

# @app.route('/option/<taskid>/list')
# def option_list(taskid):
#     url=api_server+'/option/%s/list' %taskid
#     r=requests.get(url=url)
#     return  r.content

# @app.route("/option/<taskid>/get",methods=['GET','POST'])
# def option_get(taskid):
#     url= api_server+'/option/%s/get' %taskid
#     r=requests.get(url=url)
#     return  r.content

# @app.route("/option/<taskid>/set",methods=['GET','POST'])
# def option_set(taskid):
#     url= api_server+'/option/%s/set' %taskid
#     r=requests.get(url=url)
#     return  r.content


#开始扫描，主函数
@app.route("/scan/newscan")
@app.route("/scan/start",methods=['GET','POST'])
def scan_start(taskid=None):
    if request.method=='GET':
        return render_template('scan.html')
    if request.method=='POST':
        formDatas = request.form
        scan_url_list = formDatas['url']
        scan_url_list=scan_url_list.split('\r\n')
        print scan_url_list
        if  len(scan_url_list[0])>0:
            for scan_url in scan_url_list:
                taskid = get_taskid()
                url = api_server + '/scan/%s/start' % taskid
                r = requests.post(url=url, data=json.dumps({'url': scan_url}), headers={'Content-Type': 'application/json'})
                # engineid=json.loads(r.content).get('engineid')
                current_time=datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                # sql="insert into scan(date,taskid,url,engineid,scan_status) values('%s','%s','%s','%s','running')" %(current_time,taskid,scan_url,int(engineid))
                sql = "insert into scan(date,taskid,url,scan_status) values('%s','%s','%s','running')" % (current_time, taskid, scan_url)
                db_exec(sql)
                threading.Thread(target=handle_task,args=(taskid,)).start()
            return '<script>alert(/ok/);window.location.href="/scan/list"</script>'
        else:
            return '<script>alert(/error url/);history.go(-1)</script>'

#任务处理，数据入库
def handle_task(taskid):
    global scan_status
    global data
    scan_status=get_status(taskid)
    write_status(taskid,scan_status)
    while scan_status == 'running':
        time.sleep(2)
        scan_status=get_status(taskid)
        if scan_status =='terminated':
            write_status(taskid,scan_status)
            data=get_result(taskid)
            # log=scan_log(taskid)
            write_data(taskid,data)
            # write_log(taskid,log)
            break

# @app.route("/scan/<taskid>/stop")
# def scan_stop(taskid):
#     url=api_server+'/scan/%s/stop' %taskid
#     r=requests.get(url=url)
#     return r.content
#
# @app.route("/scan/<taskid>/kill")
# def scan_kill(taskid):
#     url=api_server+'/scan/%s/kill' %taskid
#     r=requests.get(url=url)
#     return r.content

@app.route("/scan/list")
def show(cursor=None):
    cursor=db_exec('select * from scan')
    return render_template('list.html',cursor=cursor)



# @app.route("/scan/<taskid>/status")
def get_status(taskid):
    url = api_server + '/scan/%s/status' % taskid
    r = requests.get(url=url)
    scan_status=json.loads(r.content).get('status')
    return scan_status

#获取扫描结果
# @app.route('/task/<taskid>/data')
def get_result(taskid):
    url=api_server+'/scan/%s/data' %taskid
    r=requests.get(url)
    return r.content

@app.route('/scan/succ')
def get_succ(cursor=None):
    cursor=db_exec("select * from scan where scan_status='terminated' and length(data)!=58")
    return render_template('list.html',cursor=cursor)



if __name__ == '__main__':
    app.debug = True
    app.run()

