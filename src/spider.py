# See https://github.com/SocialSisterYi/bilibili-API-collect/blob/master/docs/misc/sign/wbi.md
# See https://github.com/SocialSisterYi/bilibili-API-collect/issues/868
import json
import time
import urllib.parse
from functools import reduce
from hashlib import md5

import requests

mixinKeyEncTab = [
    46,
    47,
    18,
    2,
    53,
    8,
    23,
    32,
    15,
    50,
    10,
    31,
    58,
    3,
    45,
    35,
    27,
    43,
    5,
    49,
    33,
    9,
    42,
    19,
    29,
    28,
    14,
    39,
    12,
    38,
    41,
    13,
    37,
    48,
    7,
    16,
    24,
    55,
    40,
    61,
    26,
    17,
    0,
    1,
    60,
    51,
    30,
    4,
    22,
    25,
    54,
    21,
    56,
    59,
    6,
    63,
    57,
    62,
    11,
    36,
    20,
    34,
    44,
    52,
]


cookie = "buvid3=57ADE427-90A8-6E7D-F341-02E62CA23E1B39631infoc;b_nut=1701088795"


def getMixinKey(orig: str):
    "对 imgKey 和 subKey 进行字符顺序打乱编码"
    return reduce(lambda s, i: s + orig[i], mixinKeyEncTab, "")[:32]


def encWbi(params: dict[str, str | int], img_key: str, sub_key: str):
    "为请求参数进行 wbi 签名"
    mixin_key = getMixinKey(img_key + sub_key)
    curr_time = round(time.time())
    params["dm_img_list"] = "[]"
    params["dm_img_str"] = "V2ViR0wgMS"
    params[
        "dm_cover_img_str"
    ] = "QU5HTEUgKEFNRCwgUmFkZW9uIEhEIDMyMDAgR3JhcGhpY3MgRGlyZWN0M0QxMSB2c181XzAgcHNfNV8wKUdvb2dsZSBJbmMuIChBTU"
    params["wts"] = curr_time  # 添加 wts 字段
    params = dict(sorted(params.items()))  # 按照 key 重排参数
    # 过滤 value 中的 "!'()*" 字符
    params = {
        k: "".join(filter(lambda chr: chr not in "!'()*", str(v)))
        for k, v in params.items()
    }
    query = urllib.parse.urlencode(params)  # 序列化参数
    wbi_sign = md5((query + mixin_key).encode()).hexdigest()  # 计算 w_rid
    params["w_rid"] = wbi_sign
    return params


def getWbiKeys() -> tuple[str, str]:
    "获取最新的 img_key 和 sub_key"
    # resp = requests.get("https://api.bilibili.com/x/web-interface/nav")
    # resp.raise_for_status()
    # json_content = resp.json()

    # Hardcode, today is 2023-12-16
    json_content = json.loads(
        '{"code":-101,"message":"账号未登录","ttl":1,"data":{"isLogin":false,"wbi_img":{"img_url":"https://i0.hdslb.com/bfs/wbi/7cd084941338484aae1ad9425b84077c.png","sub_url":"https://i0.hdslb.com/bfs/wbi/4932caff0ff746eab6f01bf08b70ac45.png"}}}'
    )
    img_url: str = json_content["data"]["wbi_img"]["img_url"]
    sub_url: str = json_content["data"]["wbi_img"]["sub_url"]
    img_key = img_url.rsplit("/", 1)[1].split(".")[0]
    sub_key = sub_url.rsplit("/", 1)[1].split(".")[0]
    return img_key, sub_key


img_key, sub_key = getWbiKeys()


for page in range(1, 27):
    params = {"mid": "316568752", "ps": "30", "pn": page}
    signed_params = encWbi(
        params=params,
        img_key=img_key,
        sub_key=sub_key,
    )
    data = requests.get(
        "https://api.bilibili.com/x/space/wbi/arc/search",
        params=signed_params,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0"
        },
        cookies={
            # "TM_fireMjYzL3gvc3BhY2Uvd2JpL2FyYy9zZWFyY2g_ZG1fY292ZXJfaW1nX3N0cj1RVTVIVEVVZ0tFRk5SQ3dnVW1Ga1pXOXVJRWhFSURNeU1EQWdSM0poY0docFkzTWdSR2x5WldOME0wUXhNU0IyYzE4MVh6QWdjSE5mTlY4d0tVZHZiMmRzWlNCSmJtTXVJQ2hCVFUmZG1faW1nX2xpc3Q9JTVCJTVEJmRtX2ltZ19zdHI9VjJWaVIwd2dNUyZtaWQ1702718064274": "blob%3Amoz-extension%3A%2F%2F943c948f-e0f1-4c65-a3ff-30bb1eb1b670%2F236b26c2-1cf0-47de-a3c4-c627b497d041",
            # "_uuid": "6BD101085A-21B9-5C6B-4677-4C4E84BAE97D32601infoc",
            "buvid3": "0216C413-5CDC-E284-FD47-4D767FF40F4632422infoc",
            "b_nut": "1694058632",
            # "buvid4": "F0768563-FC55-37A0-2FAF-8717EF708DC032422-023090711-C%2FMb1jdk4KMMVM81PGYj9g%3D%3D",
            # "CURRENT_FNVAL": "4048",
            # "buvid_fp": "12c84852e239f42fd78ed6d20b9ca8bd",
            # "hit-dyn-v2": "1",
            # "rpdid": "|(u~)|mYRuRk0J'uYmlm)YYJR",
            # "CURRENT_QUALITY": "80",
            # "fingerprint": "c98ad60fb574c189185a7719bcd3a243",
            # "buvid_fp_plain": "undefined",
            # "LIVE_BUVID": "AUTO5217009867959944",
            # "bili_ticket": "eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDI5MDcxMjUsImlhdCI6MTcwMjY0Nzg2NSwicGx0IjotMX0.jgaPfJtV0G2lWu2mZzAtjUmsavKVCOXWER9sX1oLFPc",
            # "bili_ticket_expires": "1702907065",
            # "b_lsid": "31D49F33_18C71C5062D",
            # "sid": "8lhh0ell",
            # "bsource": "search_google",
        },
    )
    with open(f"data/{page}.json", "w", encoding="utf-8") as f:
        f.write(data.text)
