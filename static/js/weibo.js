


var log = function() {
  console.log(arguments)
}

// 这个函数用来根据 weibo 对象生成一条微博的 HTML 代码
var weiboTemplate = function(weibo) {
  var w = weibo
  var t = `
  <div class="weibo-cell cell item" data-id=${w.id}>
    <img src="${ w.avatar }" class="avatar">
    <span class="span-margin span-margin-name">${ w.username } :</span>
    <span class="span-weibo-content">${ w.weibo }</span>
    <span class="right span-margin span-time">${ w.created_time }</span>
    <div class="right span-margin">
      <input type="hidden" name="weibo_id" value=${w.id}>
      <button class="weibo-update weibo-button">编辑</button>
      <button class="weibo-delete weibo-button">删除</button>
      <a href="#" class="com">评论(<span class="comments_num">${ w.comments_num }</span>)</a>
    </div>

    <div class="comment-div hide">
      <div class="comment-container comment-container-${w.id}">
      </div>
      <div class="weibo-div-comment">
          <input class="weibo-weiboid-addcomment"type="hidden" name="weibo_id" value=${w.id}>
          <input name="content" class="weibo-input-addcomment left m" placeholder="Comment">
          <br><button class="weibo-button-addcomment">评论</button>
      </div>
    </div>
  </div>
  `
  return t
}


var commentTemplate = function(comment) {
  var c = comment
  var t = ` <div class="cell-inner item">
              <img src="${ c.avatar }" class="avatar-s">
              <span class="name span-margin span-margin-name">${ c.name } :</span>
              <span class="comment">${ c.content }</span>
              <span class="time right span-margin">${ c.created_time }</span>
            </div>
          `
  return t
}

// 绑定发布评论
var bindEventCommentadd = function() {
  $('.weibo-container').on('click', '.weibo-button-addcomment', function() {
    var buttun = $(this)
    var commentCell = $(this).closest('.weibo-div-comment')
    var weiboComemntsNum = $(this).closest('.weibo-cell').find('.comments_num').text()*1 + 1
    log('我来看看weiboComemntsNum:', weiboComemntsNum)
    var weiboId = commentCell.find('.weibo-weiboid-addcomment').val()
    var commentContent = commentCell.find('.weibo-input-addcomment').val()
    var form = {
      weibo_id: weiboId,
      content: commentContent,
    }
    var findComment = $(`.comment-container-${weiboId}`)
    log('看看findComment:', findComment)
    var response = function(r) {
      if(r.success) {
        var comment = r.data
        $(findComment).prepend(commentTemplate(comment))
        buttun.closest('.weibo-cell').find('.comments_num').text(weiboComemntsNum)

      }else {
        alert(r.message)
      }
    }
    api.commentAdd(form, response)
  })
}


var bindEventCommentToggle = function(){
    // 展开评论事件
    $('.weibo-container').on('click', 'a.com', function(){
        $(this).parent().next().slideToggle()
        // 因为展开评论是一个超链接 a 标签
        // 所以需要 return false 来阻止它的默认行为
        // a 的默认行为是跳转链接，没有指定 href 的时候就跳转到当前页面
        // 所以需要阻止
        return false;
    })
}

var bindEventWeiboAdd = function() {
    // 给按钮绑定添加 weibo 事件
    $('#id-button-weibo-add').on('click', function(){
      // 得到微博的内容并且生成 form 数据
      var weibo = $('#id-input-weibo').val()
      log('weibo,', weibo)
      var form = {
        weibo: weibo,
      }

      // 这个响应函数会在 AJAX 调用完成后被调用
      var response = function(r) {
          /*
          这个函数会被 weiboAdd 调用，并且传一个 r 参数进来
          r 参数的结构如下
          {
              'success': 布尔值,
              'data': 数据,
              'message': 错误消息
          }
          */
          // arguments 是包含所有参数的一个 list
          console.log('成功', arguments)
          log(r)
          if(r.success) {
              // 如果成功就添加到页面中
              // 因为添加微博会返回已添加的微博数据所以直接用 r.data 得到
              var w = r.data
              log('新微博是啥', w)
              $('.weibo-container').prepend(weiboTemplate(w))
              alert("添加成功")
          } else {
              // 失败，弹出提示
              alert(r.message)
          }
      }

      // 把上面的 form 和 response 函数传给 weiboAdd
      // api 在 api.js 中，因为页面会先引用 api.js 再引用 weibo.js
      // 所以 weibo.js 里面可以使用 api.js 中的内容
      api.weiboAdd(form, response)
    })
}

