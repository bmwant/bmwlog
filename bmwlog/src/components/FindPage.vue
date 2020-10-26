<script>
import $ from 'jquery'

function showSearchResults(data) {
  var list = $(".category-lst");
  list.empty();
  if($.isEmptyObject(data)) {
      $("<div />", {
          class: "no-results",
          text: "Nothing matched --->"
      }).appendTo(list);
      return;
  }

  $.each(data, function(index, post) {
      var postLink = $("<a />", {
          href: "post/" + post.id,
          class: "text bold color theme"
      });

      $("<div />", {
          class: "category-item bck light",
          text: post.title
      }).appendTo(postLink);
      list.append(postLink);
  });
}

export default {
  name: 'search-page',
  data() {
    return {
      pageTitle: 'Lookup',
      categories: [
        { name: 'Foo', postsCount: 20 },
        { name: 'Bar', postsCount: 4 }
      ]
    }
  },
  methods: {
  },
  mounted() {
    $("#search-form").submit(function (event) {
        var action = $(this).attr('action');
        var query = $("input[name='search']").val();
        $.getJSON(action, {
            query: query
        }, showSearchResults);
        event.preventDefault();
    });
  }
}
</script>

<template>
<div id="content">
  <div class="row">
    <div class="column_8">
      <div class="category-lst">
        <a v-for="category in categories" :key="category.name" href="category/#" class="text bold color theme">
          <div class="category-item bck light">{{ category.name }} <span class="posts-count">{{ category.postsCount }}</span></div>
        </a>
      </div>
    </div>
    <div class="column_4">
      <div class="search-row">
        <form class="search-form" id="search-form" action="/search">
          <input type="text" name="search" placeholder="Search..."/>
          <button class="button success"><i class="fas fa-search"></i></button>
        </form>
      </div>
    </div>
  </div>
</div>
</template>
