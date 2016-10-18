


var log = function() {
  console.log(arguments)
}

// 这个函数用来根据 weibo 对象生成一条微博的 HTML 代码



var commentTemplate = function(comment) {
  var c = comment
  var t = ` <div class="cell-inner item">
              <img class="comment-img"width="30px"height="30px"src="${ c.avatar }">
              <span class="cell-inner-name name span-margin span-margin-name">${ c.username } :</span>
              <span class="cell-inner-comment comment">${ c.content }</span>
              <span class="cell-inner-name-time time right span-margin">${ c.created_time }</span>
            </div>
          `
  return t
}

// 绑定发布评论
var bindEventCommentadd = function() {
  $('.blog-container').on('click', '.blog-comment-button', function() {
    var buttun = $(this)
    var commentCell = buttun.closest('.blog-div-comment')
    var blogComemntsNum = buttun.closest('.blog-cell').find('.blog-comments_num').text()*1 + 1
    log('我来看看BLOGComemntsNum:', blogComemntsNum)
    var blogId = commentCell.find('.blog-addcomment-id').val()
    var commentContent = commentCell.find('.blog-comment-input').val()
    var form = {
      blog_id: blogId,
      content: commentContent,
    }
    var findComment = buttun.closest('.blog-cell').find('.all-all-comment')
    log('看看findComment:', findComment)
    var response = function(r) {
      if(r.success) {
        var comment = r.data
        $(findComment).prepend(commentTemplate(comment))
        buttun.closest('.blog-cell').find('.blog-comments_num').text(blogComemntsNum)

      }else {
        alert(r.message)
      }
    }
    api.blogcommentAdd(form, response)
  })
}


var bindEventCommentToggle = function(){
      $('.blog-cell-dodo-comment').on('click',function(){
        var commentNum = $(this)
        var commentDiv = commentNum.closest('.blog-cell').find('.comment-div')
        commentDiv.toggle()
      })
}


var bindEvents = function() {
    // 不同的事件用不同的函数去绑定处理
    // 这样逻辑就非常清晰了
    bindEventCommentToggle()
    bindEventCommentadd()
}

// 页面载入完成后会调用这个函数，所以可以当做入口
$(document).ready(function(){
    // 用 bindEvents 函数给不同的功能绑定事件处理
    // 这样逻辑就非常清晰了
    bindEvents()
})
