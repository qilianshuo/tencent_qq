def bkn(skey):
    e = "skey"
    t = 5381
    n = 0
    o = len(e)
    while n < o:
        t += (t << 5) + ord(e[n])
        n += 1
    return t & 2147483647
