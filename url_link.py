import requests
import json

# ===================== 请替换为你的小程序配置 =====================
APP_ID = "wx68aec81c081a8e6c"          # 替换成你的小程序AppID
APP_SECRET = "29d22ed0011fa2cd0fae97d803a612e7"  # 替换成你的小程序AppSecret
TARGET_PATH = "subpackages/main/webview/index"   # 要跳转的小程序页面路径（如pages/home/index）
TARGET_QUERY = "activityId=0bcf4dac0c000000&circleId=1&title=activityDetail&fromShare=1"   # 页面启动参数（可选，格式key=value&key2=value2）
IS_EXPIRE = True                    # 是否设置过期时间（True=是，False=否）
EXPIRE_TYPE = 1                     # 过期类型：1=天，2=秒
EXPIRE_INTERVAL = 1                 # 过期时长：配合EXPIRE_TYPE，1=1天/1秒
# =================================================================

def get_access_token(app_id: str, app_secret: str) -> str:
    """
    获取微信小程序接口调用凭证access_token
    :param app_id: 小程序AppID
    :param app_secret: 小程序AppSecret
    :return: 有效的access_token
    """
    try:
        url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={app_id}&secret={app_secret}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # 抛出HTTP请求异常
        result = response.json()
        
        if "errcode" in result and result["errcode"] != 0:
            raise Exception(f"获取access_token失败：{result['errmsg']}")
        
        return result["access_token"]
    
    except requests.exceptions.RequestException as e:
        raise Exception(f"网络请求异常：{str(e)}")
    except Exception as e:
        raise Exception(f"获取access_token出错：{str(e)}")

def generate_url_scheme(access_token: str) -> str:
    """
    生成微信小程序URL Scheme
    :param access_token: 接口调用凭证
    :return: 生成的URL Scheme
    """
    try:
        url = f"https://api.weixin.qq.com/wxa/generatescheme?access_token={access_token}"
        # 构造请求参数
        data = {
            "jump_wxa": {
                "path": TARGET_PATH,
                "query": TARGET_QUERY
            },
            "is_expire": IS_EXPIRE
        }
        
        # 如果设置过期时间，添加过期参数
        if IS_EXPIRE:
            data["expire_type"] = EXPIRE_TYPE
            data["expire_interval"] = EXPIRE_INTERVAL
        
        response = requests.post(url, json=data, timeout=10)
        response.raise_for_status()
        result = response.json()
        
        if result["errcode"] != 0:
            raise Exception(f"生成URL Scheme失败：{result['errmsg']}")
        
        return result["openlink"]
    
    except requests.exceptions.RequestException as e:
        raise Exception(f"网络请求异常：{str(e)}")
    except Exception as e:
        raise Exception(f"生成URL Scheme出错：{str(e)}")

def generate_url_link(access_token: str) -> str:
    """
    生成微信小程序URL Link
    :param access_token: 接口调用凭证
    :return: 生成的URL Link
    """
    try:
        url = f"https://api.weixin.qq.com/wxa/generate_urllink?access_token={access_token}"
        # 构造请求参数
        data = {
            "path": TARGET_PATH,
            "query": TARGET_QUERY,
            "is_expire": IS_EXPIRE
        }
        
        # 如果设置过期时间，添加过期参数
        if IS_EXPIRE:
            data["expire_type"] = EXPIRE_TYPE
            data["expire_interval"] = EXPIRE_INTERVAL
        
        response = requests.post(url, json=data, timeout=10)
        response.raise_for_status()
        result = response.json()
        
        if result["errcode"] != 0:
            raise Exception(f"生成URL Link失败：{result['errmsg']}")
        
        return result["url_link"]
    
    except requests.exceptions.RequestException as e:
        raise Exception(f"网络请求异常：{str(e)}")
    except Exception as e:
        raise Exception(f"生成URL Link出错：{str(e)}")

if __name__ == "__main__":
    """主函数：执行获取token、生成Scheme/Link"""
    try:
        print("===== 开始生成微信小程序链接 =====")
        # 1. 获取access_token
        print("1. 正在获取access_token...")
        access_token = get_access_token(APP_ID, APP_SECRET)
        print(f"✅ access_token获取成功：{access_token[:20]}...")
        
        # 2. 生成URL Scheme
        print("\n2. 正在生成URL Scheme...")
        url_scheme = generate_url_scheme(access_token)
        print(f"✅ URL Scheme生成成功：{url_scheme}")
        
        # 3. 生成URL Link
        print("\n3. 正在生成URL Link...")
        url_link = generate_url_link(access_token)
        print(f"✅ URL Link生成成功：{url_link}")
        
        print("\n===== 生成完成 =====")
        
    except Exception as e:
        print(f"❌ 执行失败：{str(e)}")