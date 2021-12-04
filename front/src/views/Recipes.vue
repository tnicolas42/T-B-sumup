<template>
  <div>
    <button v-on:click="reset_recipes()">Reset recipes</button>
    <button v-on:click="update_recipes()">Update recipes</button>
    <input v-model="nb_people_recipe" placeholder="edit me" type="number">
    <div class="recipes">
      <div class="recipe-card" v-on:click="download_recipe(recipe.id, nb_people_recipe)" v-for="(recipe, idx) in recipes" :key="idx">
        <img class="recipe-image" :src=recipe.img_url>
        <p class="recipe-info">{{ recipe.name }}</p>
      </div>
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
      nb_people_recipe: 4,
    }
  },
  mounted () {
    axios
      .get(this.$store.state.api_url + '/recipe/list')
      .then(response => {
        this.recipes = response.data.data
        for (var i = 0; i < this.recipes.length; i++) {
          this.recipes[i].img_url = this.$store.state.api_url + '/recipe/image/' + this.recipes[i].id
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
    },
    update_recipes: function () {
      console.log("update recipes")
      axios
        .get(this.$store.state.api_url + '/recipe/fetch')
        .then(response => {
          console.log("update recipe: OK")
        })
        .catch(error => {
          console.log("update recipe: ERROR")
        })
    },
    reset_recipes: function () {
      console.log("reset recipes")
      axios
        .get(this.$store.state.api_url + '/recipe/reset')
        .then(response => {
          this.update_recipes()
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

.recipes {
  display: flex;
  /* flex-direction: row; */
  flex-wrap: wrap;
  justify-content: start;
  align-content: flex-start;
}

.recipe-card {
  display: flex;
  flex-direction: column;
  /* position: relative; */
  /* text-align: center; */
  /* max-width: 200; */
  /* max-height: 200; */
  padding: 2%;
  flex-basis: 16%;

  display: flex;
}

.recipe-image {
  max-width: 100%;
}

.recipe-info {
  /* position: absolute;
  bottom: 0%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: white; */
}
</style>