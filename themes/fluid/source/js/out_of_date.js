
(function() {
  var times = document.getElementsByTagName('time');
  if (times.length === 0) { return; }
  var posts = document.getElementsByClassName('post-content');
  if (posts.length === 0) { return; }

  var pubTime = new Date(times[0].dateTime);  /* 文章发布时间戳 */
  var now = Date.now()  /* 当前时间戳 */
  var interval = parseInt(now - pubTime)
  /* 发布时间超过指定时间（毫秒） */
  if (interval > 3600*24*30*1000){
    var days = parseInt(interval / 86400000)
    posts[0].insertAdjacentHTML('afterbegin', '<div class="note note-warning" style="font-size:0.9rem"><p>' +
      '<div class="h6">提示</div><p>本文发布于' + days +' 天前，部分信息可能更新不及时，请注意甄别。' +
      '</p></p></div>');
  }
})();