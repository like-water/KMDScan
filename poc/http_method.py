from kmdpoc.base_poc import BasePOC
import requests

class Poc(BasePOC):
    def verify(self):
        method_list=['delete','put','copy','move','search','profind','trace','propatch',
                     'mkcol','lock','unlockor']
        unsec_method_list=[]
        res=self.url+"   Allow Not Security Method:"
        
        for k in method_list:
            if requests.request(k,url=self.url,timeout=10).status_code==200:
                res+=k+','
                unsec_method_list.append(k)
                
        if unsec_method_list:
          return True,res
        else:
          return False,res+"NONE"


if __name__ == "__main__":
    print Poc("https://www.baidu.com").execute()


