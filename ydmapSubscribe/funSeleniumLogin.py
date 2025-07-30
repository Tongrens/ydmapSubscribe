# -*- encoding: utf-8 -*-
"""
PyCharm funSeleniumLogin
2024.07.18
by Tongrens
"""
import json
import time

import ddddocr
import requests
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from seleniumwire import webdriver


def getBrowserRequests(browser: webdriver, url: str) -> dict:
    res = {}
    for request in browser.requests:
        if request.response and url in request.url:
            res['url'] = request.url
            res['headers'] = request.headers
            res['body'] = request.body
            res['params'] = request.params
    return res


def useSeleniumLogin(mobile: str, pwd: str) -> dict:
    options = Options()
    options.add_argument('--headless')
    browser = webdriver.Edge()
    browser.get('https://lhqkl.ydmap.cn/user/login')
    browser.find_element('xpath', '//*[@placeholder="请输入您的手机号"]').send_keys(mobile)
    browser.find_element('xpath', '//*[@placeholder="请输入密码"]').send_keys(pwd)
    browser.find_element('xpath', '//*[@class="el-button '
                                  'full-width el-button--primary el-button--large is-round"]').click()
    time.sleep(3)
    for _ in range(3):
        res = None
        for _ in range(6):
            imgs_url = getBrowserRequests(browser, 'api/v3/get')
            for _ in range(3):
                if imgs_url:
                    del browser.requests
                    break
                else:
                    time.sleep(1)
                    imgs_url = getBrowserRequests(browser, 'api/v3/get')
            else:
                return {'code': -1, 'msg': '获取图片失败'}
            img_res = json.loads(requests.get(imgs_url['url']).text.split('(')[1].split(')')[0])
            bg_data = requests.get(img_res['data']['bg'][0]).content
            front_data = requests.get(img_res['data']['front'][0]).content
            ocr = ddddocr.DdddOcr(show_ad=False)
            ocr_res = ocr.slide_match(front_data, bg_data)['target'][2]

            element = browser.find_element('xpath', '//*[@class="yidun_slider__icon"]')
            actions = ActionChains(browser)
            actions.click_and_hold(element).perform()
            actions.move_by_offset(ocr_res, 0).perform()
            actions.release().perform()
            time.sleep(2)
            res = getBrowserRequests(browser, 'api/pub/auth/login/mobilePwd')
            if res:
                break
        else:
            browser.find_element('xpath', '//*[@class="yidun_tips__text yidun-fallback__tip"]').click()
            time.sleep(1)
        if res:
            break
    else:
        return {'code': -1, 'msg': '滑动验证失败'}
    header = getBrowserRequests(browser, 'api/memberCenter/getMyInfo')['headers']
    if header.get('access-token') and header['access-token']:
        return {'code': 0, 'msg': '登录成功', 'accessToken': header['access-token']}
    else:
        return {'code': -1, 'msg': '获取accessToken失败'}
