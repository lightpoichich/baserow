<template>
  <div>
    <form v-if="allDateFields.length > 0" @submit.prevent="submit">
      <FormElement class="control">
        <label class="control__label control__label--small">
          {{ $t('timelineViewSettingsForm.startDateField') }}
        </label>
        <div class="control__elements">
          <Dropdown
            v-model="values.startDateFieldId"
            :show-search="true"
            :disabled="readOnly"
            :placeholder="readOnly ? ' ' : $t('action.makeChoice')"
          >
            <DropdownItem :key="null" name="" :value="null">
              <div :style="{ height: '15px' }"></div>
            </DropdownItem>
            <DropdownItem
              v-for="dateField in availableStartDateFields"
              :key="dateField.id"
              :name="dateField.name"
              :value="dateField.id"
              :icon="fieldIcon(dateField.type)"
            >
            </DropdownItem>
          </Dropdown>
          <div v-if="fieldHasErrors('startDateFieldId')" class="error">
            {{ $t('error.requiredField') }}
          </div>
        </div>
      </FormElement>
      <FormElement class="control margin-top-2">
        <label class="control__label control__label--small">
          {{ $t('timelineViewSettingsForm.endDateField') }}
        </label>
        <div class="control__elements">
          <Dropdown
            v-model="values.endDateFieldId"
            :show-search="true"
            :disabled="readOnly"
          >
            <DropdownItem :key="null" name="" :value="null">
              <div :style="{ height: '15px' }"></div>
            </DropdownItem>
            <DropdownItem
              v-for="dateField in availableEndDateFields"
              :key="dateField.id"
              :name="dateField.name"
              :value="dateField.id"
              :icon="fieldIcon(dateField.type)"
            >
            </DropdownItem>
          </Dropdown>
          <div v-if="fieldHasErrors('endDateFieldId')" class="error">
            {{ $t('error.requiredField') }}
          </div>
        </div>
      </FormElement>
      <slot></slot>
    </form>
    <div v-else class="warning">
      {{ $t('timelineViewSettingsForm.noCompatibleDateFields') }}
    </div>
  </div>
</template>

<script>
import { required } from 'vuelidate/lib/validators'
import form from '@baserow/modules/core/mixins/form'

export default {
  name: 'TimelineViewSettingsForm',
  mixins: [form],
  props: {
    allDateFields: {
      type: Array,
      required: true,
    },
    view: {
      type: Object,
      required: true,
    },
    readOnly: {
      type: Boolean,
      required: true,
    },
  },
  data() {
    return {
      values: {
        startDateFieldId: this.view.start_date_field || null,
        endDateFieldId: this.view.end_date_field || null,
      },
    }
  },
  computed: {
    availableStartDateFields() {
      return this.allDateFields.filter(
        (f) => f.id !== this.values.endDateFieldId
      )
    },
    availableEndDateFields() {
      return this.allDateFields.filter(
        (f) => f.id !== this.values.startDateFieldId
      )
    },
  },
  watch: {
    'view.start_date_field'(value) {
      if (this.values.startDateFieldId === null) {
        this.values.startDateFieldId = value
      }
    },
    'view.end_date_field'(value) {
      if (this.values.endDateFieldId === null) {
        this.values.endDateFieldId = value
      }
    },
  },
  methods: {
    fieldIcon(type) {
      const ft = this.$registry.get('field', type)
      return ft?.getIconClass() || 'calendar-alt'
    },
  },
  validations: {
    values: {
      startDateFieldId: { required },
      endDateFieldId: { required },
    },
  },
}
</script>
