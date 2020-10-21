
#模拟qq扫描二维码登录,得到cookies
import os
import re
import time
import sys
import json
import random
import warnings
import requests
import subprocess

warnings.filterwarnings('ignore')

def getACSRFToken(p_skey):
    hash_v = 5381
    if p_skey:
        for i in range(len(p_skey)):
            hash_v += (hash_v << 5) + ord(p_skey[i])
        return hash_v & 2147483647
    return None

def get_gtk(p_skey):
        hash = 5381
        for i in p_skey:
            hash += (hash << 5) + ord(i)
            g_tk = hash & 2147483647
        return g_tk


def showImage(img_path):
    try:
        if sys.platform.find('darwin') >= 0: subprocess.call(['open', img_path])
        elif sys.platform.find('linux') >= 0: subprocess.call(['xdg-open', img_path])
        else: os.startfile(img_path)
    except:
        from PIL import Image
        img = Image.open(img_path)
        img.show()
        img.close()

def saveImage(img, img_path):
    if os.path.isfile(img_path):
        os.remove(img_path)
    fp = open(img_path, 'wb')
    fp.write(img)
    fp.close()

def removeImage(img_path):
    if sys.platform.find('darwin') >= 0:
        os.system("osascript -e 'quit app \"Preview\"'")
    os.remove(img_path)

def decrypt_Qrsig(qrsig):
    e = 0
    for c in qrsig:
        e += (e << 5) + ord(c)
    return 2147483647 & e

def frd_list(qq_number, cookies):
    url = 'https://user.qzone.qq.com/proxy/domain/r.qzone.qq.com/cgi-bin/tfriend/friend_show_qqfriends.cgi'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
        'Cookie': 'p_skey='+ cookies['p_skey'] + '; uin=' + cookies['uin']
    }
    parama = {
        'uin': qq_number,
        'g_tk': get_gtk(cookies['p_skey']),
        'qzonetoken': cookies['ptcz']
    }
    text = requests.get(url, headers=headers, params=parama).text[11:-3]
    # return json.loads(res.text[11:-3])
    return json.loads(text)

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

session = requests.Session()
cur_path = os.getcwd()
xlogin_url = 'https://xui.ptlogin2.qq.com/cgi-bin/xlogin?'
qrshow_url = 'https://ssl.ptlogin2.qq.com/ptqrshow?'
qrlogin_url = 'https://ssl.ptlogin2.qq.com/ptqrlogin?'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
}
all_cookies = {}


print("通过二维码登录获取cookies，请扫描二维码")
# 1.获取pt_login_sig
params = {
    'proxy_url': 'https://qzs.qq.com/qzone/v6/portal/proxy.html',
        'daid': '5',
        'hide_title_bar': '1',
        'low_login': '0',
        'qlogin_auto_login': '1',
        'no_verifyimg': '1',
        'link_target': 'blank',
        'appid': '549000912',
        'style': '22',
        'target': 'self',
        's_url': 'https://qzs.qq.com/qzone/v5/loginsucc.html?para=izone',
        'pt_qr_app': '手机QQ空间',
        'pt_qr_link': 'https://z.qzone.com/download.html',
        'self_regurl': 'https://qzs.qq.com/qzone/v6/reg/index.html',
        'pt_qr_help_link': 'https://z.qzone.com/download.html',
        'pt_no_auth': '0'
}
res = session.get(xlogin_url, headers=headers, verify=False, params=params)
all_cookies.update(requests.utils.dict_from_cookiejar(res.cookies))
pt_login_sig = all_cookies['pt_login_sig']

# 2.获取ptqrtoken
params = {
    'appid': '549000912',
    'e': '2',
    'l': 'M',
    's': '3',
    'd': '72',
    'v': '4',
    't': str(random.random()),
    'daid': '5',
    'pt_3rd_aid': '0'
}
res = session.get(qrshow_url, headers=headers, verify=False, params=params)
all_cookies.update(requests.utils.dict_from_cookiejar(res.cookies))
ptqrtoken = decrypt_Qrsig(all_cookies['qrsig'])

# 3.保存二维码并打开
saveImage(res.content, os.path.join(cur_path, 'qrcode.jpg'))
showImage(os.path.join(cur_path, 'qrcode.jpg'))
session.cookies.update(all_cookies)

# 4.检测二维码状态
while True:
    params = {
        'u1': 'https://qzs.qq.com/qzone/v5/loginsucc.html?para=izone',
        'ptqrtoken': ptqrtoken,
        'ptredirect': '0',
        'h': '1',
        't': '1',
        'g': '1',
        'from_ui': '1',
        'ptlang': '2052',
        'action': '0-0-' + str(int(time.time())),
        'js_ver': '19112817',
        'js_type': '1',
        'login_sig': pt_login_sig,
        'pt_uistyle': '40',
        'aid': '549000912',
        'daid': '5',
        'ptdrvs': 'AnyQUpMB2syC5zV6V4JDelrCvoAMh-HP6Xy5jvKJzHBIplMBK37jV1o3JjBWmY7j*U1eD8quewY_',
        'has_onekey': '1'
    }
    res = session.get(qrlogin_url, headers=headers, verify=False, params=params)
    if '登录成功' in res.text:
        break
    elif '二维码已经失效' in res.text:
        raise RuntimeError('Fail to login, qrcode has expired...')
    time.sleep(2)

# 5.登录成功
all_cookies.update(requests.utils.dict_from_cookiejar(res.cookies))
qq_number = re.findall(r'&uin=(.+?)&service', res.text)[0]
url_refresh = res.text[res.text.find('http'): res.text.find('pt_3rd_aid=0')] + 'pt_3rd_aid=0'
session.cookies.update(all_cookies)
res = session.get(url_refresh, allow_redirects=False, verify=False)
all_cookies.update(requests.utils.dict_from_cookiejar(res.cookies))
session.cookies.update(all_cookies)
removeImage(os.path.join(cur_path, 'qrcode.jpg'))
print('[INFO]: Account -> %s, login successfully...' % qq_number)
'''测试输出cookies'''
print("Cookies如下:")
print(all_cookies)
os.system('pause')

