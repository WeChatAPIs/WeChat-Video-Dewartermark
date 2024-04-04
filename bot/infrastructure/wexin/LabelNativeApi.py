from bot.infrastructure.wexin import WechatUtils


class LabelNativeApi:
    """
    标签原生接口
    """
    pass


# 获取标签列表
def get_label_list(wechat_id):
    """
    获取标签列表
    :param wechat_id: 微信id
    :return: 标签列表
    """
    resdata = WechatUtils._post_wx_request(wechat_id, {
        "type": 36,
    })
    return resdata["data"]["labels"]


# 添加标签
def add_label(wechat_id, label_name):
    """
    添加标签
    :param wechat_id: 微信id
    :param label_name: 标签名称
    :return: 标签id
    """
    resdata = WechatUtils._post_wx_request(wechat_id, {
        "type": 37,
        "title": label_name
    })
    return resdata["data"]["labelId"]


def delete_label(wechat_id, label_id):
    """
    删除标签
    :param wechat_id: 微信id
    :param label_id: 标签id
    :return: 是否成功
    """
    resdata = WechatUtils._post_wx_request(wechat_id, {
        "type": 38,
        "labelId": int(label_id)
    })
    return resdata["status"] == 0


# 修改标签名称
def update_label(wechat_id, label_id, label_name):
    """
    修改标签名称
    :param wechat_id: 微信id
    :param label_id: 标签id
    :param label_name: 标签名称
    :return: 是否成功
    """
    resdata = WechatUtils._post_wx_request(wechat_id, {
        "type": 39,
        "labelId": int(label_id),
        "newTitle": label_name
    })
    return resdata["status"] == 0


# 修改用户标签
def update_user_label(wechat_id, user_id, label_ids=[]):
    """
    修改用户标签
    :param wechat_id:  微信id
    :param label_ids:  标签id列表
    :param user_id: 用户id
    :return: 是否成功
    """
    req = {
        "type": 40,
        "userName": user_id,
        "labelIds": label_ids,
    }
    resdata = WechatUtils._post_wx_request(wechat_id, req)
    return resdata["status"] == 0
