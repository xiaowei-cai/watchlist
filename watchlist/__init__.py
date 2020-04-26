from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Cxw910325@localhost:3306/caixiaowei'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
'''
flash() 函数在内部会把消息存储到 Flask 提供的 session 对象里。
session 用来在请求间存储数据，它会把数据签名后存储到浏览器的 Cookie 中，所以我们需要设置签名所需的密钥：
'''
app.config['SECRET_KEY'] = 'dev'  # 等同于 app.secret_key = 'dev'
db = SQLAlchemy(app)

login_manager = LoginManager(app)  # 实例化扩展类


@login_manager.user_loader
def load_user(user_id):  # 创建用户加载回调函数，接受用户 ID 作为参数
    from watchlist.models import User
    user = User.query.get(int(user_id))  # 用 ID 作为 User 模型的主键查询对应的用户
    return user  # 返回用户对象


'''
添加了@login_required这个装饰器后，
如果未登录的用户访问对应的 URL，
Flask-Login 会把用户重定向到登录页面，并显示一个错误提示。
为了让这个重定向操作正确执行，
我们还需要把 login_manager.login_view 的值设为我们程序的登录视图端点（函数名）：
'''
login_manager.login_view = 'login'


# 这个函数返回的变量（以字典键值对的形式）将会统一注入到每一个模板的上下文环境中，因此可以直接在模板中使用。
@app.context_processor
def inject_user():
    from watchlist.models import User
    user = User.query.first()
    return dict(user=user)


from watchlist import views, errors, commands
