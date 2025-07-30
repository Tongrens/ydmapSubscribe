# -*- encoding: utf-8 -*-
"""
PyCharm funMain
2024.07.10
by Tongrens
"""
import base64
import datetime
import json
import time
from urllib.parse import unquote, quote

import requests

from ydmapSubscribe import funEncrypt
from ydmapSubscribe import funSeleniumLogin


# TODO: 获取附近场馆ID和场地ID
def GetSalesIds(x: str or int, y: str or int) -> list:
    """
    :param x: 经度
    :param y: 纬度
    :return: 获取附近的场地ID
    """
    url = (f"https://lhqkl.ydmap.cn/srv100455/api/pub/sales/getSalesListByPage"
           f"?pageNumber=1&pageSize=100&amapLocation={x}%2C{y}&professional=200002&"
           f"mapIds=106011%2C105591%2C105571%2C105450%2C105500%2C105454%2C105567%2C105453%2C105577&"
           f"t={int(round(time.time() * 1000))}")
    print(url)
    res = []
    for cd in GetUrl(url)['data']['pageRecords']:
        url1 = (f'https://lhqkl.ydmap.cn/srv100455/api/pub/sport/venue/getSalesItemList?salesId={cd['id']}&'
                f't={int(round(time.time() * 1000))}')
        res1 = GetUrl(url1)['data']['salesItemVOList']

        res.append({'salesName': cd['salesName'], 'salesId': cd['id'],
                    'salesItems': [{'salesItemName': item['salesItemName'], 'salesItemId': item['salesItemId']} for item
                                   in res1]})

    return res


def searchSalesId(x: str or int, y: str or int, salesName: str) -> list:
    """
    :param x: 经度
    :param y: 纬度
    :param salesName: 场馆名称
    :return: 场馆ID
    """
    res = GetSalesIds(x, y)
    res1 = []
    for cd in res:
        if salesName in cd['salesName']:
            res1.append(cd)
    return res1


# TODO: 获取该场地时间
def GetSalesTimes(salesItemId: str or int, date: str) -> dict:
    """
    :param salesItemId: 6位场地ID
    :param date: 要查询的日期，格式为'2024-07-16'
    :return: 返回该场地当日的{date: 场馆ID、球类ID、[场地ID: {场地名称、价格ID、[{开始时间、结束时间、价格}]}]}
    """
    date_t = int(time.mktime(time.strptime(date, '%Y-%m-%d'))) * 1000
    url = (f'https://lhqkl.ydmap.cn/srv100455/api/pub/sport/venue/getSportVenueConfig'
           f'?salesItemId={salesItemId}&curDate={date_t}&venueGroupId=&t={int(round(time.time() * 1000))}')
    res = GetUrl(url)

    if res['code'] != 0:
        return {'code': -1, 'error': '获取场地信息失败'}
    else:
        res = res['data']
    if not res:
        return {'code': -1, 'error': '该日期无场地信息'}

    venueResponses = res['venueResponses']  # 场地信息
    venuePriceResponses = res['venuePriceResponses']  # 场地价格
    venueTimeSlotResponses = res['venueTimeSlotResponses']  # 场地时间段

    venueInfos = []
    for times in venueTimeSlotResponses:
        start_time = time.strftime('%H:%M', time.localtime(times['startTime'] / 1000))
        end_time = time.strftime('%H:%M', time.localtime(times['endTime'] / 1000))
        for prices in venuePriceResponses:
            if prices['startTime'] <= times['startTime'] < prices['endTime']:
                price = prices['price'] / 100
                break
        else:
            price = 'error'
        venueInfos.append({'startTime': start_time, 'endTime': end_time, 'price': price})
    venueIDs = {date: {'salesId': res['salesId'], 'salesItemId': int(salesItemId), 'venues': [{'venueId': cd['venueId'],
                                                                                               'venueInfo': {
                                                                                                   'venueName': cd[
                                                                                                       'venueName'],
                                                                                                   'venuePriceId': cd[
                                                                                                       'venuePriceId'],
                                                                                                   'TimeInfo': venueInfos}}
                                                                                              for cd in
                                                                                              venueResponses]}}

    return venueIDs


