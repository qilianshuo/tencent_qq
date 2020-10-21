# 模拟qq扫描二维码登录,得到cookies
import re
import time
import random
import warnings
import requests
from config import *
from utils import *

warnings.filterwarnings('ignore')


class Tencent_QQ:
    def __init__(self):
        self.all_cookies = dict()
        self.qq_num = int()
        self.pt_login_sig = str()
        self.ptqrtoken = str()
        self.res = None
        self.session = requests.session()

    def get_pt_login_sig(self):
        print('正在获取 pt_login_sig ……')
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
        self.res = self.session.get(xlogin_url, headers=headers, verify=False, params=params)
        self.all_cookies.update(requests.utils.dict_from_cookiejar(self.res.cookies))
        self.pt_login_sig = self.all_cookies['pt_login_sig']

    def get_ptqrtoken(self):
        print('正在获取 ptqrtoken ……')
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
        self.res = self.session.get(qrshow_url, headers=headers, verify=False, params=params)
        self.all_cookies.update(requests.utils.dict_from_cookiejar(self.res.cookies))
        self.ptqrtoken = decrypt_Qrsig(self.all_cookies['qrsig'])

    def get_show_image(self):
        print('请扫描二维码~~')
        saveImage(self.res.content, os.path.join(cur_path, 'qrcode.jpg'))
        showImage(os.path.join(cur_path, 'qrcode.jpg'))

    def wait_scan(self):
        while True:
            params = {
                'u1': 'https://qzs.qq.com/qzone/v5/loginsucc.html?para=izone',
                'ptqrtoken': self.ptqrtoken,
                'ptredirect': '0',
                'h': '1',
                't': '1',
                'g': '1',
                'from_ui': '1',
                'ptlang': '2052',
                'action': '0-0-' + str(int(time.time())),
                'js_ver': '19112817',
                'js_type': '1',
                'login_sig': self.pt_login_sig,
                'pt_uistyle': '40',
                'aid': '549000912',
                'daid': '5',
                'ptdrvs': 'AnyQUpMB2syC5zV6V4JDelrCvoAMh-HP6Xy5jvKJzHBIplMBK37jV1o3JjBWmY7j*U1eD8quewY_',
                'has_onekey': '1'
            }
            self.res = self.session.get(qrlogin_url, headers=headers, verify=False, params=params)
            if '登录成功' in self.res.text:
                print('登录成功!!')
                self.all_cookies.update(requests.utils.dict_from_cookiejar(self.res.cookies))
                self.qq_number = re.findall(r'&uin=(.+?)&service', self.res.text)[0]
                """下面这个当时没写注释，我也忘了要干什么了……似乎是获取cookies里的另一个值"""
                url_refresh = self.res.text[
                              self.res.text.find('http'): self.res.text.find('pt_3rd_aid=0')] + 'pt_3rd_aid=0'
                self.res = self.session.get(url_refresh, allow_redirects=False, verify=False)
                self.all_cookies.update(requests.utils.dict_from_cookiejar(self.res.cookies))
                break
            elif '二维码已经失效' in self.res.text:
                print('二维码失效,请重新扫描')
                raise RuntimeError('Fail to login, qrcode has expired...')
            time.sleep(2)

    def remove_image(self):
        removeImage(os.path.join(cur_path, 'qrcode.jpg'))

    def run(self):
        self.get_pt_login_sig()
        self.get_ptqrtoken()
        self.get_show_image()
        self.wait_scan()
        self.remove_image()


if __name__ == '__main__':
    qq = Tencent_QQ()
    qq.run()
    print('[INFO]: Account -> %s, login successfully...' % qq.qq_number)
    '''测试输出cookies'''
    print("Cookies如下:")
    print(qq.all_cookies)
    for each in qq.all_cookies:
        print("{}: {}".format(each,qq.all_cookies[each]))
