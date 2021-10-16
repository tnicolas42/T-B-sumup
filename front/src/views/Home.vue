<template>
  <div id="flex-container">
    <h1>Tim & Bastien</h1>
		<div id="fetching-block">
			<div>
				<button v-on:click="fetch_data">Fetch new data</button>
				<p :key="fetching_data.fetch_status">{{ fetching_data.fetch_status }}</p>
			</div>
		</div>
    <p>Nb transactions: {{ nb_transactions }}</p>
		<stats-table/>
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
			fetching_data: {
				fetch_status: "No fetching"
			}
    }
  },
  mounted () {
    axios
      .get(this.$store.state.api_url + '/transactions/size')
      .then(response => (this.nb_transactions = response.data.size))
		if (this.$route.query.sumup_code) {
			console.log("fetching data...")
			this.fetching_data.fetch_status = "Fetching..."
			axios
				.get(this.$store.state.api_url + '/transactions/fetch_all?sumup_code=' + this.$route.query.sumup_code)
				.then(() => {
					this.fetching_data.fetch_status = "Fetching OK"
				})
				.catch(error => {
					this.fetching_data.fetch_status = "Fetching ERROR"
					if (error.response) {
						console.log("error in /transactions/fetch_all\n"
							+ error.response.status + '\n'
							+ error.response.data)
					}
				})
		}
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
                window.location.href = connect_url
              })
          })
    }
  }
}
</script>

<style>
#flex-container {
	display: flex;
	flex-direction: column;
}

#fetching-block {
	display: flex;
	flex-direction: row;
	justify-content: center;
}

#fetching-block>div {
	border-style: solid;
	padding-top: 10px;
	padding-bottom: 0px;
	padding-left: 15px;
	padding-right: 15px;
}

</style>
