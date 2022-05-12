import sqlite3

conn = sqlite3.connect('icve.db',check_same_thread=False)

cur = conn.cursor()

# 初始化建表（如果表不存在）
cur.execute("create table if not exists user ("
            "id integer primary key autoincrement,"
            "userType int,"
            "userId int UNIQUE,"
            "userName text,"
            "userPwd text,"
            "newToken text,"
            "displayName text,"
            "employeeNumber text,"
            "url text,"
            "schoolName text,"
            "schoolId text,"
            "equipmentModel text,"
            "equipmentApiVersion text,"
            "clientId text,"
            "email text,"
            "comment_star text,"
            "comment_content text"
            ")")
conn.commit()


def insert(
        userType,
        userId,
        userName,
        userPwd,
        newToken,
        displayName,
        employeeNumber,
        url,
        schoolName,
        schoolId,
        equipmentModel,
        equipmentApiVersion,
        clientId,
        email,
        star='',
        content=''
):
    try:
        cur.execute(
            "INSERT INTO user (userType, userId, userName, userPwd, newToken, displayName, employeeNumber, url, schoolName, schoolId,equipmentModel, equipmentApiVersion, clientId,email,comment_star,comment_content) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (
                userType, userId, userName, userPwd, newToken, displayName, employeeNumber, url, schoolName, schoolId,
                equipmentModel, equipmentApiVersion, clientId, email, star, content))

        conn.commit()
        return {'code': '1', 'msg': '成功加入队列，序号为：' + str(cur.lastrowid)}
    except sqlite3.IntegrityError:
        return {'code': '0', 'msg': '用户已存在'}


def get_info(id=None, userId=None,account=None):
    if not id and not userId and not account:
        return ()
    elif id:
        cur.execute('select * from user where id=?', (id,))
    elif userId:
        cur.execute('select * from user where userId=?', (userId,))
    elif account:
        cur.execute('select * from user where userName=?', (account,))

    result = cur.fetchall()

    if result:
        return result[0]
    else:
        return ()


def get_one():
    cur.execute('SELECT * FROM user ORDER BY id LIMIT 1')
    result = cur.fetchall()
    if result:
        return result[0]
    else:
        return ()


def delet_one(wid=None):
    if not wid:
        cur.execute('SELECT id FROM user ORDER BY id LIMIT 1')
        wid = cur.fetchall()[0][0]
    cur.execute('DELETE FROM user WHERE id = ?', (wid,))
    conn.commit()


if __name__ == '__main__':
    # TEST

    info = insert(1, '129', 'TheName', '112233', 'IAMTOKEN', 'JOJO', '2020123456', 'https://www.noexist.com',
                  'TheSchool', 'ID123', 'iPhone 11', '15.0', 'ashdkahasjkdsa', 'eamil@.com')
    print(info)
    print(get_info(1))
    print(get_info(userId=123))
    print(get_one())
    #delet_one()
