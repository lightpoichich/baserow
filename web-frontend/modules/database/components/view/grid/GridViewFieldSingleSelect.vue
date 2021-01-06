<template>
  <div ref="cell" class="grid-view__cell" :class="{ active: selected }">
    <div
      ref="dropdownLink"
      class="grid-field-single-select"
      :class="{ 'grid-field-single-select--selected': selected }"
      @click="toggleDropdown()"
    >
      <div
        v-if="value !== null"
        class="grid-field-single-select__option"
        :class="'background-color--' + value.color"
      >
        {{ value.value }}
      </div>
      <i
        v-if="selected"
        class="fa fa-caret-down grid-field-single-select__icon"
      ></i>
    </div>
    <FieldSingleSelectDropdown
      v-if="selected"
      ref="dropdown"
      :value="valueId"
      :options="field.select_options"
      :show-input="false"
      :allow-create-option="true"
      class="dropdown--floating grid-field-single-select__dropdown"
      @show="editing = true"
      @hide="editing = false"
      @input="updateValue($event, value)"
      @create-option="createOption($event)"
    ></FieldSingleSelectDropdown>
  </div>
</template>

<script>
import gridField from '@baserow/modules/database/mixins/gridField'
import singleSelectField from '@baserow/modules/database/mixins/singleSelectField'

export default {
  mixins: [gridField, singleSelectField],
  data() {
    return {
      editing: false,
    }
  },
  methods: {
    toggleDropdown(value) {
      if (!this.selected) {
        return
      }

      this.$refs.dropdown.toggle(this.$refs.dropdownLink, value)
    },
    hideDropdown() {
      this.$refs.dropdown.hide()
    },
    select() {
      this.$el.keydownEvent = (event) => {
        // When the escape key is pressed while editing the value we can hide the
        // dropdown.
        if (event.keyCode === 27 && this.editing) {
          this.hideDropdown()
          return
        }

        // When the enter key is pressed when not editing the value we want to show the
        // dropdown.
        if (event.keyCode === 13 && !this.editing) {
          this.toggleDropdown()
        }
      }
      document.body.addEventListener('keydown', this.$el.keydownEvent)
    },
    beforeUnSelect() {
      this.hideDropdown()
      document.body.removeEventListener('keydown', this.$el.keydownEvent)
    },
    canSelectNext() {
      return !this.editing
    },
    canCopy() {
      return !this.editing
    },
    canPaste() {
      return !this.editing
    },
    canEmpty() {
      return !this.editing
    },
  },
}
</script>
