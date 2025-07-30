import requests


headers = {
    "Accept": "*/*",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "DNT": "1",
    "Pragma": "no-cache",
    "Referer": "https://lhqkl.ydmap.cn/user/login",
    "Sec-Fetch-Dest": "script",
    "Sec-Fetch-Mode": "no-cors",
    "Sec-Fetch-Site": "cross-site",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0",
    "sec-ch-ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Microsoft Edge\";v=\"126\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\""
}
url = "https://c.dun.163.com/api/v3/get"
params = {
    "referer": "https://lhqkl.ydmap.cn/user/login",
    "zoneId": "CN31",
    "dt": "",  # 1
    "acToken": "", # 2
    "id": "0908c3b5498d40ed8e17328b88a7d6a9",
    "fp": "",  # 3
    "https": "true",
    "type": "undefined",
    "version": "2.27.2",
    "dpr": "1",
    "dev": "1",
    "cb": "",  # 4
    "ipv6": "false",
    "runEnv": "10",
    "group": "",
    "scene": "",
    "lang": "zh-CN",
    "sdkVersion": "undefined",
    "iv": "4",
    "width": "538",
    "audio": "false",
    "sizeType": "10",
    "smsVersion": "v3",
    "token": "",
    "callback": "__JSONP_p3uravk_0"
}
response = requests.get(url, headers=headers, params=params)

print(response.text)
