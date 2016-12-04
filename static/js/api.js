var api = {}

var log = function() {
  console.log(arguments)
}

api.ajax = function(url, method, form, callback) {
  var data = JSON.stringify(form)
  log('data',data)
  var request = {
    url: url,
    type: method,
    contentType: 'application/json',
    data: data,

    success: function(response){
      var r = JSON.parse(response)
      callback(r)
    },
    error: function(err){

      var r = {
        'success': false,
        message: '网络错误'
      }
      callback(r)
    }
  }

  $.ajax(request)
  log('kj来：', request)
}

api.get = function(url, response) {
  api.ajax(url, 'get', {}, response)
  log('Tmd的url:', url)
}

api.post = function(url, form, response) {
  api.ajax(url, 'post', form, response)
  log('Tmd的url:', form)
}



// Todo API
api.todoAdd = function(form, response) {
  log('新TODO', form)
  var url = '/api/todo/add'
  api.post(url, form, response)
}

api.todoUpdate = function(form, response) {
  log('hah', form)
  var url = '/api/todo/update'
  api.post(url, form, response)
}

api.todoFinished = function(todoId, response) {
  var url = '/api/todo/finished/' + todoId
  api.get(url, response)
}

api.todoDelete = function(todoId, response) {
  var url = '/api/todo/delete/' + todoId
  api.get(url, response)
}


// Weibo API
api.weiboAdd = function(form, response) {
    // 添加一条微博  response 是回调函数
    var url = '/api/weibo/add'
    api.post(url, form, response)

}

api.weiboDelete = function(weiboId, response) {
    // 删除一条微博
    var url = '/api/weibo/delete/' + weiboId
    var form = {}
    api.get(url, response)
}

api.weiboUpdate = function(form, response) {
    // 添加一条微博  response 是回调函数
    var url = '/api/weibo/update'
    api.post(url, form, response)
}
// 评论 API
api.commentAdd = function(form, response) {
   var url = '/api/comment/add'
   api.post(url, form, response)
}

// blog API
// blog 评论Api
api.blogcommentAdd = function(form, response) {
  var url = '/api/comment-blog/add'
  api.post(url, form, response)
}
