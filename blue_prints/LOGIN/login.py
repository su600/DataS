import functools
import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, session

login_ = Blueprint("login_", __name__)


# SECURITY WARNING: These are default credentials for development only
# In production, use database-backed authentication with hashed passwords
# TODO: Replace with proper authentication system (see OPTIMIZATION_NOTES.md)
# IMPORTANT: Set DEFAULT_USER and DEFAULT_PASSWORD environment variables
users = [
    {
        'username': os.environ.get('DEFAULT_USER', 'admin'),  # Changed from 'root'
        'password': os.environ.get('DEFAULT_PASSWORD', 'CHANGE_ME_NOW')  # WARNING: Not hashed!
    },
    {
        'username': 'username',
        'password': 'password'
    }
]


############ 登陆验证 不登陆无法进入其它页面 ###################
def is_login(f):
    """用来判断用户是否登录成功"""

    # 保证函数在加了装饰器之后返回的不是wrapper函数名，而是原函数名

    @functools.wraps(f)
    def inner(*args, **kwargs):
        # 判断session对象中是否有seesion['user'],
        # 如果包含信息， 则登录成功， 可以访问主页；
        # 如果不包含信息， 则未登录成功， 跳转到登录界面;
        # next_url = request.path
        if session.get('user', None):
            return f(*args, **kwargs)
        else:
            # flash('用户必须登陆才能访问%s' % f.__name__)
            return redirect(url_for('home'))  ##返回首页 url_for 调用的是函数名

    return inner


#################################################################


def is_admin(f):
    """用来判断用户是否登录成功"""

    @wraps(f)
    def wrapper(*args, **kwargs):
        # 判断session对象中是否有seesion['user']等于root,
        # 如果包含信息， 则登录成功， 可以访问主页；
        # 如果不包含信息， 则未登录成功， 跳转到登录界面;；
        if session.get('user', None) == 'root':
            return f(*args, **kwargs)
        else:
            flash('只有管理员root才能访问%s' % f.__name__)
            return redirect(url_for('login_.login'))

    return wrapper

# @csrf.exempt
@login_.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', None)
        password = request.form.get('password', None)
        # 当所有的信息遍历结束， 都没有发现注册的用户存在， 则将注册的用户添加到服务器， 并跳转登录界面;
        for user in users:
            if user['username'] == username:
                return render_template('register.html', messages='用户%s已经存在' % username)
        else:
            users.append(dict(username=username, password=password))
            # 出现一个闪现信息;
            flash('用户%s已经注册成功，请登陆.....' % username, category='info')
            return redirect(url_for('login_.login'))

    return render_template('register.html')

# @csrf.exempt
@login_.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', None)
        password = request.form.get('password', None)
        for user in users:
            if user['username'] == username and user['password'] == password:
                #  将用户登录的信息存储到session中;
                session['user'] = username
                return redirect(url_for('settings_.setting'))
            if user['username'] == username and user['password'] != password:
                # 出现一个闪现信息;
                flash("密码错误，请重新登陆", "wrong")
                return redirect("#idlogin")
                # return redirect(request.url)
        else:
            # flash(ss,"ss")
            flash("该用户不存在，请重新登陆", "none")
            return redirect("#idlogin")
    return render_template("home.html")

# @csrf.exempt
@login_.route('/list')
@is_login
def list():
    return render_template('list.html', users=users)

# @csrf.exempt
@login_.route('/logout')
def logout():
    #  将用户存储到session中的信息删除;
    session.pop('user')
    flash('注销成功....')
    return render_template('home.html')

# @csrf.exempt
@login_.route('/delete/<string:username>/')
def delete(username):
    for user in users:
        # 用户存在， 则删除;
        if username == user['username']:
            users.remove(user)
            flash('删除%s用户成功' % username)
    # else:
    #     flash('用户%s不存在'%username)

    # 删除成功， 跳转到/list/路由中.....
    return redirect(url_for(list()))



