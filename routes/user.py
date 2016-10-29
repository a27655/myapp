from models.user import User
from routes import *


main = Blueprint('user', __name__)


def admin_required(f):
    @wraps(f)
    def function(*args, **kwargs):
        if int(current_user().id) < 0:
            return render_template('user_login.html', message='您尚未登录，权限不足', user=current_user())

        return f(*args, **kwargs)

    return function


@main.route('/')
def index():
    if not User.query.get(int(1)):
        form1 = {
             'username': '管理员',
             'password': '123456',
             'avatar': '/static/img/马里奥.jpg'
        }
        u1 = User(form1)
        u1.id = int(1)
        u1.save()
    if not User.query.get(int(-1)):
        form2 = {
             'username': '游客',
             'avatar': '/static/img/nimy.jpg'
        }
        u2 = User(form2)
        u2.id = int(-1)
        u2.save()

    user = current_user()

    return render_template('one.html')
#

@main.route('/user_login')
def user_login():
    u = current_user()
    if int(u.id) > 0:
        return render_template('user_login.html', message='您已成功登录', user=u)
    else:
        return render_template('user_login.html', message='游客你好，请登录', user=u)


@main.route('/login', methods=['POST'])
def login():
    form = request.form
    username = form.get('username','')
    user = User.query.filter_by(username=username).first()
    status, msg = user.validate_login(form)
    if status:
        session['user_id'] = user.id
        return render_template('user_login.html', message=msg, user=user)
    else:
        nimy = current_user()
        return render_template('user_login.html', message=msg, user=nimy)
#
@main.route('/register', methods=['POST'])
def register():
    form = request.form
    uu = current_user()
    u = User(form)
    status, msgs = u.valid()
    if status:
        u.save()
        message = msgs[0]
        return render_template('user_login.html', message=message, user=uu)
    else:
        message = msgs[1]
        return render_template('user_login.html', message=message, user=uu)


@main.route('/edit')
@admin_required
def edit():
    u = current_user()
    return render_template('user_update.html', user=u)



@main.route('/update', methods=['POST'])
@admin_required
def update():
    form = request.form
    u = current_user()
    asnew_user = User(form)
    status, msgs = asnew_user.update_valid(u)
    if status == True and len(msgs) == 1 :
        u.username = form.get('username', '')
        u.password = form.get('password', '')
        u.avatar = form.get('avatar', '/static/img/钢铁侠.jpg')
        u.qq = form.get('qq', '他还没来的及输入他的QQ')
        u.email = form.get('email', '他还没来得及输入他的Email')
        u.sign = form.get('sign', '他还没有签名')
        u.save()
        message = '修改成功'
        return render_template('user_home.html', user=u, msssage=message)
    else:
        message = ';'.join(msgs[1:])
        return render_template('user_home.html', user=u, message=message)


@main.route('/home')
def home():
    u = current_user()
    return render_template('user_home.html', user=u, message='')

@main.route('/logout')
def logout():
    session['user_id'] = None
    u = current_user()
    return render_template('one.html')
