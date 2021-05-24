<script>
import { Line } from 'vue-chartjs'

export default {
  extends: Line,
  props: {
    newUsers: {
      type: Array,
      required: true,
    },
    activeUsers: {
      type: Array,
      required: true,
    },
  },
  mounted() {
    const labels = []
    const day = 24 * 60 * 60 * 1000
    for (let i = 0; i < 30; i++) {
      const time = new Date().getTime() - day * i
      const date = new Date(time)
      labels.unshift(
        new Date(date.getFullYear(), date.getMonth(), date.getDate())
      )
    }

    const newUserData = this.mapCount(labels, this.newUsers)
    const activeUserData = this.mapCount(labels, this.activeUsers)

    this.renderChart(
      {
        labels,
        datasets: [
          {
            label: 'New users',
            borderColor: '#59cd90',
            backgroundColor: 'transparent',
            color: '#9bf2c4',
            data: newUserData,
          },
          {
            label: 'Active users',
            borderColor: '#198dd6',
            backgroundColor: 'transparent',
            color: '#b4bac2',
            data: activeUserData,
          },
        ],
      },
      {
        responsive: true,
        maintainAspectRatio: false,
        legend: {
          align: 'start',
          position: 'bottom',
        },
        scales: {
          xAxes: [
            {
              type: 'time',
              time: {
                displayFormats: {
                  day: 'MMM D',
                },
                tooltipFormat: 'MMM D',
              },
            },
          ],
        },
      }
    )
  },
  methods: {
    dateEquals(date1, date2) {
      return (
        date1.getDate() === date2.getDate() &&
        date1.getMonth() === date2.getMonth() &&
        date1.getFullYear() === date2.getFullYear()
      )
    },
    mapCount(labels, values) {
      return labels.map((date1) => {
        for (let i = 0; i < values.length; i++) {
          const date2 = new Date(values[i].date)
          if (this.dateEquals(date1, date2)) {
            return values[i].count
          }
        }
        return 0
      })
    },
  },
}
</script>
