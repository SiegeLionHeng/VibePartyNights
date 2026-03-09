import hashlib
import time
import random
import string
import requests

APP_ID = "wx68aec81c081a8e6c"
APP_SECRET = "29d22ed0011fa2cd0fae97d803a612e7"

def get_access_token():
    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APP_ID}&secret={APP_SECRET}"
    response = requests.get(url, timeout=10)
    result = response.json()
    if "errcode" in result:
        raise Exception(f"获取access_token失败: {result}")
    return result["access_token"]

def get_jsapi_ticket(access_token):
    url = f"https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token={access_token}&type=jsapi"
    response = requests.get(url, timeout=10)
    result = response.json()
    if result["errcode"] != 0:
        raise Exception(f"获取jsapi_ticket失败: {result}")
    return result["ticket"]

def create_nonce_str():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16))

def create_signature(jsapi_ticket, timestamp, nonce_str, url):
    signature_str = f"jsapi_ticket={jsapi_ticket}&noncestr={nonce_str}&timestamp={timestamp}&url={url}"
    print(f"签名字符串: {signature_str}")
    signature = hashlib.sha1(signature_str.encode('utf-8')).hexdigest()
    return signature

def get_wx_config(url):
    access_token = get_access_token()
    print(f"access_token: {access_token[:20]}...")
    
    jsapi_ticket = get_jsapi_ticket(access_token)
    print(f"jsapi_ticket: {jsapi_ticket}")
    
    timestamp = str(int(time.time()))
    nonce_str = create_nonce_str()
    signature = create_signature(jsapi_ticket, timestamp, nonce_str, url)
    
    config = {
        "appId": APP_ID,
        "timestamp": timestamp,
        "nonceStr": nonce_str,
        "signature": signature,
        "url": url
    }
    
    return config

if __name__ == "__main__":
    TARGET_URL = input("请输入你的网页URL（例如：https://your-domain.com/）: ").strip()
    
    print("===== 开始生成微信JS-SDK配置 =====")
    config = get_wx_config(TARGET_URL)
    
    print("\n===== 生成完成 =====")
    print(f"appId: {config['appId']}")
    print(f"timestamp: {config['timestamp']}")
    print(f"nonceStr: {config['nonceStr']}")
    print(f"signature: {config['signature']}")
    print(f"url: {config['url']}")
