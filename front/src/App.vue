<template>
	<fragment>
		<div id="top">
			<img src='@/assets/logoV4_white_light.png' width="80vw" height="80vw"/>
			<h1> Tim & Bastien</h1>
			<div v-if="$store.state.is_connected">
				<p>Connected !</p>
			</div>
			<div v-else>
				<button v-on:click="connect">Connect</button>
			</div>
		</div>
		<div id="app">
			<div id="nav">
				<router-link to="/">Home</router-link> |
				<router-link to="/produits_sem">Produits / semaines</router-link> |
				<router-link to="/stats_date">Stats</router-link> | 
				<router-link to="/recipes">Recettes</router-link>
			</div>
			<router-view/>
		</div>
	</fragment>
</template>

<script>
import axios from 'axios'

export default ({
	data () {
		return {
			interval: null,
		}
	},
	mounted () {
		document.title = "Tim & Bastien - admin"
		this.interval = setInterval(this.recurentCallback, this.$store.state.connect_interval);
		this.recurentCallback();
	},
	methods: {
		recurentCallback: function () {
			this.updateIsConnected()
		},
		updateIsConnected: function() {
			axios
				.get(this.$store.state.api_url + '/is_connected')
				.then(response => {
					this.$store.state.is_connected = response.data.connected
				})
		},
    connect: function() {
      console.log("connecting to sumup");
      var connect_url = null;
      axios
        .get(this.$store.state.api_url + '/set_redirect_url?url=' + window.location.href.split('?')[0])
        .then(() => {
          axios
            .get(this.$store.state.api_url + '/get_connect_url')
            .then(response => {
								connect_url = response.data
                window.location.href = connect_url
              })
          })
    },
	}
})
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav {
  padding-bottom: 10px;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}

#top {
	display: flex;
	flex-direction: row;
	justify-content: space-between;
}

#top>h1 {
	text-align: center;
}

</style>
