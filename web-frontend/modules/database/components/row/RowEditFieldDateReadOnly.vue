<template>
  <div class="control__elements">
    <div class="field-date__container">
      <div class="input__with-icon field-date">
        <input
          ref="date"
          v-model="date"
          type="text"
          class="input input--large"
          :disabled="true"
        />
        <i class="fas fa-calendar-check"></i>
      </div>
      <div
        v-if="field.date_include_time"
        class="input__with-icon field-date__time"
      >
        <input
          ref="time"
          v-model="time"
          type="text"
          class="input input--large"
          :class="{ 'input--error': touched && !valid }"
          :disabled="true"
        />
        <i class="fas fa-clock"></i>
      </div>
    </div>
  </div>
</template>

<script>
import rowEditField from '@baserow/modules/database/mixins/rowEditField'
import rowEditFieldInput from '@baserow/modules/database/mixins/rowEditFieldInput'
import dateField from '@baserow/modules/database/mixins/dateField'

export default {
  mixins: [rowEditField, rowEditFieldInput, dateField],
}
</script>
