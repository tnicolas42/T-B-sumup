<template>
	<fragment>
		<tr>
			<th colspan="7">Semaine {{ weekname }}</th>
		</tr>
		<template v-if="isDataLoaded">
			<tr v-for="(payment_type, index) in payment_type" :key="index">
				<td>{{ payment_type.payment }}</td>
				<td>{{ weekname }}</td>
				<td>Vente</td>
				<td>{{ payment_type.net }}</td>
				<td>Recu</td>
				<td>NA</td>
				<td v-if="index == 0">total brut: {{ total.brut }}</td>
				<td v-else-if="index == 1">total net: {{ total.net }}</td>
				<td v-else></td>
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
			payment_type: null,
			total: null,
			isDataLoaded: false,
		}
	},
	created () {
		axios
			.get(this.$store.state.api_url + '/stats/week/' + this.weekname.replaceAll('/', '_') + '/total')
			.then(response => {
				this.payment_type = []
				this.total = {
					'brut': to_euro(response.data.total_brut),
					'net': to_euro(response.data.total_net),
				}
				for (let payment in response.data.payment_type) {
					this.payment_type.push({
						'payment': payment,
						'net': to_euro(response.data.payment_type[payment].total_net),
						'brut': to_euro(response.data.payment_type[payment].total_brut),
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
