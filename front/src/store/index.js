import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
		api_url: window.location.protocol + '//' + window.location.hostname + ':' + process.env.VUE_APP_API_PORT,
		float_separator: ',',  // should be , or .
		is_connected: false,
		fetching_interval: 5000,
		connect_interval: 10000,
  },
  mutations: {
		setIsConnected(state, payload) {
			state.is_connected = payload
		}
  },
  actions: {
  },
  modules: {
  }
})
