<template>
  <div>
    {{ localDate }}
  </div>
</template>

<script>
import moment from 'moment'
export default {
  name: 'LocalDateField',
  props: {
    row: {
      required: true,
      type: Object,
    },
    column: {
      required: true,
      type: Object,
    },
  },
  computed: {
    localDate() {
      const date = this.row[this.column.key]
      if (date) {
        return moment.utc(date).local().format('L LT')
      } else {
        return ''
      }
    },
  },
}
</script>
