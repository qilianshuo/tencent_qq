import time
import requests


def get_gtk(p_skey):
    hash = 5381
    for i in p_skey:
        hash += (hash << 5) + ord(i)
        g_tk = hash & 2147483647
    return g_tk

def click_cardlikes(allcookies, uin):
    uin = str(uin)
    g_tk = str(get_gtk(allcookies['p_skey']))
    t = str(int(time.time()))
    url = 'https://club.vip.qq.com/visitor/like?nav=0&uin=%s&g_tk=%s&t=%s' % (uin, g_tk, t)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
        'Cookie': 'uin=' + allcookies['uin'] + '; skey=' + allcookies['skey'] + '; p_skey=' + allcookies['p_skey']
    }
    res = requests.get(url, headers=headers)
    return res.json()
