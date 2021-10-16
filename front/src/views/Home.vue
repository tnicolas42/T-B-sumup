<template>
  <div id="flex-container">
		<fletch-box/>
    <p>Nb transactions: {{ nb_transactions }}</p>
  </div>
</template>

<script>
import axios from 'axios'
import FletchBox from '../components/FecthBox.vue'

export default {
  name: 'Home',
  components: {
		FletchBox
  },
  data () {
    return {
      nb_transactions: null,
    }
  },
  mounted () {
    axios
      .get(this.$store.state.api_url + '/transactions/size')
      .then(response => (this.nb_transactions = response.data.size))
  },
}
</script>

<style>
#flex-container {
	display: flex;
	flex-direction: column;
}
</style>
