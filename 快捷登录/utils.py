# 工具函数
import os
import sys
import subprocess


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
        if sys.platform.find('darwin') >= 0:
            subprocess.call(['open', img_path])
        elif sys.platform.find('linux') >= 0:
            subprocess.call(['xdg-open', img_path])
        else:
            os.startfile(img_path)
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
