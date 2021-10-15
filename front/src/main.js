import Vue from 'vue'
import './plugins/axios'
import './plugins/utils.js'
import App from './App.vue'
import router from './router'
import store from './store'
import Fragment from 'vue-fragment'


Vue.config.productionTip = false

Vue.use(Fragment.Plugin)

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
