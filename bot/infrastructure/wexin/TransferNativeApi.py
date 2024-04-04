from bot.infrastructure.wexin import WechatUtils


class TransferNativeApi:
    """
    转账原生接口
    """
    pass


# 获取详细信息
def get_transfer_detail(wechat_id, user_id, transfer_id):
    """
    获取详细信息
    :param wechat_id: 微信id
    :param user_id: 用户id
    :param transfer_id: 转账id
    :return:
    """
    req = {
        "type": 10042,
        "userName": user_id,
        "transferId": transfer_id,
    }
    resdata = WechatUtils._post_wx_request(wechat_id, req)
    return resdata


# 确认收款
def confirm_transfer(wechat_id, user_id, transfer_id):
    """
    确认收款
    :param wechat_id: 微信id
    :param user_id: 用户id
    :param transfer_id: 转账id
    :return:
    """
    req = {
        "type": 10043,
        "userName": user_id,
        "transferId": transfer_id,
    }
    resdata = WechatUtils._post_wx_request(wechat_id, req)
    return resdata


# 退还转账
def refund_transfer(wechat_id, user_id, transfer_id):
    """
    退还转账
    :param wechat_id: 微信id
    :param user_id: 用户id
    :param transfer_id: 转账id
    :return:
    """
    req = {
        "type": 10044,
        "userName": user_id,
        "transferId": transfer_id,
    }
    resdata = WechatUtils._post_wx_request(wechat_id, req)
    return resdata

