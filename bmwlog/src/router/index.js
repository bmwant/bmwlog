import Vue from 'vue'
import Router from 'vue-router'
import BlogHome from '@/components/BlogHome'
import BlogPost from '@/components/BlogPost'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/posts/',
      name: 'blog-home',
      component: BlogHome
    },
    {
      path: '/post/:slug',
      name: 'blog-post',
      component: BlogPost
    }
  ]
})
