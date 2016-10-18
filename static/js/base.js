

$(document).ready(function() {
        $('.base-a-head').on('click', function () {
          $('.gua-active').removeClass('gua-active')
          $('.base-a-head').addClass('base-a-head-fontcolor')
          $(this).removeClass('base-a-head-fontcolor')
          $(this).addClass('gua-active')
        })
})
