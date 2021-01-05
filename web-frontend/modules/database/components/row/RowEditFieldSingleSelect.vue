<template>
  <div class="control__elements">
    <FieldSingleSelectDropdown
      :value="valueId"
      :options="field.select_options"
      @input="updateValue($event, value)"
    ></FieldSingleSelectDropdown>
  </div>
</template>

<script>
import rowEditField from '@baserow/modules/database/mixins/rowEditField'
import singleSelectField from '@baserow/modules/database/mixins/singleSelectField'

export default {
  name: 'RowEditFieldSingleSelectVue',
  mixins: [rowEditField, singleSelectField],
}
</script>
