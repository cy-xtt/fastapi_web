import pymysql

# 获取数据库连接
def getConn():
    conn = pymysql.connect(
    host="localhost",
    port=3306,
    user="root",password="123456",
    db='pre_img_1',
    charset='utf8',
    use_unicode=True)
    return conn


## 关闭数据库连接
def closeConn(conn):
    conn.close()

