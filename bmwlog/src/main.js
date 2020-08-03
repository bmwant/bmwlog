import Vue from 'vue'
import { firestorePlugin } from 'vuefire'
import App from './App.vue'
import Router from './router'

Vue.config.productionTip = false
Vue.use(firestorePlugin)

new Vue({
  render: h => h(App),
  router: Router
}).$mount('#app')


