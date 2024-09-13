<template>
  <div>
    <form v-if="allDateFields.length > 0" @submit.prevent="submit">
      <FormElement class="control">
        <label class="control__label control__label--small">
          {{ $t('timelineViewSettingsForm.startDateField') }}
        </label>
        <div class="control__elements">
          <Dropdown v-model="values.startDateFieldId" :show-search="true">
            <DropdownItem :key="null" name="" :value="null">
              <div :style="{ height: '15px' }"></div>
            </DropdownItem>
            <DropdownItem
              v-for="dateField in allDateFields"
              v-if="dateField.id !== values.endDateFieldId"
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
          <Dropdown v-model="values.endDateFieldId" :show-search="true">
            <DropdownItem :key="null" name="" :value="null">
              <div :style="{ height: '15px' }"></div>
            </DropdownItem>
            <DropdownItem
              v-for="dateField in allDateFields"
              v-if="dateField.id !== values.startDateFieldId"
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
    viewSettings: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      values: {
        startDateFieldId: null,
        endDateFieldId: null,
      },
    }
  },
  mounted() {},
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
