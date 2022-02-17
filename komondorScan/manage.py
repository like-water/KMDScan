#!/usr/bin/env python
# -*- coding: utf-8 -*-
from app import create_app
import sys

reload(sys)
sys.setdefaultencoding('utf8')

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1234, debug=True, threaded=True)
    
#     add this line just for testing semgrep
