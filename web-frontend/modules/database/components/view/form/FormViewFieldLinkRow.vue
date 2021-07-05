<template>
  <div class="control__elements">
    <PaginatedDropdown
      :fetch-page="fetchPage"
      :value="dropdownValue"
      :class="{ 'dropdown--error': touched && !valid }"
      @input="updateValue($event)"
      @hide="touch()"
    ></PaginatedDropdown>
    <div v-show="touched && !valid" class="error">
      {{ error }}
    </div>
  </div>
</template>

<script>
import PaginatedDropdown from '@baserow/modules/core/components/PaginatedDropdown'
import rowEditField from '@baserow/modules/database/mixins/rowEditField'
import FormService from '@baserow/modules/database/services/view/form'

export default {
  name: 'FormViewFieldLinkRow',
  components: { PaginatedDropdown },
  mixins: [rowEditField],
  props: {
    slug: {
      type: String,
      required: true,
    },
  },
  computed: {
    dropdownValue() {
      return this.value.length === 0 ? null : this.value[0].id
    },
  },
  methods: {
    fetchPage(page, search) {
      return FormService(this.$client).linkRowFieldLookup(
        this.slug,
        this.field.id,
        page,
        search
      )
    },
    updateValue(value) {
      this.$emit('update', value === null ? [] : [{ id: value }], this.value)
    },
  },
}
</script>
