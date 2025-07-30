import json
import random
import requests
import string

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
print(res_dict)

# dt = res_dict['data']['dt']
# ac_bid = res_dict['data']['ac']['bid']
# ac_token = res_dict['data']['ac']['token']
# print(dt, ac_bid, ac_token)