# TODO: 获取该场地三天所有可用的时间段
def Get3DaysVenue(salesItemId: str or int) -> list:
    """
    :param salesItemId: 场地ID
    :return: 该场地三天所有可用的时间段
    """
    res = []
    for i in range(3):
        date = str(datetime.date.today() + datetime.timedelta(days=i))
        res.append(CleanMap(salesItemId, GetSalesTimes(salesItemId, date)))
    return res


# TODO: 清理不可用场地
def CleanMap(mapid: str or int, dic: dict) -> dict:
    """
    :param mapid: 场地ID
    :param dic: 场地字典
    :return: 可用的场地
    """
    date = list(dic.keys())[0]
    date_t = int(time.mktime(time.strptime(date, '%Y-%m-%d'))) * 1000
    url = (f'https://lhqkl.ydmap.cn/srv100455/api/pub/sport/venue/getVenueOrderList'
           f'?salesItemId={mapid}&curDate={date_t}&venueGroupId=&t={int(round(time.time() * 1000))}')
    res = GetUrl(url)  # 已被预定的场地
    if not dic:
        return dic
    if res['code'] != 0:
        return {'code': -1, 'error': '清除不可用场地失败'}
    else:
        res = res['data']
    if not res:
        return dic
    tmp1 = []
    for vid, venue in enumerate(dic[date]['venues']):
        # 如果date_t是当天并且结束时间早于当前时间，则删除
        if date == time.strftime('%Y-%m-%d', time.localtime(time.time())):
            now_time = time.localtime(time.time())
            tmp = []
            for venueTime in venue['venueInfo']['TimeInfo']:
                if not time.strptime(date + venueTime['endTime'], f'%Y-%m-%d%H:%M') < now_time:
                    tmp.append(venueTime)
                # 转为字符串
                if venueTime['endTime'] == '00:00':
                    tmp.append(venueTime)
            dic[date]['venues'][vid]['venueInfo']['TimeInfo'] = tmp
        # 删除已被预定的场地
        tmp = []
        for venueTime in venue['venueInfo']['TimeInfo']:
            t = int(time.mktime(time.strptime('2013-01-01' + venueTime['startTime'], f'%Y-%m-%d%H:%M'))) * 1000
            for order in res:
                if order['startTime'] <= t < order['endTime'] and order['venueId'] == venue['venueId']:
                    break
            else:
                tmp.append(venueTime)
        dic[date]['venues'][vid]['venueInfo']['TimeInfo'] = tmp
        # 删除TimeInfo为空的
        if venue['venueInfo']['TimeInfo']:
            tmp1.append(venue)
    dic[date]['venues'] = tmp1
    return dic


# TODO: 登录
def Login(mobile: str, pwd: str) -> dict:
    """
    :param mobile: 手机号
    :param pwd: 密码
    :return: {mobile: accessToken}
    """
    res = funSeleniumLogin.useSeleniumLogin(mobile, pwd)
    if res.get('accessToken'):
        return {mobile: res['accessToken']}
    else:
        return res


# TODO: 获取url页面
def GetUrl(url: str, send_type: str = 'get', post_body=None) -> dict:
    """
    :param url: url
    :param send_type: get or post
    :param post_body: body
    :return: 已被解析的返回的json数据
    """
    body = unquote(url.split('?')[1]) if send_type == 'get' else post_body
    enc_res = funEncrypt.encrypto(url, '' if send_type == 'get' else body, {}, send_type, body, '')

    headers = {"nonce": enc_res[0]['nonce'], "signature": enc_res[1], "timestamp": str(enc_res[0]['timestamp'])}

    if send_type == 'get':
        res = json.loads(requests.get(url, headers=headers).text)
    else:
        res = json.loads(requests.post(url, headers=headers, json=post_body).text)
    print(res)  # 24.10.08疑似接口有变动
    if res['code'] == 0:
        return res
    else:
        return {'code': -1, 'msg': res['msg']}


