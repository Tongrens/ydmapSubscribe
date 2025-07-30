import subprocess


def N_w8(v1, v2):
    res = subprocess.check_output(f"node N1.js {v1} {v2}")
    res = res.decode('utf-8').strip()
    return res


def j_as_ww(v1):
    res = subprocess.check_output(f"node j.js {v1}")
    res = res.decode('utf-8').strip()
    return res


def run():
    # 识别滑块的距离
    x_distance = 100
    # 背景请求返回的token
    bg_token = "cc7c74c959d842e69aa980a3430b7884"

    p_string = j_as_ww(N_w8(bg_token, str(x_distance / 320 * 100)))
    print(p_string)


if __name__ == '__main__':
    run()
