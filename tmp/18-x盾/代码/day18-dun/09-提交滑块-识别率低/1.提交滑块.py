import json
import random
import subprocess
import ddddocr
import requests
import string


def N_as_w8(v1, v2):
    res = subprocess.check_output(f"node N2.js {v1} {v2}")
    res = res.decode('utf-8').strip()
    return res


def j_as_ww(v1):
    res = subprocess.check_output(f"node j.js {v1}")
    res = res.decode('utf-8').strip()
    return res


def cb_fp():
    res = subprocess.check_output("node cb_fp.js")
    char_string = res.decode('utf-8').strip()
    cb, fp = char_string.strip().split()
    return cb, fp


def A_unique2DArray(v1):
    res = subprocess.check_output(f"node w2.js {v1}")
    res = res.decode('utf-8').strip()
    return res


def get_conf():
    callback_string = f"__JSONP_{''.join(random.sample(string.ascii_letters, 7)).lower()}_1"
    res = requests.get(
        url="https://c.dun.163.com/api/v2/getconf",
        params={
            "referer": "https%3A%2F%2Fdun.163.com%2Ftrial%2Fjigsaw",
            "zoneId": "",
            "id": "07e2387ab53a4d6f930b8d9a9be71bdf",
            "ipv6": "false",
            "runEnv": "10",
            "iv": "3",
            "type": "2",
            "loadVersion": "2.4.0",
            "callback": callback_string
        },
        headers={
            "Referer": "https://dun.163.com/",
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
            "referer": "https%3A%2F%2Fdun.163.com%2Ftrial%2Fjigsaw",
            "zoneId": "CN31",
            "dt": dt,
            "acToken": ac_token,
            # "acToken": "undefined",
            "id": ac_bid,
            "fp": fp,
            "https": "true",
            "type": "2",
            "version": "2.25.0",
            "dpr": "2",
            "dev": "1",
            "cb": cb,
            "ipv6": "false",
            "runEnv": "10",
            "group": "",
            "scene": "",
            "lang": "zh-CN",
            "sdkVersion": "undefined",
            "iv": "3",
            "width": "320",
            "audio": "false",
            "sizeType": "10",
            "smsVersion": "v3",
            "token": "",
            "callback": callback_string
        },
        # cookies=cookie_dict,
        headers={
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Referer": "https://dun.163.com/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        },

    )
    res.close()
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
    with open("front.png", mode='wb') as f:
        f.write(slice_bytes)
    bg_bytes = requests.get(bg_url).content
    with open("bg.png", mode='wb') as f:
        f.write(bg_bytes)

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
    # x_distance = slide_match2(front_url, bg_url)
    # 轨迹数据
    trace_data, atom_trace_data = gen_trace_data(bg_token, x_distance + 11)
    d_string = j_as_ww(":".join(trace_data[0:50]))
    m_string = ""
    p_string = j_as_ww(N_as_w8(bg_token, str(x_distance / 320 * 100)))
    w2_string = A_unique2DArray(json.dumps(atom_trace_data, separators=(',', ':')))
    f_string = j_as_ww(N_as_w8(bg_token, w2_string))
    ext_string = j_as_ww(N_as_w8(bg_token, f"1,{len(trace_data)}"))

    #
    data_string = json.dumps({
        "d": d_string,
        "m": m_string,
        "p": p_string,
        "f": f_string,
        "ext": ext_string,
    }, separators=(',', ':'))

    cb, fp = cb_fp()
    callback_string = f"__JSONP_{''.join(random.sample(string.ascii_letters, 7)).lower()}_1"
    params = {
        "referer": "https://dun.163.com/trial/jigsaw",
        "zoneId": bg_zone_id,
        "dt": dt,
        "id": ac_bid,
        "token": bg_token,
        "acToken": "undefined",
        "data": data_string,
        "width": "320",
        "type": "2",
        "version": "2.25.0",
        "cb": cb,
        "extraData": "",
        "bf": "0",
        "runEnv": "10",
        "sdkVersion": "undefined",
        "iv": "3",
        "callback": callback_string
    }
    res = requests.get(
        url="https://c.dun.163.com/api/v3/check",
        params=params,
        headers={
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Referer": "https://dun.163.com/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        },
    )
    res.close()
    print(res.text)


if __name__ == '__main__':
    for i in range(10):
        run()
