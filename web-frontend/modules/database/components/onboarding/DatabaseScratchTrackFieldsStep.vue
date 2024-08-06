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
        v-for="(whatItem, whatKey) in whatItems.fields"
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
          :name="field.props.name"
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
import moment from '@baserow/modules/core/moment'

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
      }
      return fields
    },

    ownFieldsDefinitions() {
      // TODO: Move this to a separate file and import as mixin
      // TODO: Consider using components for field type to get i.e. icon
      return [
        {
          props: {
            name: this.$t(
              'databaseScratchTrackFieldsStep.ownFields.description'
            ),
            type: 'long_text',
          },
          icon: 'iconoir-align-left',
          rows: ['row #1', 'row #2', 'row #3'],
        },
        {
          props: {
            name: this.$t('databaseScratchTrackFieldsStep.ownFields.number'),
            type: 'number',
          },
          icon: 'baserow-icon-hashtag',
          rows: [0, -500, 131.35],
        },
        {
          props: {
            name: this.$t('databaseScratchTrackFieldsStep.ownFields.date'),
            type: 'date',
            date_format: 'ISO',
          },
          icon: 'iconoir-calendar',
          rows: [
            moment().subtract(3, 'months').format('YYYY-MM-DD'),
            moment().add(1, 'days').format('YYYY-MM-DD'),
            moment().add(1, 'months').format('YYYY-MM-DD'),
          ],
        },
        {
          props: {
            name: this.$t('databaseScratchTrackFieldsStep.ownFields.boolean'),
            type: 'boolean',
          },
          icon: 'baserow-icon-circle-checked',
          rows: [true, false, true],
        },
        {
          props: {
            name: this.$t('databaseScratchTrackFieldsStep.ownFields.duration'),
            type: 'duration',
          },
          icon: 'iconoir-clock-rotate-right',
          rows: ['row #1', 'row #2', 'row #3'],
        },
        {
          props: {
            name: this.$t('databaseScratchTrackFieldsStep.ownFields.url'),
            type: 'url',
          },
          icon: 'iconoir-link',
          rows: [
            'https://baserow.io',
            'https://example.com',
            'https://gitlab.com/baserow',
          ],
        },
        {
          props: {
            name: this.$t('databaseScratchTrackFieldsStep.ownFields.email'),
            type: 'email',
          },
          icon: 'iconoir-mail',
          rows: ['user1@baserow.io', 'user2@baserow.io', 'user3.baserow.io'],
        },
        {
          props: {
            name: this.$t('databaseScratchTrackFieldsStep.ownFields.rating'),
            type: 'rating',
          },
          icon: 'iconoir-star',
          rows: [3, 1, 5],
        },
      ]
    },

    projectsFields() {
      return {
        name: this.$t('databaseScratchTrackFieldsStep.projects.fields.name'),
        fields: {
          category: {
            props: {
              name: this.$t(
                'databaseScratchTrackFieldsStep.projects.fields.category'
              ),
              type: 'single_select',
            },
            icon: 'baserow-icon-single-select',
            rows: [
              this.$t(
                'databaseScratchTrackFieldsStep.projects.categories.design'
              ),
              this.$t(
                'databaseScratchTrackFieldsStep.projects.categories.development'
              ),
              this.$t(
                'databaseScratchTrackFieldsStep.projects.categories.marketing'
              ),
            ],
          },
          kickoffDate: {
            props: {
              name: this.$t(
                'databaseScratchTrackFieldsStep.projects.fields.kickoffDate'
              ),
              type: 'date',
              date_format: 'ISO',
            },
            icon: 'iconoir-calendar',
            rows: [
              moment().subtract(1, 'months').format('YYYY-MM-DD'),
              moment().add(1, 'weeks').format('YYYY-MM-DD'),
              moment().add(1, 'months').format('YYYY-MM-DD'),
            ],
          },
          dueDate: {
            props: {
              name: this.$t(
                'databaseScratchTrackFieldsStep.projects.fields.dueDate'
              ),
              type: 'date',
              date_format: 'ISO',
            },
            icon: 'iconoir-calendar',
            rows: [
              moment().subtract(1, 'months').format('YYYY-MM-DD'),
              moment().add(1, 'days').format('YYYY-MM-DD'),
              moment().add(3, 'weeks').format('YYYY-MM-DD'),
            ],
          },
          budget: {
            props: {
              name: this.$t(
                'databaseScratchTrackFieldsStep.projects.fields.budget'
              ),
              type: 'number',
            },
            icon: 'baserow-icon-hashtag',
            rows: [500, 1000, 3000],
          },
          completed: {
            props: {
              name: this.$t(
                'databaseScratchTrackFieldsStep.projects.fields.completed'
              ),
              type: 'boolean',
            },
            icon: 'baserow-icon-circle-checked',
            rows: [true, false, false],
          },
          notes: {
            props: {
              name: this.$t(
                'databaseScratchTrackFieldsStep.projects.fields.notes'
              ),
              type: 'long_text',
            },
            icon: 'iconoir-align-left',
            rows: [
              this.$t(
                'databaseScratchTrackFieldsStep.projects.rows.row1.notes'
              ),
              this.$t(
                'databaseScratchTrackFieldsStep.projects.rows.row2.notes'
              ),
              this.$t(
                'databaseScratchTrackFieldsStep.projects.rows.row3.notes'
              ),
            ],
          },
        },
      }
    },

    // TOD: Update rest of fields when structure is finalized
    teamsFields() {
      return {}
    },
    tasksFields() {
      return {}
    },
    campaignsFields() {
      return {}
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
        if (value === 'own') {
          this.selectedFields[value] = {
            props: {
              name: this.$t(
                'databaseScratchTrackFieldsStep.ownFields.description'
              ),
              type: 'long_text',
            },
            icon: 'iconoir-plus',
            rows: ['row #1', 'row #2', 'row #3'],
          }
        } else {
          this.selectedFields[value] = this.whatItems.fields[value]
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
