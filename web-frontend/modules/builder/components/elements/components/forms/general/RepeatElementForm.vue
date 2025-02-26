<template>
  <form @submit.prevent @keydown.enter.prevent>
    <FormGroup
      v-show="dataSourceDropdownAvailable"
      :label="$t('dataSourceDropdown.label')"
      small-label
      required
      class="margin-bottom-2"
    >
      <DataSourceDropdown
        v-model="values.data_source_id"
        small
        :data-sources="dataSources"
        :page="page"
      >
        <template #chooseValueState>
          {{ $t('collectionElementForm.noDataSourceMessage') }}
        </template>
      </DataSourceDropdown>
    </FormGroup>
    <FormGroup
      v-show="propertySelectorAvailable"
      small-label
      required
      class="margin-bottom-2"
      :label="$t('serviceSchemaPropertySelector.label')"
    >
      <ServiceSchemaPropertySelector
        v-model="values.schema_property"
        small
        :schema="propertySelectorSchema"
      >
        <template #emptyState>
          {{ $t('repeatElementForm.propertySelectorMissingArrays') }}
        </template>
        <template #chooseValueState>
          {{ $t('collectionElementForm.noSchemaPropertyMessage') }}
        </template>
      </ServiceSchemaPropertySelector>
    </FormGroup>
    <FormGroup
      v-show="pagingOptionsAvailable"
      :label="$t('repeatElementForm.itemsPerPage')"
      small-label
      required
      class="margin-bottom-2"
      :error-message="
        $v.values.items_per_page.$dirty && !$v.values.items_per_page.required
          ? $t('error.requiredField')
          : !$v.values.items_per_page.integer
          ? $t('error.integerField')
          : !$v.values.items_per_page.minValue
          ? $t('error.minValueField', { min: 1 })
          : !$v.values.items_per_page.maxValue
          ? $t('error.maxValueField', { max: maxItemPerPage })
          : ''
      "
    >
      <FormInput
        v-model="values.items_per_page"
        :placeholder="$t('repeatElementForm.itemsPerPagePlaceholder')"
        :to-value="(value) => parseInt(value)"
        type="number"
        @blur="$v.values.items_per_page.$touch()"
      />
    </FormGroup>

    <CustomStyle
      v-show="values.data_source_id"
      v-model="values.styles"
      style-key="button"
      :config-block-types="['button']"
      :theme="builder.theme"
    />
    <FormGroup
      v-show="pagingOptionsAvailable"
      small-label
      :label="$t('repeatElementForm.buttonLoadMoreLabel')"
      class="margin-bottom-2"
      required
    >
      <InjectedFormulaInput
        v-model="values.button_load_more_label"
        :placeholder="$t('elementForms.textInputPlaceholder')"
      />
    </FormGroup>
    <FormGroup
      :label="$t('repeatElementForm.orientationLabel')"
      small-label
      required
      class="margin-bottom-2"
    >
      <RadioGroup
        v-model="values.orientation"
        :options="orientationOptions"
        type="button"
      >
      </RadioGroup>
    </FormGroup>
    <FormGroup
      v-show="values.orientation === 'horizontal'"
      :error-message="itemsPerRowError"
      :label="$t('repeatElementForm.itemsPerRowLabel')"
      small-label
      required
      :helper-text="$t('repeatElementForm.itemsPerRowDescription')"
    >
      <DeviceSelector
        :device-type-selected="deviceTypeSelected"
        class="repeat-element__device-selector margin-bottom-2"
        @selected="actionSetDeviceTypeSelected"
      >
        <template #deviceTypeControl="{ deviceType }">
          <FormInput
            :ref="`itemsPerRow-${deviceType.getType()}`"
            v-model="values.items_per_row[deviceType.getType()]"
            remove-number-input-controls
            type="number"
            @input="handlePerRowInput($event, deviceType.getType())"
          />
        </template>
      </DeviceSelector>
    </FormGroup>
    <FormGroup
      small-label
      class="margin-bottom-2"
      :label="$t('repeatElementForm.toggleEditorRepetitionsLabel')"
    >
      <Checkbox :checked="isCollapsed" @input="emitToggleRepetitions($event)">
      </Checkbox>
    </FormGroup>
  </form>
</template>

