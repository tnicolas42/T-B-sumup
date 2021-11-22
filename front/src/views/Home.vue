<template>
  <div id="flex-container">
		<fetch-box/>
    <p>Nb transactions: {{ nb_transactions }}</p>
    <p>Charges totales: {{ total_charges }}</p>
    <p>Produits totaux: {{ total_produits }} (recu: {{ produits_recu }})</p>
  </div>
</template>

<script>
import axios from 'axios'
import FetchBox from '../components/FecthBox.vue'

export default {
  name: 'Home',
  components: {
		FetchBox
  },
  data () {
    return {
      nb_transactions: null,
      total_charges: null,
      total_produits: null,
      produits_recu: null,
    }
  },
  mounted () {
    axios
      .get(this.$store.state.api_url + '/transactions/size')
      .then(response => (this.nb_transactions = response.data.size))
    axios
      .get(this.$store.state.api_url + '/compte/charges')
      .then(response => (this.total_charges = response.data.charges))
    axios
      .get(this.$store.state.api_url + '/compte/produits')
      .then(response => {
        this.total_produits = response.data.produits
        this.produits_recu = response.data.recu
      })
  },
}
</script>

<style>
#flex-container {
	display: flex;
	flex-direction: column;
}
</style>
