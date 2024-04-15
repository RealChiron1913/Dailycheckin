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


cache = Cache("/cache")
ctrip = os.getenv('CTRIP', '')


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



