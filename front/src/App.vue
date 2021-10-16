<template>
	<fragment>
		<div id="top">
			<h1> Tim & Bastien</h1>
			<img src='@/assets/logoV4_white_light.png' width="80vw" height="80vw"/>
		</div>
		<div id="app">
			<div id="nav">
				<router-link to="/">Home</router-link> |
				<router-link to="/produits_sem">Produits / semaines</router-link> |
				<router-link to="/about">About</router-link>
			</div>
			<router-view/>
		</div>
	</fragment>
</template>

<script>
export default ({
	mounted () {
		document.title = "Tim & Bastien - admin"
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
