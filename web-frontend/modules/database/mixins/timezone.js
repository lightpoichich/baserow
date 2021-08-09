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
      return new Intl.DateTimeFormat().resolvedOptions().timeZone
    },
  },
}
