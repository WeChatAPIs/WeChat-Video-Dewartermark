from bot.infrastructure.wexin import WechatUtils


class DataBaseNativeApi:
    """
    数据库原生接口
    """
    pass


# 获取数据库信息
def get_database_info(wechat_id):
    """
    获取数据库信息
    :param wechat_id: 微信id
    :return:
    """
    req = {
        "type": 10057,
    }
    resdata = WechatUtils._post_wx_request(wechat_id, req)
    return resdata


# 查询数据库
def query_database(wechat_id, dbName, sql):
    """
    查询数据库
    :param wechat_id: 微信id
    :param dbName: 数据库名称
    :param sql: sql语句
    :return:
    """
    req = {
        "type": 10058,
        "sql": sql,
        "dbName": dbName
    }
    resdata = WechatUtils._post_wx_request(wechat_id, req)
    return resdata


# 备份数据库
def backup_database(wechat_id, dbName, outPath, dbHandle=None):
    """
    备份数据库
    :param wechat_id: 微信id
    :param dbName: 数据库名称，优先级低于dbHandle
    :param outPath: 备份路径
    :param dbHandle: 数据库句柄，优先级高于dbName
    :return:
    """
    req = {
        "type": 10059,
        "dbName": dbName,
        "outPath": outPath,
    }
    if dbHandle is not None:
        req["dbHandle"] = dbHandle
    resdata = WechatUtils._post_wx_request(wechat_id, req)
    return resdata
