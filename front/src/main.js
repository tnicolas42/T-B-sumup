import Vue from 'vue'
import './plugins/axios'
import './plugins/utils.js'
import App from './App.vue'
import router from './router'
import store from './store'
import Fragment from 'vue-fragment'
import Datepicker from 'vuejs-datepicker'

Vue.config.productionTip = false

Vue.use(Fragment.Plugin)
Vue.use(Datepicker)

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
