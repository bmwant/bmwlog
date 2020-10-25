import Vue from 'vue'
import Router from 'vue-router'
import BlogHome from '@/components/BlogHome'
import BlogPost from '@/components/BlogPost'
import AboutPage from '@/components/AboutPage'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/post',
      name: 'blog-home',
      component: BlogHome
    },
    {
      path: '/post/:slug',
      name: 'post-page',
      component: BlogPost
    },
    {
      path: '/search',
      name: 'search-page',
      component: BlogHome
    },
    {
      path: '/gallery',
      name: 'photos-page',
      component: BlogHome
    },
    {
      path: '/ad',
      name: 'admin-page',
      component: BlogHome
    },
    {
      path: '/play',
      name: 'playground-page',
      component: BlogHome
    },
    {
      path: '/about',
      name: 'about-page',
      component: AboutPage
    }
  ]
})
