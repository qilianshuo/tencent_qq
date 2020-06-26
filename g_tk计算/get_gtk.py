def get_gtk(p_skey):
    hash = 5381
    for i in p_skey:
        hash += (hash << 5) + ord(i)
        g_tk = hash & 2147483647
    return g_tk
