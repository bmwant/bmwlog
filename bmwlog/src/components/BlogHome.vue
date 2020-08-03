<script>
export default {
  name: 'blog-home',
  data() {
    return {
      page_title: 'Blog',
      posts: []
    }
  },
  methods: {
    getPosts() {
      this.posts = [
        {
          slug: "first-post",
          title: "My first post",
          description: "The short description"
        },
        {
          slug: "second-post",
          title: "My second post",
          description: "The short description"
        },
      ]
    }
  },
  created() {
    this.getPosts()
  }
}
</script>

<template>
<div id="content">
  <div class="row">
    <div class="column_8 padding-bottom padding-top margin-bottom margin-top">
      <div id="posts-container">
        <div class="box"
          v-for="(post,index) in posts"
          :key="post.slug + '_' + index"
        >
          <router-link :to="'/post/' + post.slug">
            <a href="" class="post-header-lst text bold color theme">{{ post.title }}</a>
          </router-link>
          <div class="post-date-lst">
            <div class="post-date bck light"><time>21/11/2020</time></div>
          </div>
          <div class="post-text-lst text justify">
            {{ post.description }}
          </div>
        </div>

        <div class="post-delim"></div>
      </div>
      <div class="load-more">
        <button id="load-button" class="button success" onclick="loadMore()">I want more!</button>
      </div>
    </div>
  </div>
</div>
</template>