# TODO: 预约场地
def SubscribeMap(salesId: int, salesItemId: int, venueId: int, date: str, startTime: str, endTime: str,
                 accessToken: str) -> dict:
    """
    :param salesId: 场馆ID
    :param salesItemId: 球类ID
    :param venueId: 场地ID
    :param date: 日期(2024-7-19)
    :param startTime: 开始时间(09:00)
    :param endTime: 结束时间(10:00)
    :param accessToken: 登录信息
    :return: 预约结果
    """
    startTime = int(time.mktime(time.strptime('2013-1-1' + startTime, '%Y-%m-%d%H:%M'))) * 1000
    endTime = int(time.mktime(time.strptime('2013-1-1' + endTime, '%Y-%m-%d%H:%M'))) * 1000
    date = int(time.mktime(time.strptime(date, '%Y-%m-%d'))) * 1000
    body = {"sportPlatformList": [
        {"venueId": venueId, "startTime": startTime, "endTime": endTime, "teamId": None, "teamColor": None,
         "fightDeclaration": None, "fightMobile": None, "parentId": 0, "userAddRequestList": []}], "salesId": salesId,
        "salesItemId": salesItemId, "orderDate": date,
        "tempServerCacheKey": "MDBjMDA5ZTEtODU2YS00ODhiLWI5ZTYtN2YyOGY4OGFhYWYy"}  # 存疑
    body = quote(json.dumps(body).replace(' ', ''))
    body = base64.b64encode(body.encode('utf-8')).decode('utf-8')
    data = [body[i:i + 117] for i in range(0, len(body), 117)]
    body = {"data": [funEncrypt.login_encrypt(data[i]) for i in range(len(data))]}
    url = 'https://lhqkl.ydmap.cn/srv100455/api/sport/venueOrder/save'
    enc_res = funEncrypt.encrypto(url, body, {}, 'post', body, '')
    headers = {"nonce": enc_res[0]['nonce'], "signature": enc_res[1], "timestamp": str(enc_res[0]['timestamp']),
               "access-token": accessToken}
    res = json.loads(requests.post(url, headers=headers, json=body).text)
    print(res)
    if res['code'] == 0:
        if res['msg'] == '未登录':
            return {'code': -1, 'msg': res['msg']}
        return {'code': 0, 'msg': '预约成功，请及时付款'}
    else:
        return {'code': -1, 'msg': res['msg']}


if __name__ == '__main__':
    # Login('13000000000', 'admin')
    print(GetSalesIds(114.03, 22.65))
    # print(searchSalesId(114.03, 22.65, '简上'))
    # print(Get3DaysVenue(102914))
    # print(SubscribeMap(103909, 102914, ))
    # print(SubscribeMap(107010, 108756, 126298, '2024-08-11', '22:00', '23:00', 'eyJhbGciOiJIUzI1NiIsInppcCI6IkRFRiJ9.eJyNj8uKwkAQRf-l1qHp6lc0O1FhwoAuFLKUTrrUjEnHSaso4r9PhyHDLN3euucU9wl1CJBBc_w-NezhWntmlYcE6H6GDFOJKLkxPIGvSx17peZigpVOhUJlRFpaR5WxU6uNUGrvIlmHBZXXA2R72wRKoLfede0nPSKuU665nOhYuwbqt92J_HvWpjvUfulvsV0s5x-zbcwuA567f94dcq603omRyOMKQJwyFJIhl8z8ndbD7iJfLdbFZpRt-tvg-7Uk0FJbUj8k44PXD7F8VS4.mleh31e9MfDt9SJwjasoxsD9ZYyzYBKtPR4GqTziUhE'))
