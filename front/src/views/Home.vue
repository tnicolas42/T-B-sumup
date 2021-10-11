<template>
  <div>
    <h1>Tim & Bastien</h1>
    <p>Nb transactions: {{ nb_transactions }}</p>
		<stats-table/>
    <button v-on:click="fetch_data">Fetch new data</button>
  </div>
</template>

<script>
import axios from 'axios'
import StatsTable from '../components/StatsTable.vue'

export default {
  name: 'Home',
  components: {
		StatsTable
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
  methods: {
    fetch_data: function() {
      console.log("fetch new data");
      var connect_url = null;
      axios
        .get(this.$store.state.api_url + '/set_redirect_url?url=http://127.0.0.1:8080')
        .then(() => {
          axios
            .get(this.$store.state.api_url + '/get_connect_url')
            .then(response => {
                connect_url = response.data
                console.log(connect_url)
                window.location.href = connect_url
              })
          })
    }
  }
}
</script>
