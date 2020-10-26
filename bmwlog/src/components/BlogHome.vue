<script>
import { db } from '@/db'


export default {
  name: 'blog-home',
  data() {
    return {
      pageTitle: 'Posts',
      posts: []
    }
  },
  firestore: {
    posts: db.collection('posts'),
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
        {
          slug: "third-post",
          title: "This is post number 3",
          description: "The short description and some text"
        }
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
        <div v-for="(post,index) in posts" :key="post.slug + '_' + index">
          <div class="box">
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

      </div>
      <div class="load-more">
        <button id="load-button" class="button success" onclick="loadMore()">I want more!</button>
      </div>
    </div>
    <div class="column_4 hide-tablet hide-phone">

    </div>
  </div>
</div>
</template>
