<template>
  <div>
    <div v-for="(name, id) in recipes" :key="id">
      <button v-on:click="download_recipe(id, 12)">Telecharger {{ name }}</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Recipes',
  components: {
  },
  data () {
    return {
      recipes: null,
    }
  },
  mounted () {
    axios
      .get(this.$store.state.api_url + '/recipe/list')
      .then(response => {
        this.recipes = response.data
        console.log(this.recipes)
      })
  },
  methods: {
    download_recipe: function(file_id, nb) {
      console.log("download recipe")
			axios
        .get(this.$store.state.api_url + "/recipe/download/" + file_id + "/" + nb)
        .then(response => {
          window.location.href = response.data
        })
    }
  }
}
</script>
