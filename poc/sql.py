import requests,json,time
from kmdpoc.base_poc import BasePOC

class SqlmapApi:
    def __init__(self):
        resp=requests.get("http://127.0.0.1:8775/task/new")
        self.taskid=resp.json()['taskid']

    def sqlmapStart(self,taskid,data):
        url='http://127.0.0.1:8775/scan/'+taskid+'/start'
        headers = {'Content-Type': 'application/json'}
        resp=requests.post(url,data=data,headers=headers)
        return resp.json()['engineid']

    def sqlmapStatus(self,taskid):
        url='http://127.0.0.1:8775/scan/'+taskid+'/status'
        resp=requests.get(url)
        return resp.json()['status']

    def sqlmapResult(self,taskid):
        url='http://127.0.0.1:8775/scan/'+taskid+'/data'
        resp=requests.get(url)
        return resp.json()


    def sqlmapLog(self,taskid):
        url='http://127.0.0.1:8775/scan/'+taskid+'/log'
        resp=requests.get(url)
        return resp.json(),resp.content


class Poc(BasePOC):

    def verify(self):
        sqlmap=SqlmapApi()
        sqlmap.sqlmapStart(sqlmap.taskid,data=json.dumps(self.request_detail))

        times=0
        while sqlmap.sqlmapStatus(sqlmap.taskid)=='running':
            if times<60:
                times+=1
                time.sleep(3)
            else:
                raise Exception("Time Out")
                


        result=sqlmap.sqlmapResult(sqlmap.taskid)
        if result['data']==[]:
            return False
        else:
            return True,result['data']


