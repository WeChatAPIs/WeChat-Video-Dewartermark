from bot.infrastructure.wexin import WechatUtils


class MsgCallbackNativeApi:
    """
    消息回调
    """
    pass


# 获取消息处理器列表
def get_msg_handler_list(wechat_id):
    req = {
        "type": 1003,
    }
    resdata = WechatUtils._post_wx_request(wechat_id, req)
    return resdata


# TCP处理器
def add_tcp_msg_handler(wechat_id, host, port):
    """
    添加TCP处理器
    :param wechat_id: 微信ID
    :param host: IP地址
    :param port: 端口号
    :return:
    """
    req = {
        "type": 1001,
        "protocol": 1,
        "host": host,
        "port": port
    }
    resdata = WechatUtils._post_wx_request(wechat_id, req)
    return resdata


# 添加HTTP消息处理器
def add_http_msg_handler(wechat_id, handler_url):
    req = {
        "type": 1001,
        "protocol": 2,
        "url": handler_url
    }
    resdata = WechatUtils._post_wx_request(wechat_id, req)
    return resdata



# WebSocket处理器
def add_websocket_msg_handler(wechat_id, url):
    """
    添加WebSocket消息处理器，您需要自己实现WebSocket Server。
    该类处理器使用长连接，发送完成后不会断开。
    :param wechat_id: 微信ID
    :param url: ws://127.0.0.1:8888
    :return:
    """
    req = {
        "type": 1001,
        "protocol": 3,
        "url": url
    }
    resdata = WechatUtils._post_wx_request(wechat_id, req)
    return resdata


# Windows消息处理器
def add_windows_msg_handler(wechat_id, hWnd):
    """
    添加Windows消息处理器，您需要创建一个窗口并为其处理WM_COPYDATA消息。
    :param wechat_id: 微信ID
    :param hWnd: 窗口句柄
    :return:
    """
    req = {
        "type": 1001,
        "protocol": 4,
        "hWnd": hWnd
    }
    resdata = WechatUtils._post_wx_request(wechat_id, req)
    return resdata

#移除处理器
def remove_msg_handler(wechat_id, cookie):
    """
    移除消息处理器
    :param wechat_id: 微信ID
    :param handler_id: 处理器ID
    :return:
    """
    req = {
        "type": 1002,
        "cookie": cookie
    }
    resdata = WechatUtils._post_wx_request(wechat_id, req)
    return resdata
