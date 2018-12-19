$(document).ready(function() {
  // Render markdown to html
  var postElem = $('#main');
  var converter = new showdown.Converter();
  if(postElem.html().trim().startsWith('<')) {
    console.warn('Assuming html for old articles, skip converting to markdown');
  } else {
    var text = postElem.html()
      .replace(/&gt;/g, '>')
      .replace(/&lt;/g, '<')
      .replace(/&amp;/g, '&')
      .trim();
    var newHtml = converter.makeHtml(text);
    postElem.html(newHtml);
  }
  var url = document.URL;
  $('.social-sharing').children('a').each(function() {
    var newHref = $(this).attr('href') + url;
    $(this).attr('href', newHref);
  });

  // Open links in new tab
  $('.post-text a').each(function(index, elem) {
    $(elem).attr('target', '_blank');
  });
});

/*Like button*/
function checkThisPostForLike(postId) {
  var postsString = $.cookie('posts_liked');
  if(postsString === undefined) {
    return false;
  } else {
    var arr = postsString.split(',');
    return arr.indexOf(postId.toString()) !== -1;
  }
}

$(document).ready(function() {
  var postId = $('#content').data('post-id');
  if(checkThisPostForLike(postId)) {
    $("#like-button")
      .removeClass('like-button')
      .addClass('like-button-disabled')
      .off('click');
    $("#like-text").hide();
    $("#likes-count").show();
    $("#like-icon").addClass('love');
  } else {
    $("#like-button").click(function() {
      $(".doge").slideToggle("fast");
      setTimeout(function() {$(".doge").slideToggle("fast");}, 1100);

      $.ajax({
        url: "/like/" + postId
      }).done(function() {
        $.cookie.raw = true;
        $("#like-text").hide();
        var likesCounterElem = $('#likes-count');
        var counter = parseInt(likesCounterElem.text());
        likesCounterElem.text(counter+1).show();
        $("#like-icon").addClass('love');
        $("#like-button")
          .removeClass('like-button')
          .addClass('like-button-disabled')
          .off('click');

        var postsString = $.cookie('posts_liked');

        if(postsString === undefined) {
          $.cookie('posts_liked', postId, { expires : 12*30 });
        } else {
          var new_posts = postsString + "," + postId;
          $.cookie('posts_liked', new_posts, { expires : 12*30 });
        }
      });
    });
  }
});
