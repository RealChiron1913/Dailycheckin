def ctripSign(**kwargs):
    result = {
        "code": 400,
        "msg": f'请输入cticket',
        "time": int(time())
    }
    token = kwargs.get("token", "")
    if not token:
        return result
    token = kwargs["token"]
    cache.set(f'ctrip_{token}', token)
    meta = {
        "method": "POST",
        "url": "https://m.ctrip.com/restapi/soa2/22769/signToday",
        "params": {
            # "_fxpcqlniredt": "09031177218518661420",
            # "x-traceID": "09031177218518661420-1682060530972-8434515"
        },
        "data": dumps({
            # "platform": "H5",
            "openId": "",
            # "rmsToken": "",
            # "head": {
            #     "cid": "09031177218518661420",
            #     "ctok": "",
            #     "cver": "1.0",
            #     "lang": "01",
            #     "sid": "8888",
            #     "syscode": "09",
            #     "auth": "",
            #     "xsid": "",
            #     "extension": []
            # }
        }),
        "cookies": {"cticket": token},
    }
    res = await req(**meta)
    # print(res.text)
    if res and res.status_code == 200:
        msg = res.json()["message"]
        # if res.json()["code"] == "":
        #     cache.delete(f'csai_{token}')
        result.update({
            "code": 200,
            "msg": f'携程用户：{token} {msg}',
        })
    # 钉钉通知
    logger.info(result)
    await dingAlert(**result)
    return result