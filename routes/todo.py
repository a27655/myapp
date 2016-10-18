from models.todo import Todo
from routes import *


main = Blueprint('todo', __name__)


def admin_required(f):
    @wraps(f)
    def function(*args, **kwargs):
        if int(current_user().id) < 0:
            return render_template('user_login.html', message='您尚未登录，无法操作todo')
        elif int(current_user().id) != int(1) :
            abort(401)
        return f(*args, **kwargs)
    return function



@main.route('/')
def all_todo():
    u = current_user()
    ftodos = Todo.query.filter_by(user_id=u.id, tag='finished').all()
    utodos = Todo.query.filter_by(user_id=u.id, tag='unfinished').all()
    return render_template('todo.html', utodos=utodos, ftodos=ftodos, user=u)


@main.route('/finished/<int:todo_id>')
@admin_required
def finished(todo_id):
    t = Todo.query.get(todo_id)
    t.tag = 'finished'
    return redirect(url_for('.all_todo'))


@main.route('/detele/<int:todo_id>')
@admin_required
def detele(todo_id):
    t = Todo.query.get(todo_id)
    t.detele()
    return redirect(url_for('.all_todo'))


@main.route('/edit/<int:todo_id>')
@admin_required
def edit(todo_id):
    u = current_user()
    return render_template('todo_edit.html', todo_id=todo_id, user=u)


@main.route('/update', methods=['post'])
@admin_required
def update():
    form = request.form
    tid = form.get('todo-id', -1)
    tcontent = form.get('content', '')
    t = Todo.query.get(tid)
    t.task = tcontent
    t.created_time = t.time()
    t.save()
    return redirect(url_for('.all_todo'))
