<template>
	<div id="fetching-block">
		<div>
			<button v-on:click="fetch_data">Fetch new data</button>
			<p :key="fetching_data.fetch_status">{{ fetching_data.fetch_status }}</p>
		</div>
	</div>
</template>

<script>
import axios from 'axios'

export default {
	name: 'FetchBox',
	data () {
		return {
			fetching_data: {
				fetch_status: "No fetching"
			}
		}
	},
	mounted () {
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
        .get(this.$store.state.api_url + '/set_redirect_url?url=' + window.location.href)
        .then(() => {
          axios
            .get(this.$store.state.api_url + '/get_connect_url')
            .then(response => {
                connect_url = response.data
                window.location.href = connect_url
              })
          })
    }
  },
}
</script>


<style>
#fetching-block {
	display: flex;
	flex-direction: row;
	justify-content: center;
	margin-bottom: 10px;
}

#fetching-block>div {
	border-style: solid;
	padding-top: 10px;
	padding-bottom: 0px;
	padding-left: 15px;
	padding-right: 15px;
}
</style>