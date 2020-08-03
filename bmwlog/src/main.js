import Vue from 'vue'
import App from './App.vue'
import Router from './router'

Vue.config.productionTip = false
window.$ = window.jQuery = require('jquery')

new Vue({
  render: h => h(App),
  router: Router,
}).$mount('#app')
