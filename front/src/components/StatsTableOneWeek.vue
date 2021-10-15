<template>
	<fragment>
		<tr>
			<th colspan="7">Semaine {{ weekname }}</th>
		</tr>
		<template v-if="isDataLoaded">
			<tr v-for="(payment_type, index) in week" :key="index">
				<td>{{ payment_type.payment }}</td>
				<td>{{ weekname }}</td>
				<td>Vente</td>
				<td>{{ payment_type.net }}</td>
				<td>Recu</td>
				<td>NA</td>
				<td></td>
			</tr>
		</template>
	</fragment>
</template>

<script>
import axios from 'axios'
import { to_euro } from '../plugins/utils'

export default {
	name: 'StatsTableOneWeek',
	props: {
		weekname: String,
	},
	data () {
		return {
			week: null,
			isDataLoaded: false,
		}
	},
	created () {
		axios
			.get(this.$store.state.api_url + '/stats/week/' + this.weekname.replaceAll('/', '_') + '/total')
			.then(response => {
				this.week = []
				for (let payment in response.data) {
					this.week.push({
						'payment': payment,
						'net': to_euro(response.data[payment].total_net),
						'brut': to_euro(response.data[payment].total_brut),
					})
				}
				this.isDataLoaded = true
			})
	},
	mounted () {
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
