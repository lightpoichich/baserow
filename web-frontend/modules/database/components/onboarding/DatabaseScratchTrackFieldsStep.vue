<template>
  <div>
    <h1>{{ $t('databaseScratchTrackFieldsStep.title') }}</h1>
    <p>
      {{
        $t('databaseScratchTrackFieldsStep.description', {
          selectedFieldsLimitCount,
        })
      }}
    </p>
    <div class="flex flex-wrap margin-bottom-3" style="--gap: 8px">
      <Chips
        v-for="(whatItem, whatKey) in whatItems"
        :key="whatKey"
        :active="Object.keys(selectedFields).includes(whatKey)"
        :disabled="isChipDisabled(whatKey)"
        :icon="whatItem.icon"
        @click="toggleSelection(whatKey)"
        >{{ whatItem.props.name }}
      </Chips>
      <Chips
        icon="iconoir-plus"
        :disabled="isChipDisabled('own')"
        :active="addOwnField === true"
        @click="handleAddOwnField"
      >
        {{ $t('databaseScratchTrackStep.addYourOwn') }}
      </Chips>
    </div>

    <FormGroup
      v-if="addOwnField"
      :label="$t('databaseScratchTrackStep.tableName')"
      required
      small-label
      class="margin-bottom-2"
    >
      <Dropdown v-model="ownField" :show-search="false">
        <DropdownItem
          v-for="field in ownFieldsDefinitions"
          :key="field.props.type"
          :name="field.name"
          :value="field"
          :icon="field.icon"
        >
        </DropdownItem>
      </Dropdown>
      <FormInput
        v-model="ownField.props.name"
        :placeholder="$t('databaseScratchTrackStepFields.fieldName')"
        size="large"
      />
      <template #error>{{ $t('error.requiredField') }}</template>
    </FormGroup>
  </div>
</template>

<script>
import DatabaseScratchTrackFieldsStepDataMixin from '@baserow/modules/database/components/onboarding/DatabaseScratchTrackFieldsStepDataMixin'

export default {
  name: 'DatabaseScratchTrackFieldsStep',
  mixins: [DatabaseScratchTrackFieldsStepDataMixin],
  props: {
    data: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      addOwnField: false,
      // Move this to mounted and fill with previous step choice
      what: 'projects',
      selectedFieldsLimitCount: 4,
      selectedFieldsCount: 0,
      selectedFields: {},
      ownField: {
        props: {
          name: '',
        },
      },
    }
  },
  computed: {
    canSkip() {
      // TODO: This doesn't work in this step
      return true
    },
    whatItems() {
      let fields
      switch (this.what) {
        case 'projects':
          fields = this.projectsFields
          break
        case 'teams':
          fields = this.teamsFields
          break
        case 'tasks':
          fields = this.tasksFields
          break
        case 'campaigns':
          fields = this.campaignsFields
          break
      }
      return fields
    },
  },
  watch: {
    ownField: {
      handler(field) {
        this.selectedFields.own = field
        this.updateValue()
      },
      deep: true,
    },
  },
  mounted() {
    ;(this.what = this.data.database_scratch_track.tableName.toLowerCase()),
      this.updateValue()
  },
  methods: {
    isChipDisabled(name) {
      return (
        this.selectedFieldsCount >= this.selectedFieldsLimitCount &&
        !Object.keys(this.selectedFields).includes(name)
      )
    },
    isValid() {
      return !this.$v.$invalid
    },
    handleAddOwnField() {
      if (!this.addOwnField) {
        this.ownField = this.ownFieldsDefinitions[0]
      }

      this.addOwnField = !this.addOwnField
      this.toggleSelection('own')
      this.updateValue()
    },
    toggleSelection(value) {
      const isAlreadySelected = Object.keys(this.selectedFields).includes(value)
      if (
        this.selectedFieldsCount >= this.selectedFieldsLimitCount &&
        !isAlreadySelected
      ) {
        return
      }

      if (isAlreadySelected) {
        this.selectedFieldsCount--
        delete this.selectedFields[value]
      } else {
        this.selectedFieldsCount++
        if (value !== 'own') {
          this.selectedFields[value] = this.whatItems[value]
        }
      }
      this.updateValue()
    },
    updateValue() {
      const fields = this.selectedFields
      this.$emit('update-data', { fields })
    },
  },
  validations() {
    return {}
  },
}
</script>
