from .db import *
import random
from .server_model import predict
from PIL import Image




img_id_list = []
def insert_table(image: Image.Image):
    conn = getConn()
    cursor = conn.cursor()
    sql = "INSERT INTO img_table (id,age,img) VALUES  (%s,%s,%s)"
    id_x = ''.join(random.choice('0123456789') for i in range(12))
    img_id_list.append(id_x)
    age_1 = predict(image)
    img = image
    cursor.execute(sql, (id_x, age_1, img))
    conn.commit()
    cursor.close()
    conn.close()
    return id_x

# def insert_user_table(user)
#     conn = getConn()
#     cursor = conn.cursor()
#     sql = "INSERT INTO user_data (Uusername,Upassword,id_x) VALUES  (%s,%s,%s)"
#     id_x = str(img_id_list)
#     print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=',Uuser['username'])
# #     #cursor.execute(sql, (user['username'], user['password'], id_x))