<script>
import _ from 'lodash'
import { required, integer, minValue, maxValue } from 'vuelidate/lib/validators'
import elementForm from '@baserow/modules/builder/mixins/elementForm'
import collectionElementForm from '@baserow/modules/builder/mixins/collectionElementForm'
import DeviceSelector from '@baserow/modules/builder/components/page/header/DeviceSelector.vue'
import { mapActions, mapGetters } from 'vuex'
import CustomStyle from '@baserow/modules/builder/components/elements/components/forms/style/CustomStyle'
import InjectedFormulaInput from '@baserow/modules/core/components/formula/InjectedFormulaInput'
import ServiceSchemaPropertySelector from '@baserow/modules/core/components/services/ServiceSchemaPropertySelector.vue'
import DataSourceDropdown from '@baserow/modules/builder/components/dataSource/DataSourceDropdown.vue'

export default {
  name: 'RepeatElementForm',
  components: {
    DataSourceDropdown,
    DeviceSelector,
    CustomStyle,
    InjectedFormulaInput,
    ServiceSchemaPropertySelector,
  },
  mixins: [elementForm, collectionElementForm],
  inject: ['applicationContext'],
  data() {
    return {
      allowedValues: [
        'data_source_id',
        'schema_property',
        'items_per_page',
        'items_per_row',
        'orientation',
        'button_load_more_label',
        'styles',
      ],
      values: {
        data_source_id: null,
        schema_property: null,
        items_per_page: 1,
        items_per_row: {},
        orientation: 'vertical',
        button_load_more_label: '',
        styles: {},
      },
    }
  },
  computed: {
    ...mapGetters({ deviceTypeSelected: 'page/getDeviceTypeSelected' }),
    isCollapsed() {
      const { element } = this.applicationContext
      return this.$store.getters['element/getRepeatElementCollapsed'](element)
    },
    deviceTypes() {
      return Object.values(this.$registry.getOrderedList('device'))
    },
    itemsPerRowError() {
      for (const device of this.deviceTypes) {
        const validation = this.$v.values.items_per_row[device.getType()]
        if (validation.$dirty) {
          if (!validation.integer) {
            return this.$t('error.integerField')
          }
          if (!validation.minValue) {
            return this.$t('error.minValueField', { min: 1 })
          }
          if (!validation.maxValue) {
            return this.$t('error.maxValueField', { max: 10 })
          }
        }
      }
      return ''
    },
    orientationOptions() {
      return [
        {
          label: this.$t('repeatElementForm.orientationVertical'),
          value: 'vertical',
          icon: 'iconoir-table-rows',
        },
        {
          label: this.$t('repeatElementForm.orientationHorizontal'),
          value: 'horizontal',
          icon: 'iconoir-view-columns-3',
        },
      ]
    },
  },
  mounted() {
    if (_.isEmpty(this.values.items_per_row)) {
      this.values.items_per_row = this.deviceTypes.reduce((acc, deviceType) => {
        acc[deviceType.getType()] = 2
        return acc
      }, {})
    }
  },
  methods: {
    ...mapActions({
      actionSetDeviceTypeSelected: 'page/setDeviceTypeSelected',
    }),
    emitToggleRepetitions(value) {
      const { element } = this.applicationContext
      this.$store.dispatch('element/setRepeatElementCollapsed', {
        element,
        collapsed: value,
      })
    },
    handlePerRowInput(event, deviceTypeType) {
      this.$v.values.items_per_row[deviceTypeType].$touch()
      this.values.items_per_row[deviceTypeType] = parseInt(event)
      this.$emit('input', this.values)
    },
  },
  validations() {
    const itemsPerPageRules = { integer }
    if (this.pagingOptionsAvailable) {
      itemsPerPageRules.required = required
      itemsPerPageRules.minValue = minValue(1)
      itemsPerPageRules.maxValue = maxValue(this.maxItemPerPage)
    }
    return {
      values: {
        items_per_page: itemsPerPageRules,
        items_per_row: this.deviceTypes.reduce((acc, deviceType) => {
          acc[deviceType.getType()] = {
            integer,
            minValue: minValue(1),
            maxValue: maxValue(10),
          }
          return acc
        }, {}),
      },
    }
  },
}
</script>
