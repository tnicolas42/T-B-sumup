<template>
	<div id="fetching-block">
		<div>
			<div id="auto_fetching" v-if="$store.state.is_connected">
				<input type="checkbox" v-model="auto_fetching"/>
				<p>Auto fetching</p>
			</div>

			<div v-if="$store.state.is_connected">
				<button v-on:click="fetch_data">Fetch new data</button>
			</div>
			<div v-else>
				<p>Connect before fetch data</p>
			</div>
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
			},
			auto_fetching: false,
			interval: null,
		}
	},
	mounted () {
		this.interval = setInterval(this.recurentCallback, this.$store.state.fetching_interval);
		this.recurentCallback();
	},
	destroyed() {
    clearInterval(this.interval);
  },
  methods: {
		recurentCallback: function () {
			if (this.$store.state.is_connected && this.auto_fetching) {
				this.fetch_data()
			}
		},
    fetch_data: function() {
			if (this.fetching_data.fetch_status != "Fetching...") {
				console.log("fetching data...")
				this.fetching_data.fetch_status = "Fetching..."
				axios
					.get(this.$store.state.api_url + '/transactions/fetch_all')
					.then(() => {
						this.fetching_data.fetch_status = "Fetching OK"
					})
					.catch(error => {
						if (error.response.status == 401) {
							this.fetching_data.fetch_status = "Fetching ERROR (not connected)"
						}
						else {
							this.fetching_data.fetch_status = "Fetching ERROR"
						}
						if (error.response) {
							console.log("error in /transactions/fetch_all\n"
								+ error.response.status + '\n'
								+ error.response.data)
						}
					})
			}
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

#auto_fetching {
	display: flex;
	flex-direction: row;
}
#auto_fetching>p {
	margin-top: 0px;
	margin-bottom: 0px;
	margin-left: 5px;
}
</style>