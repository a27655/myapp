from models.user import User
from routes import *
from models.follow import Follow


main = Blueprint('follow', __name__)


@main.route('/add')
def add():
    u = current_user()
    if u:
        form = request.form
        print ('ceuicec')

        f = Follow(form)
        f.fans = u
        f.save()
    else:
        message = '关注功能需要登录'
        return render_template('user_login.html', message=message)


@main.route('/delete')
def delete():
    u = current_user()
    if u:
        form = request.form
        print ('ceuicec')

        f = Follow.query.get(form.get('follow_id', ''))
        f.delete()
    else:
        message = '关注功能需要登录'
        return render_template('user_login.html', message=message)
