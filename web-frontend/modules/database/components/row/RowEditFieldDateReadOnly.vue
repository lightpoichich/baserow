<template>
  <div class="control__elements">
    <div
      class="row-edit-field-date-read-only-container"
      :class="{
        'row-edit-field-date-read-only--has-time': field.date_include_time,
      }"
    >
      <div ref="dateDisplay" class="row-edit-field-date-read-only__date">
        {{ getDate(field, value) }}
      </div>
      <div
        v-if="field.date_include_time"
        ref="timeDisplay"
        class="row-edit-field-date-read-only__time"
      >
        {{ getTime(field, value) }}
      </div>
    </div>
  </div>
</template>

<script>
import rowEditField from '@baserow/modules/database/mixins/rowEditField'
import readOnlyDateField from '@baserow/modules/database/mixins/readOnlyDateField'

export default {
  mixins: [rowEditField, readOnlyDateField],
}
</script>
