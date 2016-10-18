

var log = function() {
  console.log(arguments)
}

var todoTemplete = function(todo) {
  var t = todo
  form = `
          <div class="utodo-div-list"data-id="${t.id}">
            <img class="img"src="/static/img/no.png" alt="" />
            <span class="utodo-span-text utodo-span">${t.task}</span>
            <span class="utodo-span-time utodo-span right">${t.created_time}</span>
            <a class="todo-a-complete right"href="#">完成</a>
            <a class="todo-a-update right"href="#">编辑</a>
          </div>`
  return form
}

var ftodoTemplete = function(todo) {
  var t = todo
  form = `
          <div class="ftodo-div-list"data-id="${t.id}">
            <img class="img"src="/static/img/yes.png" alt="" />
            <span class="ftodo-span-text ftodo-span">${t.task}</span>
            <span class="ftodo-span-time ftodo-span right">${t.created_time}</span>
            <a class="ftodo-a-detele right"href="#">删除</a>
          </div>`
  return form
}

// 绑定添加todo事件
var bindEventTodoAdd = function() {
  $('.todo-button').on('click', function(){
    var inputTodo = $('.todo-input').val()
    log('新输入：', inputTodo)
    var form = {
      task: inputTodo,
    }
    log('看看新form:', form)
    var response = function(r) {
      if(r.success){
        var t = r.data

        $('.todo-div-main-utodo').append(todoTemplete(t))

      }else{
        alert(r.message)
      }

    }
    api.todoAdd(form, response)
  })
}


// 显示隐藏编辑

  var bindEventEditToggle = function() {
    $('.todo-div-main').on('click', '.todo-a-update', function(event){
    var todoCell = $(event.target).closest('.utodo-div-list')

    var form = `
            <div class="utodo-div-update">
            <input class="todo-update-input"type="text"name="content">
            <button class="todo-update-update"href="#">编辑完成</button>
            </div>
               `
    if(todoCell.hasClass('has-class')) {
        var formUpdate = todoCell.find('.utodo-div-update')
        formUpdate.remove()
        todoCell.removeClass('has-class')
    }else {
        todoCell.append(form)
        todoCell.addClass('has-class')
    }
    return false;

  })
}


//绑定编辑todo事件
var bindEventTodoUpdate = function(){
  $('.todo-div-main').on('click', '.todo-update-update', function(event){
    var button = $(event.target)
    log('button:', button)
    var divUpdate = button.closest('.utodo-div-update')
    var divlist = button.closest('.utodo-div-list')
    log('divlist',divlist)
    var todoId = $(divlist).data('id')

    var value = divUpdate.find('.todo-update-input').val()

    var form = {
      content: value,
      id: todoId
    }
    log('看看form', form)
    var response = function(r) {
      if(r.success){
        var t = r.data
        log('看看新保存todo', t)
        divlist.find('.utodo-span-text').text(t.task)
        divlist.find('.utodo-span-time').text(t.created_time)
        divUpdate.slideUp()
        divlist.removeClass('has-class')
      }else {
        alert(r.message)
      }
    }
    api.todoUpdate(form, response)

  })
}

//绑定完成事件
var bindEventTodoFinished = function(){
  $('.todo-div-main').on('click', '.todo-a-complete', function(event){
    var todoList = $(event.target).closest('.utodo-div-list')
    log('删除键的父节点', todoList)
    var ftodo = $(event.target).closest('.todo-div-main').find('.todo-div-main-ftodo')
    var todoId = $(todoList).data('id')
    log('todo的Id', todoId)

    var response = function(r) {
      if(r.success){
        var t = r.data
        $(todoList).slideUp()
        ftodo.append(ftodoTemplete(t))
      }else {
        alert(r.message)
      }
    }
    log('9999', response)
    api.todoFinished(todoId, response)
    return false;

  })
}

// 删除
var bindEventTodoDelete = function(){
  $('.todo-div-main').on('click', '.ftodo-a-detele', function(event){
    var todoList = $(event.target).closest('.ftodo-div-list')
    log('删除键的父节点', todoList)
    var todoId = $(todoList).data('id')
    log('todo的Id', todoId)

    var response = function(r) {
      if(r.success){
        $(todoList).slideUp()
      }else {
        alert(r.message)
      }
    }
    log('9999', response)
    api.todoDelete(todoId, response)
    return false;

  })
}


var bindEvents = function() {

    bindEventTodoAdd()
    bindEventEditToggle()
    bindEventTodoUpdate()
    bindEventTodoFinished()
    bindEventTodoDelete()

}




$(document).ready(function(){
    log('hha')
    bindEvents()
})
