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
              v-for="field in ownFields"
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
          <p
            v-if="
              $v.ownField.props.name.$dirty && $v.ownField.props.name.$invalid
            "
            class="control__messages--error"
          >
            <template v-if="!$v.ownField.props.name.required">
              {{ $t('error.requiredField') }}
            </template>
            <template v-if="!$v.ownField.props.name.uniqueNameValidator">
              {{ $t('error.alreadyInUse') }}
            </template>
          </p>
        </div>
      </div>
    </FormGroup>
  </div>
</template>

<script>
import { requiredIf } from 'vuelidate/lib/validators'
import { DatabaseScratchTrackOnboardingType } from '@baserow/modules/database/onboardingTypes'

export default {
  name: 'DatabaseScratchTrackFieldsStep',
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
      isOwnFieldValidationEnabled: false,
      whatItems: [],
      ownFields: [],
    }
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
    this.what =
      this.data[
        DatabaseScratchTrackOnboardingType.getType()
      ].tableName.toLowerCase()
    let onboardingTrackFieldsType

    try {
      onboardingTrackFieldsType = this.$registry.get(
        'onboardingTrackFields',
        `database_scratch_track_fields_${this.what}`
      )
    } catch {
      onboardingTrackFieldsType = this.$registry.get(
        'onboardingTrackFields',
        `database_scratch_track_fields_custom`
      )
    }
    this.whatItems = onboardingTrackFieldsType.getFields()
    this.ownFields = onboardingTrackFieldsType.getOwnFields()
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
      const isActive = Object.keys(this.selectedFields).includes(name)
      if (name === 'own') {
        this.isOwnFieldValidationEnabled = isActive
      }
      return isActive
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
            this.ownField = this.ownFields[0]
          }
          this.selectedFields.own = this.ownField
        } else {
          this.selectedFields[value] = this.whatItems[value]
          this.$v.ownField.props.name.$touch()
        }
      }
      this.updateValue()
    },
    updateValue() {
      const fields = this.selectedFields
      this.$emit('update-data', { fields })
    },
    getSelectedFieldNames() {
      return Object.entries(this.selectedFields)
        .filter(([key, value]) => key !== 'own')
        .map(([key, value]) => value.name)
    },
  },
  validations() {
    return {
      ownField: {
        props: {
          name: {
            required: requiredIf(() => this.isOwnFieldValidationEnabled),
            // TODO: needs to be also triggered when predefined fields
            // are selected (i.e. change name to "Notes" then selecting
            // "Notes" field should trigger error here
            uniqueNameValidator: (value) => {
              const selectedFieldNames = this.getSelectedFieldNames()
              return selectedFieldNames && !selectedFieldNames.includes(value)
            },
          },
        },
      },
    }
  },
}
</script>
