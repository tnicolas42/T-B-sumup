<template>
  <div>
    <input v-model="nb_people_recipe" placeholder="edit me" type="number">
    <div class="recipe_buttons" v-for="(recipe, idx) in recipes" :key="idx">
      <button v-on:click="download_recipe(recipe.id, nb_people_recipe)">{{ recipe.name }}</button>
      <!-- <img src="@/assets/recipes/tranche.png"/> -->
      <img :src="require(recipe.img)"/>
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
    require('../assets/recipes/tranche.png')
    return {
      recipes: null,
      nb_people_recipe: 4,
    }
  },
  mounted () {
    axios
      .get(this.$store.state.api_url + '/recipe/list_with_image')
      .then(response => {
        this.recipes = response.data.data

          for (var i = 0; i < this.recipes.length; i++) {
            this.recipes[i].img = '@/' + this.recipes[i].img_path
            // this.recipes[i].img = 'recipes/tranche.png'
          }
      })
  },
  methods: {
    download_recipe: function(file_id, nb) {
      console.log("download recipe for " + nb)
			axios
        .get(this.$store.state.api_url + "/recipe/download/" + file_id + "/" + nb)
        .then(response => {
          window.location.href = response.data
        })
    }
  }
}
</script>

<style scoped>
.recipe_buttons {
  display: flex;
  flex-direction: column;
}

.recipe_buttons>button {
  background-color: #4CAF50; /* Green */
  border: none;
  color: white;
  padding: 15px 32px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  border-radius: 12px;
  margin: 2px;
}
</style>