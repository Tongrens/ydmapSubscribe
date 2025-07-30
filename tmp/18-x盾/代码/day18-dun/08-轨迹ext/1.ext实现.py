import subprocess
import random
import json


def N_w8(v1, v2):
    res = subprocess.check_output(f"node N2.js {v1} {v2}")
    res = res.decode('utf-8').strip()
    return res


def A_unique2DArray(v1):
    res = subprocess.check_output(f"node w2.js {v1}")
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

    trace_data = []
    atom_trace_data = []
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
        line = N_w8(bg_token, line)
        trace_data.append(line)

    ext_string = j_as_ww(N_w8(bg_token, f"1,{len(trace_data)}"))
    print(ext_string)


if __name__ == '__main__':
    run()
