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
        :active="isChipActive(whatKey)"
        :disabled="isChipDisabled(whatKey)"
        :icon="whatItem.icon"
        @click="toggleSelection(whatKey)"
        >{{ whatItem.props.name }}
      </Chips>
      <Chips
        icon="iconoir-plus"
        :disabled="isChipDisabled('own')"
        :active="isChipActive('own')"
        @click="toggleSelection('own')"
      >
        {{ $t('databaseScratchTrackStep.addYourOwn') }}
      </Chips>
    </div>

    <FormGroup
      v-if="isChipActive('own')"
      required
      small-label
      class="margin-bottom-2 onboarding__form-group"
    >
      <div class="onboarding__form-group-row">
        <div class="onboarding__form-group-column">
          <div class="onboarding__form-group-label">
            {{ $t('databaseScratchTrackFieldsStep.fieldType') }}
          </div>
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
        </div>
        <div class="onboarding__form-group-column">
          <div class="onboarding__form-group-label">
            {{ $t('databaseScratchTrackFieldsStep.fieldName') }}
          </div>
          <FormInput
            v-model="ownField.props.name"
            :placeholder="$t('databaseScratchTrackFieldsStep.fieldName')"
            size="large"
            :error="
              $v.ownField.props.name.$dirty && $v.ownField.props.name.$invalid
            "
            @blur="$v.ownField.props.name.$touch()"
          />
        </div>
      </div>
      <template #error>{{ $t('error.requiredField') }}</template>
    </FormGroup>
  </div>
</template>

<script>
import DatabaseScratchTrackFieldsStepDataMixin from '@baserow/modules/database/components/onboarding/DatabaseScratchTrackFieldsStepDataMixin'
import { required } from 'vuelidate/lib/validators'

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
      what: '',
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
      console.log('CALLED SKIP ON FIELDS')
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
        default:
          fields = this.customFields
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
    this.what = this.data.database_scratch_track.tableName.toLowerCase()
    this.updateValue()
  },
  methods: {
    isChipDisabled(name) {
      return (
        this.selectedFieldsCount >= this.selectedFieldsLimitCount &&
        !Object.keys(this.selectedFields).includes(name)
      )
    },
    isChipActive(name) {
      return Object.keys(this.selectedFields).includes(name)
    },
    isValid() {
      return !this.$v.$invalid
    },
    toggleSelection(value) {
      const isAlreadySelected = this.isChipActive(value)
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
        if (value === 'own') {
          // preselect first field if nothing was selected
          if (!this.ownField.props.name) {
            this.ownField = this.ownFieldsDefinitions[0]
          }
          this.selectedFields.own = this.ownField
        } else {
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
  validations: {
    ownField: {
      props: {
        name: { required },
      },
    },
  },
}
</script>
