import sqlite3


def init_table_t_wait_verify_friend(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS t_wait_verify_friend (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            wechatId TEXT NOT NULL,
            encryptUserName TEXT NOT NULL,
            ticket TEXT NOT NULL,
            content TEXT NOT NULL,
            wxid TEXT NOT NULL,
            create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    pass


def insert_wait_verify_friend(wechatId, encryptUserName, ticket, content, wxid):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO t_wait_verify_friend (wechatId, encryptUserName, ticket, content, wxid,create_time) VALUES (?, ?, ?, ?, ?,datetime("now","localtime"))',
        (wechatId, encryptUserName, ticket, content, wxid))
    conn.commit()
    cursor.close()
    conn.close()


def select_wait_verify_friend(autoWechat):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT id, wechatId, encryptUserName, ticket, content, wxid, create_time
    FROM t_wait_verify_friend AS a
    WHERE id = (
        SELECT MIN(id)
        FROM t_wait_verify_friend AS b
        WHERE a.wechatId = b.wechatId and b.wechatId in (%s)
    );
    ''' % ','.join('?'*len(autoWechat)), autoWechat)
    data = cursor.fetchall()
    return data


def delete_wait_verify_friend(id):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM t_wait_verify_friend WHERE id = ?", (id,))
    conn.commit()
    cursor.close()
    conn.close()
