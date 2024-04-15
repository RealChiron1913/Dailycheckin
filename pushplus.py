#以下是使用plusplus推送加通知的函数       
import httpx
import re
import sys
import time
from urllib.parse import urlencode
from urllib.parse import quote
import os

r = httpx.Client(http2=True, timeout=60)
plusplus_token= os.getenv("PUSHPLUS")            #plusplus推送加的token，如需通知功能，可填写此项；如果不需要通知，可以留空''



def plusplus(title: str, content: str) -> None:
    if plusplus_token == '':
        print("plusplus推送加 服务的 token 未设置!!\n取消推送")
        return
    url = 'http://www.pushplus.plus/send?token='+plusplus_token+'&title='+quote(title)+'&content='+quote(content)
    response = r.get(url).text
    print("plusplus推送加 推送消息,并返回："+response)
