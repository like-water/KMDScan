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
    print Poc("http://a.tets.com").execute()
