from bot.infrastructure.wexin import WechatUtils


class GroupNativeApi:
    """
    群聊原生接口
    """
    pass


# 创建群聊
def create_group(wechat_id, name, user_list):
    """
    创建群聊
    :param wechat_id:  微信id
    :param name:  群聊名称
    :param user_list:  群聊成员列表
    :return:
    """
    req = {
        "type": 45,
        "userNames": user_list,
    }
    return WechatUtils._post_wx_request(wechat_id, req)


# 修改群聊名称
def update_group_name(wechat_id, group_id, name):
    """
    修改群聊名称
    :param wechat_id: 微信id
    :param group_id: 群聊id
    :param name: 群聊名称
    :return:
    """
    req = {
        "type": 10023,
        "chatroomUserName": group_id,
        "chatroomName": name,
    }
    return WechatUtils._post_wx_request(wechat_id, req)


# 移除群聊成员
def remove_group_member(wechat_id, group_id, user_list):
    """
    移除群聊成员
    :param wechat_id: 微信id
    :param group_id: 群聊id
    :param user_list: 用户列表
    :return:
    """
    req = {
        "type": 33,
        "chatroomUserName": group_id,
        "userNames": user_list,
    }
    return WechatUtils._post_wx_request(wechat_id, req)


# 修改群内个人昵称
def update_group_member_name(wechat_id, group_id, name):
    """
    修改群内个人昵称
    :param wechat_id: 微信id
    :param group_id: 群聊id
    :param name: 昵称
    :return:
    """
    req = {
        "type": 10024,
        "chatroomUserName": group_id,
        "nickName": name,
    }
    return WechatUtils._post_wx_request(wechat_id, req)


# 获取群聊详细信息
def get_group_detail(wechat_id, group_id):
    """
    获取群聊详细信息
    :param wechat_id: 微信id
    :param group_id: 群聊id
    :return:
    """
    req = {
        "type": 30,
        "chatroomUserName": group_id,
    }
    return WechatUtils._post_wx_request(wechat_id, req)


# 获取群成员详细信息
def get_group_member_detail(wechat_id, group_id):
    """
    获取群成员详细信息
    :param wechat_id: 微信id
    :param group_id: 群聊id
    :return:
    """
    req = {
        "type": 31,
        "chatroomUserName": group_id
    }
    return WechatUtils._post_wx_request(wechat_id, req)


# 显示/隐藏群成员昵称
def show_group_member_name(wechat_id, group_id, is_show):
    """
    显示/隐藏群成员昵称
    :param wechat_id: 微信id
    :param group_id: 群聊id
    :param is_show: 是否显示
    :return:
    """
    req = {
        "type": 10025,
        "chatroomUserName": group_id,
        "isShow": is_show
    }
    return WechatUtils._post_wx_request(wechat_id, req)


# 开启/关闭群聊免打扰
def set_group_silence(wechat_id, group_id, is_silence):
    """
    开启/关闭群聊免打扰
    :param wechat_id: 微信id
    :param group_id: 群聊id
    :param is_disturb: 是否免打扰
    :return:
    """
    req = {
        "type": 10026,
        "chatroomUserName": group_id,
        "isSilence": is_silence
    }
    return WechatUtils._post_wx_request(wechat_id, req)


# 开启/关闭群聊邀请确认
def set_group_invite_confirm(wechat_id, group_id, isNeedConfirm):
    """
    开启/关闭邀请用户入群时需管理员确认。
    :param wechat_id: 微信id
    :param group_id: 群聊id
    :param isNeedConfirm: 是否需要管理员确认
    :return:
    """
    req = {
        "type": 10030,
        "chatroomUserName": group_id,
        "isNeedConfirm": isNeedConfirm
    }
    return WechatUtils._post_wx_request(wechat_id, req)


# 开启/关闭仅管理员修改群名
def set_group_only_admin_modify_name(wechat_id, group_id, isOnlyAdminChangeName):
    """
    开启或关闭仅管理员可修改群聊名称
    :param wechat_id: 微信id
    :param group_id: 群聊id
    :param isOnlyAdminModifyName: 是否仅管理员可修改群名
    :return:
    """
    req = {
        "type": 10031,
        "chatroomUserName": group_id,
        "isOnlyAdminChangeName": isOnlyAdminChangeName
    }
    return WechatUtils._post_wx_request(wechat_id, req)


# 设置群公告
def set_group_notice(wechat_id, group_id, content):
    """
    设置群公告
    :param wechat_id: 微信id
    :param group_id: 群聊id
    :param content: 公告内容
    :return:
    """
    req = {
        "type": 10052,
        "chatroomUserName": group_id,
        "announcement": content
    }
    return WechatUtils._post_wx_request(wechat_id, req)


