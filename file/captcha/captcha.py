import json
import random
import string

import ddddocr
import execjs
import requests


def N_as_w8(v1, v2):
    with open('N2.js', 'r', encoding='utf-8') as f:
        js_code = f.read()
    res = execjs.compile(js_code).call('N_as_w8', v1, v2)
    return res


def j_as_ww(v1):
    with open('j.js', 'r', encoding='utf-8') as f:
        js_code = f.read()
    res = execjs.compile(js_code).call('fun', v1)
    return res


def cb_fp():
    with open('cb_fp.js', 'r', encoding='utf-8') as f:
        js_code = f.read()
    cb = execjs.compile(js_code).call('get_cb')
    fp = execjs.compile(js_code).call('get_fp')
    return cb, fp


def A_unique2DArray(v1):
    with open('w2.js', 'r', encoding='utf-8') as f:
        js_code = f.read()
    res = execjs.compile(js_code).call('fun', v1)
    return res


def get_conf():
    callback_string = f"__JSONP_{''.join(random.sample(string.ascii_letters, 7)).lower()}_1"
    headers = {"Referer": "https://lhqkl.ydmap.cn/user/login",
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                             "(KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"}
    params = {"referer": "https://lhqkl.ydmap.cn/user/login", "zoneId": "", "id": "0908c3b5498d40ed8e17328b88a7d6a9",
              "ipv6": "false", "runEnv": "10", "iv": "4", "type": "2", "loadVersion": "2.4.0",
              "callback": callback_string}
    res = requests.get(url="https://c.dun.163.com/api/v2/getconf", headers=headers, params=params)
    res_string = res.text.strip(f"{callback_string}(").strip(");")
    res_dict = json.loads(res_string)
    dt = res_dict['data']['dt']
    ac_bid = res_dict['data']['ac']['bid']
    ac_token = res_dict['data']['ac']['token']
    return dt, ac_bid, ac_token


def get(dt, ac_bid, ac_token, cb, fp):
    callback_string = f"__JSONP_{''.join(random.sample(string.ascii_letters, 7)).lower()}_1"
    headers = {"Accept-Language": "zh-CN,zh;q=0.9", "Referer": "https://lhqkl.ydmap.cn/user/login",
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                             "(KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"}
    params = {"referer": "https://lhqkl.ydmap.cn/user/login", "zoneId": "CN31", "dt": dt, "acToken": ac_token,
              "id": ac_bid, "fp": fp, "https": "true", "type": "undefined", "version": "2.27.2", "dpr": "1", "dev": "1",
              "cb": cb, "ipv6": "false", "runEnv": "10", "group": "", "scene": "", "lang": "zh-CN",
              "sdkVersion": "undefined", "iv": "4", "width": "220", "audio": "false", "sizeType": "10",
              "smsVersion": "v3", "token": "", "callback": callback_string}
    res = requests.get(url="https://c.dun.163.com/api/v3/get", headers=headers, params=params)
    res_string = res.text.strip(f"{callback_string}(").strip(");")
    res_dict = json.loads(res_string)
    bg_url = res_dict['data']['bg'][0]
    front_url = res_dict['data']['front'][0]
    bg_token = res_dict['data']['token']
    bg_type = res_dict['data']['type']
    bg_zone_id = res_dict['data']['zoneId']
    return bg_url, front_url, bg_token, bg_type, bg_zone_id


def slide_match(front_url, bg_url):
    slice_bytes = requests.get(front_url).content
    bg_bytes = requests.get(bg_url).content

    # with open("front.png", mode='wb') as f:
    #     f.write(slice_bytes)
    # with open("bg.png", mode='wb') as f:
    #     f.write(bg_bytes)

    slide = ddddocr.DdddOcr(det=False, ocr=False, show_ad=False)
    res = slide.slide_match(slice_bytes, bg_bytes, simple_target=True)
    x1, y1, x2, y2 = res['target']
    # print(x1, y1, x2, y2)  # 114 45 194 125
    return int(x1 / 1.5)


def gen_trace_data(bg_token, x_distance):
    atom_trace_data = []
    trace_data = []

    interval_value = random.randint(100, 300)
    step = 2
    for i in range(0, x_distance + 1, step):
        x_value = i + step
        if x_value > x_distance:
            x_value = x_distance
        interval_value += random.randint(10, 20)
        y_value = random.randint(0, 5)

        # atom_trace_data
        chunk_list = [x_value, y_value, interval_value]
        atom_trace_data.append(chunk_list)

        # trace_data
        line = f"{x_value},{y_value},{interval_value}"
        line = N_as_w8(bg_token, line)
        trace_data.append(line)

    return trace_data, atom_trace_data


def run():
    # get_conf请求
    dt, ac_bid, ac_token = get_conf()

    # get请求
    cb, fp = cb_fp()
    bg_url, front_url, bg_token, bg_type, bg_zone_id = get(dt, ac_bid, ac_token, cb, fp)

    # 识别
    x_distance = slide_match(front_url, bg_url)

    # 轨迹数据
    trace_data, atom_trace_data = gen_trace_data(bg_token, x_distance + 11)
    d_string = j_as_ww(":".join(trace_data[0:50]))
    m_string = ""
    p_string = j_as_ww(N_as_w8(bg_token, str(x_distance / 320 * 100)))
    w2_string = A_unique2DArray(json.dumps(atom_trace_data, separators=(',', ':')))
    f_string = j_as_ww(N_as_w8(bg_token, w2_string))
    ext_string = j_as_ww(N_as_w8(bg_token, f"1,{len(trace_data)}"))

    # 构建data
    data_string = json.dumps({"d": d_string, "m": m_string, "p": p_string, "f": f_string, "ext": ext_string},
                             separators=(',', ':'))

    cb, fp = cb_fp()
    callback_string = f"__JSONP_{''.join(random.sample(string.ascii_letters, 7)).lower()}_1"
    headers = {"Accept-Language": "zh-CN,zh;q=0.9", "Referer": "https://lhqkl.ydmap.cn/user/login",
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                             "(KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"}
    params = {"referer": "https://lhqkl.ydmap.cn/user/login", "zoneId": bg_zone_id, "dt": dt, "id": ac_bid,
              "token": bg_token, "acToken": "undefined", "data": data_string, "width": "414", "type": "2",
              "version": "2.27.2", "cb": cb, "extraData": "", "bf": "0", "runEnv": "10", "sdkVersion": "undefined",
              "iv": "4", "callback": callback_string}
    res = requests.get(url="https://c.dun.163.com/api/v3/check", headers=headers, params=params)
    return json.loads(res.text.strip(f"{callback_string}(").strip(");"))


if __name__ == '__main__':
    while True:
        respone = run()
        if respone['msg'] == 'ok' and respone['data']['result']:
            print(respone)
            print("验证成功")
            break
        else:
            print(respone)
