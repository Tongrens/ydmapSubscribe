# -*- encoding: utf-8 -*-
"""
PyCharm funEncrypt
2024.07.15
by Tongrens
"""
import json
import random
import time
from urllib.parse import unquote

import execjs
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.number import bytes_to_long, long_to_bytes


# TODO: 加密URL和BODY的主函数，可以使用GET和POST
def encrypto(e, t, n, a, o, i):
    """
    :param e: url
    :param t: post_body
    :param n: {}
    :param a: 'get' or 'post'
    :param o: body
    :param i: ''
    :return:
    """
    xssKey = ('CykdY1StU8t9EAvNQTlh613BUeLoSXgNS9EAYnKghmNcDvM8ePtisYHaWZyNE2d5'
              '8GNhm8YeJ324NWW6mo3eg0QYCofezpkmCMibALwSjUJ6EmztPaekBRe3XQSoQIBi')
    duration = 0  # 矫正时间

    if '.do' not in e:
        signatures = enc_url(e, t, a, xssKey, -duration)
    else:
        signatures = enc_body(o, t, a, xssKey, -duration)
    return signatures


# TODO: 生成uuid
def get_uuid():
    # 生成uuid
    e = int(time.time() * 1000)
    uuid_str = "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx"

    def replacer(t):
        nonlocal e
        n = (e + int(16 * random.random())) % 16
        e = e // 16
        if t == 'x':
            return hex(n)[2:]
        else:
            return hex(3 & n | 8)[2:]

    return ''.join(replacer(c) if c in 'xy' else c for c in uuid_str)


# TODO: 通过execjs调用js文件，传入url+body拼接后的字符串，生成signature
def enc_url_d(e):
    """
    :param e: url+body拼接后的字符串
    :return: signature
    """
    with open('../file/enc.js', 'r', encoding='utf-8') as f:
        jscall = f.read()
    ctx = execjs.compile(jscall).call('y', e)
    return ctx


# TODO: 在进行enc_body_d之前，对body进行处理
def enc_body_d(e, t, n, i, r):
    """
    :param e: nonce & timestamp
    :param t: body
    :param n: ''
    :param i: 'get' or 'post'
    :param r: xssKey
    :return: signature
    """
    o = e.copy()
    res = {}
    for k, v in t.items():
        if isinstance(v, list):
            for idx, val in enumerate(v):
                res[f'{k}%5B{idx}%5D'] = val
        else:
            res[k] = v
    o.update(res)
    o.update(n)
    a = sorted(o.items())
    a.append(("_key", r))
    _l = "&".join([f"{t}={n}" for t, n in a])
    u = enc_url_d(_l)
    return u


# TODO: 生成url的signature
def enc_url(e, t, n, o, s):
    """
    :param e: url
    :param t: post参数
    :param n: 'get' or 'postJSON'
    :param o: xssKey
    :param s: duration 矫正时间
    :return: signature
    """
    u = get_uuid()
    h = u.replace('-', '')
    f = int(time.time() * 1000)
    p = {"nonce": h, "timestamp": f + s}
    m = "&".join([f"_{keys}={value}" for keys, value in {'key': o, 'timestamp': f + s, 'nonce': h}.items()])
    v = json.dumps(t) if n == 'post' else ''
    if e is None or e == '':
        g = None
    else:
        parts = e.split("?")
        if len(parts) < 2 or parts[1] is None or parts[1] == '':
            g = None
        else:
            a = parts[1]
            if a is None or a == '':
                g = None
            else:
                g = a.split("#")[0]
    y = unquote(g) if g else ''
    # b = post_join_str(v) if n == 'post' else ''  # post参数
    # _ = '' if n == 'post' else ''  # post参数
    b = _ = ''
    # 上面两个post我也不会了
    S = ','.join([m, y, b, _, v]).replace(' ', '')
    w = enc_url_d(S).upper()
    return p, w


# TODO: 生成body的signature
def enc_body(e, t, n, i, r):
    """
    :param e: body
    :param t: ''
    :param n: 'get' or 'post'
    :param i: xssKey
    :param r: duration 矫正时间
    :return: signature
    """
    o = get_uuid()
    a = o.replace('-', '')
    s = int(time.time() * 1000)
    u = {"nonce": a, "timestamp": s + r}
    c = enc_body_d(u, e, t, n, i).upper()
    return u, c


# TODO: RSA加密方法
class RSAEncryptor:
    def __init__(self, public_key):
        self.key = RSA.import_key(public_key)

    def encrypt(self, message):
        e = (self.key.n.bit_length() + 7) // 8

        def encode_message(message, e):
            if e < len(message) + 11:
                print("Message too long for RSA")
                return None

            i = bytearray()
            r = len(message) - 1
            while r >= 0 and e > 0:
                n = ord(message[r])
                r -= 1
                if n < 128:
                    i.append(n)
                elif n < 2048:
                    i.append((n & 63) | 128)
                    i.append((n >> 6) | 192)
                else:
                    i.append((n & 63) | 128)
                    i.append(((n >> 6) & 63) | 128)
                    i.append((n >> 12) | 224)
            i.append(0)

            while e > len(i) + 2:
                o = get_random_bytes(1)
                while o == b'\x00':
                    o = get_random_bytes(1)
                i.append(o[0])
            i.append(2)
            i.append(0)
            i = bytearray(reversed(i))
            return bytes(i)

        encoded_message = encode_message(message, e)
        if encoded_message is None:
            return None

        m = bytes_to_long(encoded_message)
        c = pow(m, self.key.e, self.key.n)
        n = long_to_bytes(c).hex()
        return n.zfill(2 * e)


# TODO: 登录加密，使用RSA加密
def login_encrypt(txt):
    public_key = """-----BEGIN PUBLIC KEY-----
    MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDQDcOWsgzqCxmAlJnxT2Jd9OcCB7GGKMllw+xCgKJVZm5UpbXgdYOtmIRH2wNw4tkXMB2JXC/sUgmiEpb9DNi43Uq68UY2LcvWdF/9dSr7nY56kt02HA/LF/ST1LGAyERDim9P+Nd5ZR5WNy/adqeHJpkLCJ5NGn+s9MckabkJyQIDAQAB
    -----END PUBLIC KEY-----"""
    encryptor = RSAEncryptor(public_key)
    ciphertext = encryptor.encrypt(txt)
    return encrypt_to_base64(ciphertext)


# TODO: 对RSA加密后的数据进行base64编码
def encrypt_to_base64(t):
    f = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    _l = '='
    r = ""
    for e in range(0, len(t) - 2, 3):
        i = int(t[e:e + 3], 16)
        r += f[i >> 6] + f[i & 63]
    if len(t) % 3 == 1:
        i = int(t[-1], 16)
        r += f[i << 2]
    elif len(t) % 3 == 2:
        i = int(t[-2:], 16)
        r += f[i >> 2] + f[(i & 3) << 4]
    while len(r) % 4 != 0:
        r += _l
    return r
