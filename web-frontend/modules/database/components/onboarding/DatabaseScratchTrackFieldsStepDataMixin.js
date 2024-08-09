import moment from '@baserow/modules/core/moment'
import {
  BooleanFieldType,
  DateFieldType,
  DurationFieldType,
  EmailFieldType,
  LongTextFieldType,
  NumberFieldType,
  PhoneNumberFieldType,
  RatingFieldType,
  SingleSelectFieldType,
  URLFieldType,
} from '@baserow/modules/database/fieldTypes'

export default {
  data() {
    return {
      icons: {
        [LongTextFieldType.getType()]: new LongTextFieldType().iconClass,
        [NumberFieldType.getType()]: new NumberFieldType().iconClass,
        [DateFieldType.getType()]: new DateFieldType().iconClass,
        [BooleanFieldType.getType()]: new BooleanFieldType().iconClass,
        [DurationFieldType.getType()]: new DurationFieldType().iconClass,
        [URLFieldType.getType()]: new URLFieldType().iconClass,
        [EmailFieldType.getType()]: new EmailFieldType().iconClass,
        [RatingFieldType.getType()]: new RatingFieldType().iconClass,
        [SingleSelectFieldType.getType()]: new SingleSelectFieldType()
          .iconClass,
        [PhoneNumberFieldType.getType()]: new PhoneNumberFieldType().iconClass,
      },
    }
  },

  computed: {
    ownFieldsDefinitions() {
      return [
        {
          name: this.$t('databaseScratchTrackFieldsStep.fields.description'),
          props: {
            name: this.$t('databaseScratchTrackFieldsStep.fields.description'),
            type: LongTextFieldType.getType(),
          },
          icon: this.icons[LongTextFieldType.getType()],
          rows: [
            this.$t(
              'databaseScratchTrackFieldsStep.customFields.row1.description'
            ),
            this.$t(
              'databaseScratchTrackFieldsStep.customFields.row2.description'
            ),
            this.$t(
              'databaseScratchTrackFieldsStep.customFields.row3.description'
            ),
          ],
        },
        {
          name: this.$t('databaseScratchTrackFieldsStep.fields.number'),
          props: {
            name: this.$t('databaseScratchTrackFieldsStep.fields.number'),
            type: NumberFieldType.getType(),
          },
          icon: this.icons[NumberFieldType.getType()],
          rows: [0, -500, 131.35],
        },
        {
          name: this.$t('databaseScratchTrackFieldsStep.fields.date'),
          props: {
            name: this.$t('databaseScratchTrackFieldsStep.fields.date'),
            type: DateFieldType.getType(),
            date_format: 'ISO',
          },
          icon: this.icons[DateFieldType.getType()],
          rows: [
            moment().subtract(3, 'months').format('YYYY-MM-DD'),
            moment().add(1, 'days').format('YYYY-MM-DD'),
            moment().add(1, 'months').format('YYYY-MM-DD'),
          ],
        },
        {
          name: this.$t('databaseScratchTrackFieldsStep.fields.boolean'),
          props: {
            name: this.$t('databaseScratchTrackFieldsStep.fields.boolean'),
            type: BooleanFieldType.getType(),
          },
          icon: this.icons[BooleanFieldType.getType()],
          rows: [true, false, true],
        },
        {
          name: this.$t('databaseScratchTrackFieldsStep.fields.duration'),
          props: {
            name: this.$t('databaseScratchTrackFieldsStep.fields.duration'),
            type: DurationFieldType.getType(),
            duration_format: 'h:mm:ss',
          },
          icon: this.icons[DurationFieldType.getType()],
          rows: [100, 1000, 10000],
        },
        {
          name: this.$t('databaseScratchTrackFieldsStep.fields.url'),
          props: {
            name: this.$t('databaseScratchTrackFieldsStep.fields.url'),
            type: URLFieldType.getType(),
          },
          icon: this.icons[URLFieldType.getType()],
          rows: [
            'https://baserow.io',
            'https://example.com',
            'https://gitlab.com/baserow',
          ],
        },
        {
          name: this.$t('databaseScratchTrackFieldsStep.fields.email'),
          props: {
            name: this.$t('databaseScratchTrackFieldsStep.fields.email'),
            type: EmailFieldType.getType(),
          },
          icon: this.icons[EmailFieldType.getType()],
          rows: [
            'donnmoore@company.com',
            'gordonb@company.com',
            'janetcook@company.com',
          ],
        },
        {
          name: this.$t('databaseScratchTrackFieldsStep.fields.rating'),
          props: {
            name: this.$t('databaseScratchTrackFieldsStep.fields.rating'),
            type: RatingFieldType.getType(),
          },
          icon: this.icons[RatingFieldType.getType()],
          rows: [3, 1, 5],
        },
      ]
    },

    projectsFields() {
      const selectOptions = [
        {
          id: -1,
          value: this.$t(
            'databaseScratchTrackFieldsStep.projects.categories.design'
          ),
          color: 'gray',
        },
        {
          id: -2,
          value: this.$t(
            'databaseScratchTrackFieldsStep.projects.categories.development'
          ),
          color: 'yellow',
        },
        {
          id: -3,
          value: this.$t(
            'databaseScratchTrackFieldsStep.projects.categories.marketing'
          ),
          color: 'blue',
        },
      ]

      return {
        category: {
          props: {
            name: this.$t('databaseScratchTrackFieldsStep.fields.category'),
            type: SingleSelectFieldType.getType(),
            select_options: selectOptions,
          },
          icon: this.icons[SingleSelectFieldType.getType()],
          rows: selectOptions,
        },
        kickoffDate: {
          props: {
            name: this.$t('databaseScratchTrackFieldsStep.fields.kickoffDate'),
            type: DateFieldType.getType(),
            date_format: 'ISO',
          },
          icon: this.icons[DateFieldType.getType()],
          rows: [
            moment().subtract(1, 'months').format('YYYY-MM-DD'),
            moment().add(1, 'weeks').format('YYYY-MM-DD'),
            moment().add(1, 'months').format('YYYY-MM-DD'),
          ],
        },
        dueDate: {
          props: {
            name: this.$t('databaseScratchTrackFieldsStep.fields.dueDate'),
            type: DateFieldType.getType(),
            date_format: 'ISO',
          },
          icon: this.icons[DateFieldType.getType()],
          rows: [
            moment().subtract(1, 'months').format('YYYY-MM-DD'),
            moment().add(1, 'days').format('YYYY-MM-DD'),
            moment().add(3, 'weeks').format('YYYY-MM-DD'),
          ],
        },
        budget: {
          props: {
            name: this.$t('databaseScratchTrackFieldsStep.fields.budget'),
            type: NumberFieldType.getType(),
          },
          icon: this.icons[NumberFieldType.getType()],
          rows: [500, 1000, 3000],
        },
        completed: {
          props: {
            name: this.$t('databaseScratchTrackFieldsStep.fields.completed'),
            type: BooleanFieldType.getType(),
          },
          icon: this.icons[BooleanFieldType.getType()],
          rows: [true, false, false],
        },
        notes: {
          props: {
            name: this.$t('databaseScratchTrackFieldsStep.fields.notes'),
            type: LongTextFieldType.getType(),
          },
          icon: this.icons[LongTextFieldType.getType()],
          rows: [
            this.$t('databaseScratchTrackFieldsStep.projects.row1.notes'),
            this.$t('databaseScratchTrackFieldsStep.projects.row2.notes'),
            this.$t('databaseScratchTrackFieldsStep.projects.row3.notes'),
          ],
        },
      }
    },

    teamsFields() {
      const selectOptions = [
        {
          id: 1,
          value: this.$t('databaseScratchTrackFieldsStep.teams.roles.designer'),
          color: 'gray',
        },
        {
          id: 2,
          value: this.$t(
            'databaseScratchTrackFieldsStep.teams.roles.developer'
          ),
          color: 'yellow',
        },
        {
          id: 3,
          value: this.$t('databaseScratchTrackFieldsStep.teams.roles.marketer'),
          color: 'blue',
        },
      ]
      return {
        role: {
          props: {
            name: this.$t('databaseScratchTrackFieldsStep.fields.role'),
            type: SingleSelectFieldType.getType(),
            select_options: selectOptions,
          },
          icon: this.icons[SingleSelectFieldType.getType()],
          rows: selectOptions,
        },
        phone: {
          props: {
            name: this.$t('databaseScratchTrackFieldsStep.fields.phone'),
            type: PhoneNumberFieldType.getType(),
          },
          icon: this.icons[SingleSelectFieldType.getType()],
          rows: ['(508) 398-0845', '(803) 996-6704', '(269) 445-2068'],
        },
        email: {
          props: {
            name: this.$t('databaseScratchTrackFieldsStep.fields.email'),
            type: EmailFieldType.getType(),
          },
          icon: this.icons[EmailFieldType.getType()],
          rows: [
            'donnmoore@company.com',
            'gordonb@company.com',
            'janetcook@company.com',
          ],
        },
        active: {
          props: {
            name: this.$t('databaseScratchTrackFieldsStep.fields.active'),
            type: BooleanFieldType.getType(),
          },
          icon: this.icons[BooleanFieldType.getType()],
          rows: [true, false, true],
        },
      }
    },

    tasksFields() {
      return {
        estimatedDays: {
          props: {
            name: this.$t(
              'databaseScratchTrackFieldsStep.fields.estimatedDays'
            ),
            type: NumberFieldType.getType(),
          },
          icon: this.icons[NumberFieldType.getType()],
          rows: [2, 7, 13],
        },
        completed: {
          props: {
            name: this.$t('databaseScratchTrackFieldsStep.fields.completed'),
            type: BooleanFieldType.getType(),
          },
          icon: this.icons[BooleanFieldType.getType()],
          rows: [true, false, false],
        },
        description: {
          props: {
            name: this.$t('databaseScratchTrackFieldsStep.fields.description'),
            type: LongTextFieldType.getType(),
          },
          icon: this.icons[LongTextFieldType.getType()],
          rows: [
            this.$t('databaseScratchTrackFieldsStep.tasks.row1.description'),
            this.$t('databaseScratchTrackFieldsStep.tasks.row2.description'),
            this.$t('databaseScratchTrackFieldsStep.tasks.row3.description'),
          ],
        },
      }
    },

    campaignsFields() {
      return {
        description: {
          props: {
            name: this.$t('databaseScratchTrackFieldsStep.fields.description'),
            type: LongTextFieldType.getType(),
          },
          icon: this.icons[LongTextFieldType.getType()],
          rows: [
            this.$t(
              'databaseScratchTrackFieldsStep.campaigns.row1.description'
            ),
            this.$t(
              'databaseScratchTrackFieldsStep.campaigns.row2.description'
            ),
            this.$t(
              'databaseScratchTrackFieldsStep.campaigns.row3.description'
            ),
          ],
        },
        startDate: {
          props: {
            name: this.$t('databaseScratchTrackFieldsStep.fields.startDate'),
            type: DateFieldType.getType(),
            date_format: 'ISO',
          },
          icon: this.icons[DateFieldType.getType()],
          rows: [
            moment().subtract(1, 'months').format('YYYY-MM-DD'),
            moment().add(1, 'weeks').format('YYYY-MM-DD'),
            moment().add(1, 'months').format('YYYY-MM-DD'),
          ],
        },
        endDate: {
          props: {
            name: this.$t('databaseScratchTrackFieldsStep.fields.endDate'),
            type: DateFieldType.getType(),
            date_format: 'ISO',
          },
          icon: this.icons[DateFieldType.getType()],
          rows: [
            moment().subtract(1, 'months').format('YYYY-MM-DD'),
            moment().add(1, 'days').format('YYYY-MM-DD'),
            moment().add(3, 'weeks').format('YYYY-MM-DD'),
          ],
        },
        budget: {
          props: {
            name: this.$t('databaseScratchTrackFieldsStep.fields.budget'),
            type: NumberFieldType.getType(),
          },
          icon: this.icons[NumberFieldType.getType()],
          rows: [12000, 30000, 2000],
        },
      }
    },

    customFields() {
      return {
        date: {
          props: {
            name: this.$t('databaseScratchTrackFieldsStep.fields.date'),
            type: DateFieldType.getType(),
            date_format: 'ISO',
          },
          icon: this.icons[DateFieldType.getType()],
          rows: [
            moment().subtract(1, 'months').format('YYYY-MM-DD'),
            moment().add(1, 'weeks').format('YYYY-MM-DD'),
            moment().add(1, 'months').format('YYYY-MM-DD'),
          ],
        },
        number: {
          props: {
            name: this.$t('databaseScratchTrackFieldsStep.fields.number'),
            type: NumberFieldType.getType(),
          },
          icon: this.icons[NumberFieldType.getType()],
          rows: [500, -1000, 3000],
        },
        completed: {
          props: {
            name: this.$t('databaseScratchTrackFieldsStep.fields.completed'),
            type: BooleanFieldType.getType(),
          },
          icon: this.icons[BooleanFieldType.getType()],
          rows: [true, false, false],
        },
        description: {
          props: {
            name: this.$t('databaseScratchTrackFieldsStep.fields.description'),
            type: LongTextFieldType.getType(),
          },
          icon: this.icons[LongTextFieldType.getType()],
          rows: [
            this.$t(
              'databaseScratchTrackFieldsStep.customFields.row1.description'
            ),
            this.$t(
              'databaseScratchTrackFieldsStep.customFields.row2.description'
            ),
            this.$t(
              'databaseScratchTrackFieldsStep.customFields.row3.description'
            ),
          ],
        },
      }
    },
  },
}