# 退出群聊
def quit_group(wechat_id, group_id):
    """
    退出群聊
    :param wechat_id: 微信id
    :param group_id: 群聊id
    :return:
    """
    req = {
        "type": 10028,
        "chatroomUserName": group_id,
    }
    return WechatUtils._post_wx_request(wechat_id, req)


# 添加管理员
def add_group_admin(wechat_id, group_id, user_id):
    """
    添加管理员
    :param wechat_id: 微信id
    :param group_id: 群聊id
    :param user_id: 用户列表
    :return:
    """
    req = {
        "type": 49,
        "chatroomUserName": group_id,
        "userName": user_id,
    }
    return WechatUtils._post_wx_request(wechat_id, req)


# 移除管理员
def remove_group_admin(wechat_id, group_id, user_id):
    """
    移除管理员
    :param wechat_id: 微信id
    :param group_id: 群聊id
    :param user_id: 用户列表
    :return:
    """
    req = {
        "type": 50,
        "chatroomUserName": group_id,
        "userName": user_id,
    }
    return WechatUtils._post_wx_request(wechat_id, req)


# 转让群聊
def transfer_group(wechat_id, group_id, user_id):
    """
    转让群聊
    :param wechat_id: 微信id
    :param group_id: 群聊id
    :param user_id: 用户列表
    :return:
    """
    req = {
        "type": 51,
        "chatroomUserName": group_id,
        "userName": user_id,
    }
    return WechatUtils._post_wx_request(wechat_id, req)


# 解散群聊
def dismiss_group(wechat_id, group_id):
    """
    解散群聊
    :param wechat_id: 微信id
    :param group_id: 群聊id
    :return:
    """
    req = {
        "type": 52,
        "chatroomUserName": group_id,
    }
    return WechatUtils._post_wx_request(wechat_id, req)


# 获取群聊二维码
def get_group_qrcode(wechat_id, group_id, onlyQrcodeUrl=True):
    """
    获取群聊二维码
    :param wechat_id: 微信id
    :param group_id: 群聊id
    :param onlyQrcodeUrl: 仅二维码url，默认为true
    :return:
    """
    req = {
        "type": 10054,
        "chatroomUserName": group_id,
        "onlyQrcodeUrl": onlyQrcodeUrl,
    }
    return WechatUtils._post_wx_request(wechat_id, req)


# 群聊邀请验证
def group_invite_verify(wechat_id, url):
    """
    获取群聊邀请验证的完整链接，POST访问即可入群。
    :param wechat_id: 微信id
    :param url: 群邀请原始链接，从消息推送接口获取
    :return:
    """
    req = {
        "type": 10089,
        "url": url
    }
    return WechatUtils._post_wx_request(wechat_id, req)


# 保存/取消保存群聊到通讯录
def save_group_to_contact(wechat_id, group_id, is_save):
    """
    保存/取消保存群聊到通讯录
    :param wechat_id: 微信id
    :param group_id: 群聊id
    :param is_save: 是否保存
    :return:
    """
    req = {
        "type": 10027,
        "chatroomUserName": group_id,
        "isSave": is_save
    }
    return WechatUtils._post_wx_request(wechat_id, req)


# 添加群成员到通讯录
def add_group_member_to_contact(wechat_id, group_id, user_id, message=None):
    """
    添加群成员到通讯录
    :param wechat_id: 微信id
    :param group_id: 群聊id
    :param user_list: 用户列表
    :return:
    """
    req = {
        "type": 10090,
        "userName": user_id,
        "chatroomUserName": group_id
    }
    if message is not None:
        req["message"] = message

    return WechatUtils._post_wx_request(wechat_id, req)



# 添加群成员
def add_group_member(wechat_id, group_id, user_list):
    """
    添加群成员
    :param wechat_id: 微信id
    :param group_id: 群聊id
    :param user_list: 用户列表
    :return:
    """
    user_list = [user_list] if isinstance(user_list, str) else user_list
    req = {
        "type": 32,
        "chatroomUserName": group_id,
        "userNames": user_list,
    }
    memberList = get_group_member_detail(wechat_id, group_id)
    # 如果群成员数量大于40人，则使用邀请方式
    if len(memberList["data"]["members"]) >= 40:
        req = {
            "type": 79,
            "chatroomUserName": group_id,
            "userNames": user_list
        }
    return WechatUtils._post_wx_request(wechat_id, req)
