from routes import *
import json

from models.todo import Todo
from models.weibo import Weibo
from models.blog import Blog
from models.comment import Comment

main = Blueprint('api', __name__)

def api_response(success, data=None, message=''):
    r = {
        'success': success,
        'data': data,
        'message': message
    }
    print('看看R：', r)
    return json.dumps(r, ensure_ascii=False)


def admin_required(f):
    @wraps(f)
    def function(*args, **kwargs):
        if int(current_user().id) < 0:
            return api_response(False, message='您没有登录，无法进行相关操作')
        elif int(current_user().id) != int(1):
            return api_response(False, message='帐号权限不足')
        return f(*args, **kwargs)

    return function


def admin_required_login(f):
    @wraps(f)
    def function(*args, **kwargs):
        if int(current_user().id) < 0:
            return api_response(False, message='您没有登录，无法进行相关操作')
        return f(*args, **kwargs)

    return function

# Todoapi
@main.route('/todo/add', methods=['POST'])
@admin_required
def todo_add():
    form = request.get_json()
    u = current_user()
    t = Todo(form)
    t.user = u
    if t.valid():
        t.save()
        return api_response(True, data=t.json())
    else:
        return api_response(False, message=t.error_message())



@main.route('/todo/update', methods=['post'])
@admin_required
def todo_update():
    form = request.get_json()
    print('kjkj:', form)
    u = current_user()
    tid = form.get('id', '-1')
    t = Todo.query.get(tid)
    print('看看t', t)
    t.created_time = t.time()
    t.task = form.get('content', '')
    print('再看看新t', t)
    if t.valid():
        t.save()
        return api_response(True, data=t.json())
    else:
        return api_response(False, message=t.error_message())



@main.route('/todo/finished/<int:todo_id>')
@admin_required
def todo_finished(todo_id):
    t = Todo.query.get(todo_id)
    t.tag = 'finished'
    t.created_time = t.time()
    t.save()
    return api_response(True, data=t.json())



@main.route('/todo/delete/<int:todo_id>')
@admin_required
def todo_delete(todo_id):
    t = Todo.query.get(todo_id)
    t.delete()
    return api_response(True, message='删除成功')




# weiboapi
@main.route('/weibo/add', methods=['POST'])
@admin_required
def weibo_add():
    form = request.get_json()
    print('form是啥：', form)
    u = current_user()
    t = Weibo(form)
    print('看看t', t)
    t.user = u
    print('看看：', t)
    if t.valid():
        t.save()
        return api_response(True, data=t.json())
    else:
        return api_response(False, message=t.error_message())



@main.route('/weibo/delete/<int:weibo_id>', methods=['GET'])
@admin_required
def weibo_delete(weibo_id):

    w = Weibo.query.get(weibo_id)
    print('啦啦W：', w)
    w.delete()
    if Weibo.query.get(weibo_id) is None:
        return api_response(True)
    else:
        return api_response(False)




@main.route('/weibo/update', methods=['POST'])
@admin_required
def weibo_update():
    form = request.get_json()
    print('kjkj:', form)
    u = current_user()
    wid = form.get('id', '-1')
    t = Weibo.query.get(wid)
    print('看看t', t)
    t.created_time = t.time()
    t.weibo = form.get('weibo', '')
    print('再看看新t', t)
    if t.valid():
        t.save()
        return api_response(True, data=t.json())
    else:
        return api_response(False, message=t.error_message())


# comment api
@main.route('/comment/add', methods=['POST'])
@admin_required_login
def comment_add():
    form = request.get_json()
    u = current_user()
    c = Comment(form)
    c.user = u
    wid = form.get('weibo_id')
    print('lll:', wid)
    w = Weibo.query.get(wid)
    print('kkk:', w)
    c.weibo = w
    print('ppp', c.weibo)
    if c.valid(w):
        c.save()
        return api_response(True, data=c.json())
    else:
        return api_response(False, message=c.error_message())



@main.route('/comment-blog/add', methods=['POST'])
@admin_required_login
def commentblog_add():
    # 前端发送来的数据是一个JOSN字符串
    # 在flask用request.get_json()来把josn字符串转化成字典form
    form = request.get_json()
    u = current_user()
    c = Comment(form)
    c.user = u
    bid = form.get('blog_id')
    print('lll:', bid)
    b = Blog.query.get(bid)
    print('kkk:', b)
    c.blog = b
    print('ppp', c.weibo)
    if c.valid(w=b):
        c.save()

        ##调用上面的封装函数api_response，返回r
        return api_response(True, data=c.json())
    else:
        return api_response(False, message=c.error_message())