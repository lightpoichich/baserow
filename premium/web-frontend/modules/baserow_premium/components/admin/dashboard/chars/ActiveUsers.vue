<script>
import { Line } from 'vue-chartjs'

export default {
  extends: Line,
  mounted() {
    this.renderChart(
      {
        labels: [
          new Date(2021, 0, 1),
          new Date(2021, 0, 2),
          new Date(2021, 0, 3),
          new Date(2021, 0, 4),
          new Date(2021, 0, 5),
          new Date(2021, 0, 6),
          new Date(2021, 0, 7),
          new Date(2021, 0, 8),
          new Date(2021, 0, 9),
          new Date(2021, 0, 10),
          new Date(2021, 0, 11),
          new Date(2021, 0, 12),
          new Date(2021, 0, 13),
          new Date(2021, 0, 14),
          new Date(2021, 0, 15),
          new Date(2021, 0, 16),
          new Date(2021, 0, 17),
          new Date(2021, 0, 18),
          new Date(2021, 0, 19),
          new Date(2021, 0, 20),
          new Date(2021, 0, 21),
          new Date(2021, 0, 22),
          new Date(2021, 0, 23),
          new Date(2021, 0, 24),
          new Date(2021, 0, 25),
          new Date(2021, 0, 26),
          new Date(2021, 0, 27),
          new Date(2021, 0, 28),
          new Date(2021, 0, 29),
          new Date(2021, 0, 30),
        ],
        datasets: [
          {
            label: '',
            borderColor: '#198dd6',
            backgroundColor: '#ebf7ff',
            color: '#b4bac2',
            data: [
              40,
              39,
              10,
              40,
              39,
              80,
              40,
              40,
              39,
              10,
              40,
              39,
              80,
              40,
              40,
              39,
              10,
              40,
              39,
              80,
              40,
              40,
              39,
              10,
              40,
              39,
              80,
              40,
              10,
              20,
            ],
          },
        ],
      },
      {
        responsive: true,
        maintainAspectRatio: false,
        legend: {
          display: false,
        },
        scales: {
          xAxes: [
            {
              type: 'time',
              time: {
                displayFormats: {
                  quarter: 'MMM D',
                },
              },
            },
          ],
        },
      }
    )
  },
}
</script>