var bindEventWeiboDelete = function() {
    // 绑定删除微博按钮事件
    $('.weibo-container').on('click', '.weibo-delete', function(){
      // 得到当前的 weibo_id
      var weiboId = $(this).closest('.weibo-cell').data('id')

      // 得到整个微博条目的标签
      var weiboCell = $(this).closest('.weibo-cell')

      // 调用 api.weiboDelete 函数来删除微博并且在删除成功后删掉页面上的元素
      api.weiboDelete(weiboId, function(response) {
          // 直接用一个匿名函数当回调函数传给 weiboDelete
          // 这是 js 常用的方式
          var r = response
          if(r.success) {

              // slideUp 可以以动画的形式删掉一个元素
              $(weiboCell).slideUp()
              alert("删除成功")
          } else {
              console.log('错误', arguments)
              alert("删除失败")
          }
      })
    })
}

// 绑定隐藏编辑
var bindEventUpdateToggle = function() {
    $('.weibo-container').on('click', '.weibo-update', function() {
      var weibocell = $(this).closest('.weibo-cell')
      form =   `<div class="weibo-div-update">
                  <input class="weibo-update-content"type="text"placeholder="Edit Weibo"></input>
                  <button class="weibo-update-ok">编辑完成</button>
                </div>
               `
    if(weibocell.hasClass('has-class')) {
        var formUpdate = weibocell.find('.weibo-div-update')
        formUpdate.remove()
        weibocell.removeClass('has-class')
    }else {
        weibocell.append(form)
        weibocell.addClass('has-class')
             }
    })

}

// 绑定编辑
var bindEventWeiboUpdate = function() {
    $('.weibo-container').on('click', '.weibo-update-ok', function() {


      var weibocell = $(this).closest('.weibo-cell')
      var weiboId = weibocell.data('id')
      var updatecell = $(this).closest('.weibo-div-update')
      var updateWeibo = $(this).closest('.weibo-div-update')
      var value = updateWeibo.find('.weibo-update-content').val()
      log('为什么log没有呢')
      log('kjkj:', value)
      var form = {
          weibo: value,
          id: weiboId
          }
      var response = function(r) {
          if(r.success) {
            //r.data，一个字典，是一个微博对象的所有属性，
            //在Model.py的Weibo类的函数json（）生成
            //然后在
              var w = r.data
              weibocell.find('.span-weibo-content').text(w.weibo)
              weibocell.find('.span-time').text(w.created_time)
              updatecell.slideUp()
              weibocell.removeClass('has-class')
              alert("编辑成功")
          } else {
              // 失败，弹出提示
              alert(r.message, '网络错误')
          }
    }
      api.weiboUpdate(form, response)
    })

}




var bindEvents = function() {
    // 不同的事件用不同的函数去绑定处理
    // 这样逻辑就非常清晰了
    bindEventCommentToggle()
    bindEventWeiboAdd()
    bindEventWeiboDelete()
    bindEventWeiboUpdate()
    bindEventUpdateToggle()
    bindEventCommentadd()
}

// 页面载入完成后会调用这个函数，所以可以当做入口
$(document).ready(function(){
    // 用 bindEvents 函数给不同的功能绑定事件处理
    // 这样逻辑就非常清晰了
    bindEvents()
})
