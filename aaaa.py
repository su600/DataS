import functools
from flask import Flask,render_template,request,redirect, url_for, flash, session

app = Flask(__name__)

def check_login(func):
    @functools.wraps(func)

    def inner(*args,**kwargs):
        next_url = request.path  #获取登录之前的页面路径
        print("=====",next_url)

        if session.get('user'):
            return func(*args,**kwargs)
        else:
            return redirect(url_for('login',next=next_url))

    return inner

@app.route('/login',methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    username = request.form.get("username")
    password = request.form.get("password")
    if username == "chen" and password == "123":
        session["user"] = username
        print("====")
        print(request.args.get('next'))
        print("====")
        next_url = request.args.get('next')
        print(request.full_path)

        return redirect(next_url) #跳转到登录之前的页面


    return render_template("login.html")
@app.route('/logout')
def logout():
    # 删除所有当前请求相关的session
    session.pop("user")
    return redirect(url_for('login'))

@app.route('/index')
@check_login
def index():

    print(request.full_path)
    print(request.path)
    print(request.url)
    print(request.url_root)
    print(request.url_rule)

    return render_template("a.html",sut_dict = STUDENT_DICT)


@app.route('/detail/<int:nid>')
@check_login
def detail(nid):
    info = STUDENT_DICT[nid]

    return render_template("detail.html",info=info)


@app.route('/delete/<int:nid>')
@check_login
def delete(nid):
    del STUDENT_DICT[nid]
    return redirect(url_for('index'))

app.run()