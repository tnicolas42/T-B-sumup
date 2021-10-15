import Store from '../store/index.js'

const to_euro = (value) => {
	return value.toFixed(2).replace('.', Store.state.float_separator) + '€'
}

const utilsPlugin = {
	install: (Vue) => {
		Vue.prototype.$to_euro = to_euro
	}
}

export { to_euro }
export default utilsPlugin