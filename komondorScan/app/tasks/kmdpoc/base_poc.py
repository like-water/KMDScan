# -*- coding: utf-8 -*-
class BasePOC(object):
    def __init__(self,
                 url="",
                 method="GET",
                 header=None,
                 data=None,
                 request_detail=None):
        self.url = url
        self.method = method.upper()
        self.header = header
        self.data = data
        self.request_detail = request_detail

    def verify(self):
        pass

    def execute(self):
        try:
            result = self.verify()
            code, rel = 1, ""
            if isinstance(result, bool):
                code = result
                rel = ""
            elif isinstance(result, tuple):
                code = result[0]
                rel = result[1]
            else:
                raise Exception("Unknown verify function return")
            if code:
                return 1, rel
            else:
                return 0, rel
        except Exception, ex:
            return 2, ex.message

    def send_request(self, **kwargs):
        import requests
        if not kwargs.get("timeout"):
            kwargs["timeout"] = 10

        if self.method == "GET":
            return requests.get(self.url,
                                data=self.data,
                                headers=self.header,
                                **kwargs)
        elif self.method == "POST":
            return requests.post(
                self.url, data=self.data, headers=self.header, **kwargs)
        elif self.method == "PUT":
            return requests.put(self.url,
                                data=self.data,
                                headers=self.header,
                                **kwargs)
        elif self.method == "DELETE":
            return requests.delete(
                self.url, data=self.data, headers=self.header, **kwargs)
        elif self.method == "OPTIONS":
            return requests.options(
                self.url, data=self.data, headers=self.header, **kwargs)
        elif self.method == "HEAD":
            return requests.head(
                self.url, data=self.data, headers=self.header, **kwargs)
        elif self.method == "PATCH":
            return requests.patch(
                self.url, data=self.data, headers=self.header, **kwargs)
        else:
            return None
