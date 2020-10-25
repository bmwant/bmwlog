<template>
  <div id="app">
    <Header />
    <router-view></router-view>
    <Footer />
  </div>
</template>

<script>
// import old js files
// import './assets/js/jquery-1.9.1.js';
// import './assets/js/jquery.cookie.js';
import './assets/js/functions.js';
// import './assets/js/toastr.min.js';
// import HelloWorld from './components/HelloWorld.vue'
import Header from './components/Header.vue'
import Footer from './components/Footer.vue'
// import BlogHome from '@/components/BlogHome.vue'

export default {
  name: 'App',
  components: {
    Header,
    Footer
  }
}
</script>

<style>
@import './assets/styles/tuktuk.css';
@import './assets/styles/tuktuk.theme.css';
/* @  import './assets/styles/fontawesome-all.min.css'; */
@import './assets/styles/style.css';
@import './assets/styles/toastr.css';
@import './assets/styles/tag-basic-style.css';
</style>
