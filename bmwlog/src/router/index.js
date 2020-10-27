import Vue from 'vue'
import Router from 'vue-router'
import BlogHome from '@/components/BlogHome'
import BlogPost from '@/components/BlogPost'
import AboutPage from '@/components/AboutPage'
import PhotosPage from '@/components/PhotosPage'
import AdminPage from '@/components/AdminPage'
import SearchPage from '@/components/FindPage'
import PlaygroundPage from '@/components/PlaygroundPage'

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
      component: SearchPage
    },
    {
      path: '/gallery',
      name: 'photos-page',
      component: PhotosPage
    },
    {
      path: '/ad',
      name: 'admin-page',
      component: AdminPage
    },
    {
      path: '/play',
      name: 'playground-page',
      component: PlaygroundPage
    },
    {
      path: '/about',
      name: 'about-page',
      component: AboutPage
    }
  ]
})
