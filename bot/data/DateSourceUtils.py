import logging
import sqlite3

from bot.data import DbWaitVerifyFriend

log = logging.getLogger(__name__)


def initTable():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    # 创建 t_wait_verify_friend 表
    DbWaitVerifyFriend.init_table_t_wait_verify_friend(cursor)
    conn.commit()
    cursor.close()
    conn.close()
    log.info("初始化数据库完成")
