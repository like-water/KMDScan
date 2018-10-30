# komondorScan   
## poc开发   

导入BasePOC，实现验证方法：verify函数    
该函数返回：
- 有bug返回true 及详情    
- 没有bug返回false   
- 异常判断返回true及详情   

以测试banner信息为例：    

```
#!coding-utf-8
from kmdpoc.base_poc import BasePOC
import requests

class Poc(BasePOC):
    def verify(self):
        header_server=requests.get(self.url).headers
        if "Server" in header_server.keys():
            if header_server['Server'].find("Tengine")==-1:
                return True,"THE banner of server is "+header_server['Server']
            else:
                return False
        else:
            return False


if __name__ == "__main__":
    print Poc("http://alopex.tests.com").execute()
```

**另注：本平台只限用于安全测试使用；切勿用于其它用途；如有法律责任，概不负责！**
