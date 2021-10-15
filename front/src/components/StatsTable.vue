<template>
<div>
	<h1>Produits</h1>
	<h2>Total</h2>
		<table>
		<tr>
			<th>Initulé</th>
			<th>Total</th>
		</tr>
		<tr>
			<td>Net</td>
			<td>{{ total_net }}</td>
		</tr>
		<tr>
			<td>Brut</td>
			<td>{{ total_brut }}</td>
		</tr>
	</table>
	<h2>Par semaines</h2>
	<table>
		<tr>
			<th>Initulé</th>
			<th>Date</th>
			<th>Catégorie</th>
			<th>Montant</th>
			<th>status</th>
			<th>Justif</th>
			<th>Commentaire</th>
		</tr>
		<template v-for="(week, idx) in weeks">
			<stats-table-one-week :key="idx" :weekname="week"/>
		</template>
	</table>
</div>
</template>

<script>
import axios from 'axios'
import { to_euro } from '../plugins/utils'
import StatsTableOneWeek from '../components/StatsTableOneWeek.vue'

export default {
	name: 'StatsTable',
  components: {
		StatsTableOneWeek
  },
	data () {
		return {
			total_net: null,
			total_brut: null,
			weeks: null,
		}
	},
	created () {
		axios
			.get(this.$store.state.api_url + '/stats/get_weeks')
			.then(response => {
				this.weeks = response.data.weeks
				// var tmp_weeks = new Array(response.data.weeks.length)
				// for (let week in response.data.weeks) {
					// axios
					// 	.get(this.$store.state.api_url + '/stats/week/' + response.data.weeks[week].replaceAll('/', '_') + '/total')
					// 	.then(response_week => {
					// 		tmp_weeks[week] = {
					// 			'weekname': response.data.weeks[week],
					// 			'payment': []
					// 		}
					// 		for (let payment in response_week.data) {
					// 			tmp_weeks[week].payment.push({
					// 				'payment': payment,
					// 				'net': to_euro(response_week.data[payment].total_net),
					// 				'brut': to_euro(response_week.data[payment].total_brut),
					// 			})
					// 		}
					// 	})
				// }
				// this.weeks = tmp_weeks
			})
	},
	mounted () {
		axios
			.get(this.$store.state.api_url + '/stats/total')
			.then(response => {
				this.total_net = to_euro(response.data.total_net)
				this.total_brut = to_euro(response.data.total_brut)
			})
	},
}
</script>

<style>
table {
  font-family: arial, sans-serif;
  border-collapse: collapse;
  width: 100%;
}

td, th {
  border: 1px solid #dddddd;
  text-align: center;
  padding: 8px;
}

tr:nth-child(even) {
  background-color: #dddddd;
}
</style>
