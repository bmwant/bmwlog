import $ from 'jquery';

function setActiveLink() {  // eslint-disable-line no-unused-vars
  var currentPath = document.location.pathname;
  var selector = "a[href='" + currentPath + "']";
  $("nav a").removeClass("active"); // Clear all previous active link in navbar for sure
  $(selector).addClass("active");
}

function noLoadButton() {
  $("#load-button")
    .removeClass("success")
    .addClass("secondary")
    .text("Cannot find what you want? Look up by category.")
    .attr("onclick","window.location='/categories'");
}

function loadMore() {  // eslint-disable-line no-unused-vars
  var nextpage = parseInt($.cookie("currentPage"));
  if(nextpage > 5) {
    noLoadButton();
  }
  $.get("/loadmore",
    {
      "page": nextpage
    },
    function(data) {
      if($.isEmptyObject(data)) {
        noLoadButton();
      }
      $.each(data, function(index, post) {
        var link = $("<a>", {
          href: "/post/" + post.url_id,
          class: "post-header-lst text bold color theme",
          text: post.title
        });

        var timeelem = $("<time>", {text: post.date});
        var timewrap = $("<div>", {class: "post-date bck light"}).append(timeelem);
        var timediv = $("<div>", {class: "post-date-lst"}).append(timewrap);
        var maindiv = $("<div>", {
          class: "post-text-lst text justify",
          text: post.short_text
        });
        var box = $("<div>", {class: "box"});
        box.append(link).append(timediv).append(maindiv);
        var delimdiv = $("<div>", {class: "post-delim"});
        $("#posts-container").append(box).append(delimdiv);
      });
    },
    "json"
  );
  $.cookie("currentPage", nextpage+1);
}
