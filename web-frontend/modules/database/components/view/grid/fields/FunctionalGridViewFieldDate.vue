<template functional>
  <div ref="cell" class="grid-view__cell">
    <div
      class="grid-field-date"
      :class="{ 'grid-field-date--has-time': props.field.date_include_time }"
    >
      <div
        ref="dateDisplay"
        class="grid-field-date__date"
        :class="{ 'grid-field-date-read-only__date': props.isReadOnly }"
      >
        {{ $options.methods.getDate(props.field, props.value) }}
      </div>
      <div
        v-if="props.field.date_include_time"
        ref="timeDisplay"
        class="grid-field-date__time"
        :class="{ 'grid-field-date-read-only__time': props.isReadOnly }"
      >
        {{ $options.methods.getTime(props.field, props.value) }}
      </div>
    </div>
  </div>
</template>

<script>
import readOnlyDateField from '@baserow/modules/database/mixins/readOnlyDateField'

export default {
  name: 'FunctionalGridViewFieldDate',
  mixins: [readOnlyDateField],
  props: {
    isReadOnly: {
      type: Boolean,
      required: false,
      default: false,
    },
    field: {
      type: Object,
      required: true,
    },
    value: {
      type: String,
      required: false,
      default: '',
    },
  },
  mounted() {
    console.log('HELLO WHATUP')
  },
}
</script>
