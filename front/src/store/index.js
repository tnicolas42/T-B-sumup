import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
		api_url: 'http://127.0.0.1:5000',
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
