<template>
  <div class="view-date-selector">
    <a class="view-date-selector__prev" @click="selectPrevious">
      <i class="iconoir-nav-arrow-left"></i>
    </a>
    <a class="view-date-selector__next" @click="selectNext">
      <i class="iconoir-nav-arrow-right"></i>
    </a>

    <Button type="secondary" size="large" @click="selectCurrent">
      {{ $t('viewDateSelector.today') }}
    </Button>
  </div>
</template>

<script>
import moment from '@baserow/modules/core/moment'

export default {
  name: 'ViewDateSelector',
  props: {
    selectedDate: {
      type: Object,
      required: true,
    },
  },
  methods: {
    selectPrevious() {
      const newSelectedDate = moment(this.selectedDate).subtract(1, 'month')
      this.$emit('date-selected', newSelectedDate)
    },
    selectCurrent() {
      this.$emit('date-selected', moment())
    },
    selectNext() {
      const newSelectedDate = moment(this.selectedDate).add(1, 'month')
      this.$emit('date-selected', newSelectedDate)
    },
  },
}
</script>
