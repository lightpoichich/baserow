<template>
  <form @submit.prevent @keydown.enter.prevent>
    <CustomStyle
      v-model="values.styles"
      style-key="input"
      :config-block-types="['input']"
      :theme="builder.theme"
    />
    <FormGroup
      class="margin-bottom-2"
      small-label
      required
      :label="$t('recordSelectorElementForm.selectRecordsFrom')"
    >
      <DataSourceDropdown
        v-model="values.data_source_id"
        small
        :data-sources="listDataSources"
        :page="page"
      >
        <template #chooseValueState>
          {{ $t('recordSelectorElementForm.noDataSourceMessage') }}
        </template>
      </DataSourceDropdown>
    </FormGroup>
    <FormGroup
      class="margin-bottom-2"
      small-label
      :label="$t('recordSelectorElementForm.itemsPerPage')"
      :error-message="
        $v.values.items_per_page.$dirty && !$v.values.items_per_page.required
          ? $t('error.requiredField')
          : !$v.values.items_per_page.integer
          ? $t('error.integerField')
          : !$v.values.items_per_page.minValue
          ? $t('error.minValueField', { min: 5 })
          : !$v.values.items_per_page.maxValue
          ? $t('error.maxValueField', { max: maxItemPerPage })
          : ''
      "
    >
      <FormInput
        v-model="values.items_per_page"
        type="number"
        :to-value="(value) => parseInt(value)"
        :placeholder="$t('recordSelectorElementForm.itemsPerPagePlaceholder')"
        @blur="$v.values.items_per_page.$touch()"
      />
    </FormGroup>
    <!--
    We use a key here otherwise Vuejs reuse the components of the following
    formula input with the old application context when the v-if becomes true.
    Therefore the "allowSameElement" value is wrong showing invalid formula when they
    are valid. We could also solve this by using a v-show instead of a v-if.
    -->
    <FormGroup
      v-if="values.data_source_id"
      key="optionNameSuffix"
      class="margin-bottom-2"
      small-label
      :label="$t('recordSelectorElementForm.optionNameSuffix')"
      :helper-text="$t('recordSelectorElementForm.optionNameSuffixHelper')"
      required
    >
      <InjectedFormulaInput
        v-model="values.option_name_suffix"
        :placeholder="
          $t('recordSelectorElementForm.optionNameSuffixPlaceholder')
        "
        :application-context-additions="{
          allowSameElement: true,
        }"
      />
    </FormGroup>
    <FormGroup
      small-label
      class="margin-bottom-2"
      :label="$t('generalForm.labelTitle')"
      required
    >
      <InjectedFormulaInput
        v-model="values.label"
        :placeholder="$t('generalForm.labelPlaceholder')"
      />
    </FormGroup>
    <FormGroup
      v-if="values.data_source_id"
      small-label
      class="margin-bottom-2"
      :label="$t('generalForm.valueTitle')"
      required
    >
      <InjectedFormulaInput
        v-model="values.default_value"
        :placeholder="$t('generalForm.valuePlaceholder')"
      />
    </FormGroup>
    <FormGroup
      small-label
      class="margin-bottom-2"
      :label="$t('generalForm.placeholderTitle')"
      required
    >
      <InjectedFormulaInput
        v-model="values.placeholder"
        :placeholder="$t('generalForm.placeholderPlaceholder')"
      />
    </FormGroup>
    <FormGroup
      small-label
      class="margin-bottom-2"
      required
      :label="$t('recordSelectorElementForm.multipleLabel')"
    >
      <Checkbox v-model="values.multiple"></Checkbox>
    </FormGroup>
    <FormGroup
      small-label
      class="margin-bottom-2"
      required
      :label="$t('generalForm.requiredTitle')"
    >
      <Checkbox v-model="values.required"></Checkbox>
    </FormGroup>
  </form>
</template>

<script>
import collectionElementForm from '@baserow/modules/builder/mixins/collectionElementForm'
import InjectedFormulaInput from '@baserow/modules/core/components/formula/InjectedFormulaInput.vue'
import formElementForm from '@baserow/modules/builder/mixins/formElementForm'
import CustomStyle from '@baserow/modules/builder/components/elements/components/forms/style/CustomStyle.vue'
import { integer, maxValue, minValue, required } from 'vuelidate/lib/validators'
import DataSourceDropdown from '@baserow/modules/builder/components/dataSource/DataSourceDropdown.vue'

export default {
  name: 'RecordSelectorElementForm',
  components: { DataSourceDropdown, CustomStyle, InjectedFormulaInput },
  mixins: [formElementForm, collectionElementForm],
  data() {
    return {
      allowedValues: [
        'required',
        'data_source_id',
        'items_per_page',
        'label',
        'default_value',
        'placeholder',
        'multiple',
        'option_name_suffix',
        'styles',
      ],
      values: {
        required: false,
        data_source_id: null,
        items_per_page: null,
        label: '',
        default_value: '',
        placeholder: '',
        multiple: false,
        option_name_suffix: '',
        styles: {},
      },
    }
  },
  computed: {
    // For now, RecordSelector only supports data sources that return arrays
    listDataSources() {
      return this.dataSources.filter(
        (dataSource) =>
          dataSource.type &&
          this.$registry.get('service', dataSource.type).returnsList
      )
    },
  },
  validations() {
    return {
      values: {
        items_per_page: {
          required,
          integer,
          // We need at least 5 items to trigger the
          // infinite scroll
          minValue: minValue(5),
          maxValue: maxValue(this.maxItemPerPage),
        },
      },
    }
  },
  watch: {
    'values.data_source_id': {
      handler(value) {
        this.values.data_source_id = value

        // If the data source was removed we should also delete the name formula
        if (value === null) {
          this.values.option_name_suffix = ''
        }
      },
      immediate: true,
    },
  },
}
</script>
