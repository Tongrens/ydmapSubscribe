import json
import random
import requests
import string
import execjs

def cb_fp():
    with open('sdk.js', 'r', encoding='utf-8') as f:
        js_code = f.read()
    cb = execjs.compile(js_code).call('get_cb')
    fp = execjs.compile(js_code).call('get_fp')
    return cb, fp

def get_conf():
    callback_string = f"__JSONP_{''.join(random.sample(string.ascii_letters, 7)).lower()}_1"
    res = requests.get(
        url="https://c.dun.163.com/api/v2/getconf",
        params={
            "referer": "https://lhqkl.ydmap.cn/user/login",
            "zoneId": "",
            "id": "0908c3b5498d40ed8e17328b88a7d6a9",
            "ipv6": "false",
            "runEnv": "10",
            "iv": "4",
            "type": "2",
            "loadVersion": "2.4.0",
            "callback": callback_string
        },
        headers={
            "Referer": "https://lhqkl.ydmap.cn/user/login",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        },
    )
    res.close()
    res_string = res.text.strip(f"{callback_string}(").strip(");")
    res_dict = json.loads(res_string)
    dt = res_dict['data']['dt']
    ac_bid = res_dict['data']['ac']['bid']
    ac_token = res_dict['data']['ac']['token']
    return dt, ac_bid, ac_token

def get(dt, ac_bid, ac_token, cb, fp):
    callback_string = f"__JSONP_{''.join(random.sample(string.ascii_letters, 7)).lower()}_1"

    res = requests.get(
        url="https://c.dun.163.com/api/v3/get",
        params={
            "referer": "https://lhqkl.ydmap.cn/user/login",
            "zoneId": "CN31",
            "dt": dt,
            "acToken": ac_token,
            "id": ac_bid,
            "fp": fp,
            "https": "true",
            "type": None,
            "version": "2.27.2",
            "dpr": "1",
            "dev": "1",
            "cb": cb,
            "ipv6": "false",
            "runEnv": "10",
            "group": "",
            "scene": "",
            "lang": "zh-CN",
            "sdkVersion": "undefined",
            "iv": "4",
            "width": "220",
            "audio": "false",
            "sizeType": "10",
            "smsVersion": "v3",
            "token": "",
            "callback": callback_string
        },
        headers={
            # "Accept-Language": "zh-CN,zh;q=0.9",
            "Referer": "https://lhqkl.ydmap.cn/user/login",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        },

    )
    res.close()
    res_string = res.text.strip(f"{callback_string}(").strip(");")
    res_dict = json.loads(res_string)
    print(res_dict)

def run():
    # get_conf请求
    dt, ac_bid, ac_token = get_conf()

    # get请求
    cb, fp = cb_fp()

    get(dt, ac_bid, ac_token, cb, fp)


if __name__ == '__main__':
    run()
