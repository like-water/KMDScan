# komondorScan
一款自动化安全测试工具，感谢@AloneFire
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
    print Poc("http://aex.tests.com").execute()
```

**另注：本平台只限用于安全测试使用；切勿用于其它用途；如有法律责任，概不负责！**
#另脱敏 这里ip、数据库等信息都是瞎写的，大家按照自己实际情况填写

