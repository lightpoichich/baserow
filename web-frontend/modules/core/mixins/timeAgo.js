import { getHumanPeriodAgoCount } from '@baserow/modules/core/utils/date'

export default {
  data() {
    return {
      timeAgo: '',
      refreshPeriod: null,
    }
  },
  mounted() {
    this.updateTimeAgo()
    if (this.refreshPeriod) {
      this.interval = setInterval(this.updateTimeAgo, this.refreshPeriod)
    }
  },
  beforeDestroy() {
    clearInterval(this.interval)
  },
  methods: {
    updateTimeAgo() {
      const { period, count } = getHumanPeriodAgoCount(this.lastUpdated)
      if (period === 'seconds' && count <= 5) {
        this.timeAgo = this.$t('datetime.justNow')
        this.refreshPeriod = 1000
      } else if (period === 'seconds') {
        this.timeAgo = this.$t('datetime.fewSecondsAgo')
        this.refreshPeriod = 5 * 1000
      } else {
        this.refreshPeriod = period === 'minutes' ? 60 * 1000 : 3600 * 1000
        this.timeAgo = this.$tc(`datetime.${period}Ago`, count)
      }
    },
  },
}
