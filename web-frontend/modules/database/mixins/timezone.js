import moment from 'moment'

export default {
  data() {
    return {
      allowedValues: ['timezone'],
      values: {
        timezone: this.getCurrentTimezone(),
      },
    }
  },
  methods: {
    getCurrentTimezone() {
      return moment.tz.guess()
    },
  },
}
