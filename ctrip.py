# cron 1 0 0 * * * ctrip.py

import asyncio
import json
from diskcache import Cache
from typing import Dict, Union
from diskcache import Cache
from json import dumps
from httpx import AsyncClient
from loguru import logger
from time import time
import os
import httpx
from urllib.parse import quote



cache = Cache("/cache")
ctrip = os.getenv('CTRIP', '')
plusplus_token= os.getenv("PUSHPLUS")            #plusplus推送加的token，如需通知功能，可填写此项；如果不需要通知，可以留空''
r = httpx.Client(http2=True, timeout=60)


def plusplus(title: str, content: str) -> None:
    if plusplus_token == '':
        print("plusplus推送加 服务的 token 未设置!!\n取消推送")
        return
    url = 'http://www.pushplus.plus/send?token='+plusplus_token+'&title='+quote(title)+'&content='+quote(content)
    response = r.get(url).text
    print("plusplus推送加 推送消息,并返回："+response)


# 携程签到
async def ctripSign():
    result = {
        "code": 400,
        "msg": f'请输入cticket',
        "time": int(time())
    }
    if ctrip == "":
        return result
    
    cache.set(f'ctrip_{ctrip}', ctrip)

    meta = {
        "method": "POST",
        "url": "https://m.ctrip.com/restapi/soa2/22769/signToday",
        "params": {},  # Update this as needed
        "data": dumps({
            # Add your payload here as needed
        }),
        "cookies": {"cticket": ctrip},
    }
    result = await request(meta['method'], meta['url'], meta['params'], meta['data'], meta['cookies'])

    message = json.loads(result['msg'])['message']

    print(message)

    cache.set(f'ctrip_{ctrip}', ctrip)
    
    logger.info(result)


    await pushplus("携程签到", message)
    return result

async def request(method: str, url: str, params: Dict[str, str], data: Union[str, Dict[str, str]], cookies: Dict[str, str]):
    async with AsyncClient() as client:
        response = await client.request(method, url, params=params, data=data, cookies=cookies)
        result = {
            "code": response.status_code,
            "msg": response.text,
            "time": int(time())
        }
        return result

if __name__ == '__main__':
    asyncio.run(ctripSign())



