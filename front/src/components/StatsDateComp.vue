<template>
	<fragment>
		<div id='topBox'>
			<div id='dateBox'>
				<div>
					<input type="checkbox" v-model="start_date_check"/>
					<Datepicker
						v-model="start_date"
						:value="start_date"
						:monday-first=true
					/>
				</div>
				<div>
					<input type="checkbox" v-model="end_date_check"/>
					<Datepicker
						v-model="end_date"
						:value="end_date"
						:monday-first=true
					/>
				</div>
				<button v-on:click="stats_interval">Validate</button>
			</div>

			<fetch-box/>
		</div>

		<template v-if="stats">
			<table>
				<tr>
					<td>Nb transactions</td>
					<td>{{ stats.nb_transactions }}</td>
				</tr>
				<tr>
					<td>Nb repas</td>
					<td>{{ stats.nb_repas }}</td>
				</tr>
				<tr>
					<td>Total brut</td>
					<td>{{ stats.total_brut }}</td>
				</tr>
				<tr>
					<td>Total net</td>
					<td>{{ stats.total_net }}</td>
				</tr>
			</table>

			<hr/>
			<template v-if="Object.keys(stats.categories).length > 0">
				<table>
					<tr>
						<th>Categorie</th>
						<th>Nb vendues</th>
					</tr>

					<tr v-for="(val, key) in stats.categories" :key="key">
						<td>{{ key }}</td>
						<td>{{ val }}</td>
					</tr>
				</table>

				<hr/>
			</template>
		</template>

		<template v-if="last_transaction">
			<table>
				<tr>
					<td>Last transaction date</td>
					<td>{{ last_transaction.time.slice(0, 19) }}</td>
				</tr>
				<tr>
					<td>Last transaction code</td>
					<td>{{ last_transaction.transaction_code }}</td>
				</tr>
				<tr>
					<td>Last transaction price</td>
					<td>{{ last_transaction.amount_brut }}</td>
				</tr>
			</table>

		</template>
	</fragment>
</template>

<script>
import axios from 'axios'
import Datepicker from 'vuejs-datepicker'
import FetchBox from '../components/FecthBox.vue'
import { to_euro } from '../plugins/utils'

export default {
	name: 'StatsDateComp',
	components: {
		Datepicker,
		FetchBox,
	},
  data() {
    return {
			start_date_check: true,
			end_date_check: true,
			start_date: new Date(),
			end_date: new Date(),
			stats: null,
			last_transaction: null,
    }
  },
	mounted() {
		this.stats_interval()
	},
	methods: {
		stats_interval: function() {
			let start = 'start_date=' + this.start_date.toLocaleDateString('fr-FR').replace("/", "_")
			let end = 'end_date=' + this.end_date.toLocaleDateString('fr-FR').replace("/", "_")
			let url = ''
			if (this.start_date_check) {
				url += '?' + start
			}
			if (this.start_date_check) {
				if (url == '') {
					url += '?'
				}
				else {
					url += '&'
				}
				url += end
			}
			axios
				.get(this.$store.state.api_url + '/stats/interval' + url)
				.then(response => {
					this.stats = response.data
					this.stats.total_brut = to_euro(this.stats.total_brut)
					this.stats.total_net = to_euro(this.stats.total_net)
				})
				.catch(error => {
					if (error.response) {
						console.log("error in /stats/interval\n"
							+ error.response.status + '\n'
							+ error.response.data)
					}
				})
			axios
				.get(this.$store.state.api_url + '/transactions/get/last')
				.then(response => {
					this.last_transaction = response.data
					this.last_transaction.amount_brut = to_euro(this.last_transaction.amount_brut)
					this.last_transaction.amount_net = to_euro(this.last_transaction.amount_net)
				})
				.catch(error => {
					if (error.response) {
						console.log("error in /transactions/get/last\n"
							+ error.response.status + '\n'
							+ error.response.data)
					}
				})
		},
	}
}
</script>

<style scoped>
#topBox {
	display: flex;
	flex-direction: row;
	justify-content: space-around;
}

#dateBox {
	display: flex;
	flex-direction: column;
	justify-content: center;
	border-style: solid;
	padding-top: 10px;
	padding-bottom: 10px;
	padding-left: 15px;
	padding-right: 15px;
	margin-bottom: 10px;
}

#dateBox>div {
	display: flex;
	flex-direction: row;
}
</style>
