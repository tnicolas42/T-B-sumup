<template>
  <div>
    <div id="update-box">
      <button v-on:click="reset_recipes()">Reset recipes</button>
      <button v-on:click="update_recipes()">Update recipes</button>
      <div class="checkbox-text">
        <input type="checkbox" v-model="update_only_new"/>
        <p>Check only for new recipe (otherwise, update all recipes)</p>
      </div>
    </div>
    <div id="search-box">
      <input v-model="search_string" placeholder="search..." type="string" v-on:keyup="search_recipes(search_string, search_only_on_name)">
      <div class="checkbox-text">
        <input type="checkbox" v-model="search_only_on_name" v-on:click="search_recipes(search_string, !search_only_on_name)"/>
        <p>Only on name</p>
      </div>
    </div>
    <select v-model="chosen_categorie" @change="search_recipes(search_string, search_only_on_name)" v-if="categorie_list">
      <option v-for="(cat, idx) in categorie_list" :key="idx">{{ cat }}</option>
    </select>
    <select v-model="chosen_allergenic" multiple @change="search_recipes(search_string, search_only_on_name)" v-if="allergenic_list">
      <option v-for="(allergenic, idx) in allergenic_list" :key="idx">{{ allergenic }}</option>
    </select>
    <br>
    <span>Conviens aux allergies suivantes: {{ chosen_allergenic }}</span>
    <div class="recipes">
      <div class="recipe-card" v-for="(recipe, idx) in recipes" :key="idx">
        <div class="recipe-image" v-bind:style="{ backgroundImage: 'url(' + recipe.img_url + ')' }">
          <div class="recipe-name"><b>{{ recipe.name }}</b></div>
        </div>
        <div class="icons">
          <img src="@/assets/icons/google_sheets.png" v-on:click="open_recipe(recipe.id)">
          <input v-model="recipe.nb_people_recipe" placeholder="edit me" type="number">
          <img src="@/assets/icons/download.png" v-on:click="download_recipe(recipe.id, recipe.nb_people_recipe)">
        </div>
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
      update_only_new: true,
      search_string: "",
      search_only_on_name: false,
      allergenic_list: null,
      chosen_allergenic: [],
      categorie_list: null,
      chosen_categorie: 'All',
    }
  },
  mounted () {
    this.search_recipes("")
    axios
      .get(this.$store.state.api_url + "/recipe/allergenic_list")
      .then(response => {
        this.allergenic_list = response.data.data
      })
    axios
      .get(this.$store.state.api_url + "/recipe/categorie_list")
      .then(response => {
        this.categorie_list = response.data.data
        this.categorie_list.push('All')
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
    open_recipe: function(file_id) {
      window.open('https://docs.google.com/spreadsheets/d/' + file_id, '_blank')
    },
    update_recipes: function () {
      console.log("update recipes")
      axios
        .get(this.$store.state.api_url + '/recipe/fetch?only_new=' + this.update_only_new)
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
    },
    search_recipes: function (searchstr, onlyname=false) {
      var allergenic_data = ""
      if (this.chosen_allergenic != null) {
        for (const al of this.chosen_allergenic) {
          if (allergenic_data != '') {
            allergenic_data += '.'
          }
          allergenic_data += al
        }
      }
      console.log(allergenic_data)
      var req = this.$store.state.api_url + '/recipe/list?search=' + searchstr + '&only_name=' + onlyname + '&categorie=' + this.chosen_categorie + '&allergenic=' + allergenic_data
      console.log("search repices (" + req + ")")
      axios
        .get(req)
        .then(response => {
          this.recipes = response.data.data
          console.log(this.recipes)
          for (var i = 0; i < this.recipes.length; i++) {
            this.recipes[i].img_url = this.$store.state.api_url + '/recipe/image/' + this.recipes[i].id
            this.recipes[i].nb_people_recipe = 4
          }
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
  flex-wrap: wrap;
  justify-content: flex-start;
  align-content: center;
}

.recipe-card {
  display: flex;
  flex-direction: column;
  margin: 1%;
  padding: 0.5%;
  width: 200px;
  height: 240px;
  display: flex;
  background-color: rgba(255, 255, 255, 0.144);
}
.recipe-card:hover {
  background-color: rgba(190, 190, 190, 0.445);
}

.recipe-image {
  min-height: 200px;
  min-width: 200px;
  background-position: 50% 50%;
  background-size: cover;
  align-content: flex-end;
}

.recipe-name {
  color: #000;
  display: flex;
  min-height: 15%;
  min-width: 100%;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  align-self: center;
  flex: 0 auto;
  border-radius: 0px;
  background-color: rgb(193 193 193 / 56%);
  font-size: 15px;
  line-height: 15px;
}

.icons {
  display: flex;
  flex-direction: row;
  justify-content: space-around;
  align-items: center;
  margin-top: 5px;
  height: 40px;
}
.icons>input {
  width: 100px;
  height: 18px;
}
.icons>img {
  max-width: 30px;
  max-height: 30px;
}
.icons>img:hover {
  max-width: 35px;
  max-height: 35px;
}

#update-box {
  display: flex;
  flex-direction: row;
  justify-content: center;
  margin: 10px;
}
#search-box {
  display: flex;
  flex-direction: row;
  justify-content: center;
  margin: 10px;
}

.checkbox-text {
	display: flex;
	flex-direction: row;
}
.checkbox-text>p {
	margin-top: 0px;
	margin-bottom: 0px;
	margin-left: 5px;
}
</style>