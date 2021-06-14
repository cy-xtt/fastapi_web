import uvicorn
from fastapi import FastAPI, File, UploadFile,Form,Response
from starlette.responses import RedirectResponse
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse
from test_fastapi_2.server_model import read_imagefile,predict,load_model
from .storage_img import insert_table
from starlette.requests import Request
from starlette.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from .db import *


app = FastAPI(title='人脸年龄识别', description='人脸年龄识别')

# app.mount("/static",StaticFiles(directory="static"),name="static")
templates = Jinja2Templates(directory='templates')

# print(templates.TemplateResponse('index.html',{}))

@app.get("/", response_class=HTMLResponse,summary='注册和登录选择页面',tags=['注册和登录选择页面'])
async def index(request:Request):
    return """
    <html>
    <head>
        <title>欢迎使用人脸面部年龄识别</title>
    </head>
    <body>
        <a href="http://127.0.0.1:8000/register">注册</a>
        <a href="http://127.0.0.1:8000/loading">登录</a>
    </body>
    </html>
    """

@app.get('/loading',response_class=HTMLResponse,summary='用户登录',tags=['登录页面'])
def get_loading():
    return """ 
        <html>
        <div style="width:100%;text-align:center">
            <head>           
                    <title>用户登录页面</title>
                    <p></p>
            </head>
            <body>
                <h1>用户登录</h1>
                    <form action="/aaaloading" method="post">
                        <p><input type="text" name="username" placeholder="用户名"></p>
                        <p><input type="password" name="password" placeholder="密码"></p>
                        <p><input type="submit" value="登录"></p>
                    </form>               
            </body>
        </div>
        </html>    
        """


@app.post('/aaaloading', response_class=HTMLResponse,summary='用户登录验证',tags=['登录验证'])
async def aaaloading( username: int = Form(...), password: str = Form(...)):
    # 用户密码一致性验证
        # 如果两次密码一致
    user = {'username': username, 'password': password}
    conn = getConn()
    cursor = conn.cursor()
    sql = "select * From pre_img_1.user_data where Uusername='{}' and Upassword='{}'".format(username,password)
    num = cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()
    if num == 0:
        return """ 
        <html>
        <div style="width:100%;text-align:center">
            <head>            
                <title>用户登录页面</title>
            </head>
            <body>               
                    <h1>用户登录</h1>
                    <form action="/aaaloading" method="post">
                        <p><input type="text" name="username" placeholder="用户名"></p>
                        <p><input type="password" name="password" placeholder="密码"></p>
                        <p><input type="submit" value="登录" ></p>             
                    </form>
                    <form action="/register" method="get">
                        <p><input type="submit" value="注册" ></p>             
                    </form>
            </body>
        </div>
        </html>    
        """
    elif num == 1:
        return """
                <html>
                <head>
                    <title>上传文件</title>
                </head>
                <body>
                    <h3>上传文件</h3>
                    <form method="post" action="/predict/image" enctype="multipart/form-data">
                        <input type="file" name="file"/><br>
                        <input type="submit" value="上传">
                    </form>

                </body>
                </html>
                """




@app.get('/register',response_class=HTMLResponse,summary='用户注册',tags=['注册页面'])
def get_register():
    return """ 
    <html>
    <head>
        <div style="width:100%;text-align:center">
            <title>用户注册页面</title>        
        </head>
        <body>
                <h1>用户注册</h1>
                <form action="/aaaregister" method="post">
                    <p><input type="text" name="username" placeholder="用户名"></p>
                    <p><input type="password" name="password" placeholder="密码"></p>
                    <p><input type="password" name="repassword" placeholder="确认密码"></p>
                    <p><input type="submit" value="注册"></p>
                 </form>
        </body>
        </div>
    </html>    
    """


Users = []
@app.post('/aaaregister',response_class=HTMLResponse,summary='用户注册验证',tags=['注册验证'])
async def register(username: int = Form(...),password: str = Form(...),repassword: str = Form(...)):
    #用户密码一致性验证
    if password == repassword:
        #如果两次密码一致
        user = {'username':username,'password':password}
        conn = getConn()
        cursor = conn.cursor()
        sql = "INSERT INTO user_data (Uusername,Upassword) VALUES  (%s,%s)"
        cursor.execute(sql, (user['username'], user['password']))
        conn.commit()
        cursor.close()
        conn.close()
        #save_user = insert_user_table(user)
        Users.append(user)
        #存入数据库
        return """
                    
            <html>
            <head>
                <title>上传文件</title>
            </head>
            <body>
                <h3>上传文件</h3>
                <form method="post" action="/predict/image" enctype="multipart/form-data">
                    <input type="file" name="file"/><br>
                    <input type="submit" value="上传">
                </form>
            
            </body>
            </html>
        """
    else:
        return """ 
                <html>
                <div style="width:100%;text-align:center">
                    <head>
                    
                        <title>用户注册页面</title>
                    </head>
                    <body>
                        <h1>用户注册</h1>
                        <form action="/aaaregister" method="post">
                            <p><input type="text" name="username" placeholder="用户名"></p>
                            <p><input type="password" name="password" placeholder="密码"></p>
                            <p><input type="password" name="repassword" placeholder="确认密码"></p>
                            <p><input type="submit" value="注册"></p>
                    </form>
                    </body>
                </div>
                </html>    
                """



image_id_list = []
@app.post("/predict/image",response_class=HTMLResponse,summary='预测',tags=['图片预测'])
async def predict_api(file: UploadFile = File(...)):
    extension = file.filename.split(".")[-1] in ("jpg", "jpeg", "png")
    if not extension:
        return "图片格式错误！"
    print('++++++++++++++',file.filename)
    image = read_imagefile(await file.read())
    print('图片格式',type(image))
    prediction = predict(image)
    image_id_x = insert_table(image)
    image_id_list.append(image_id_x)
    print('预测的类别',prediction)
    result = {'预测': str(prediction)}
    return JSONResponse(result)



if __name__ == "__main__":
    uvicorn.run(app, debug=True)

