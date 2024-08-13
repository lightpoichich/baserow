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
import { Registerable } from '@baserow/modules/core/registry'

export const fieldHandlerRegistry = {
  [SingleSelectFieldType.getType()]: function (field, response) {
    return response.data.select_options.map((option) => option.id)
  },
}

export class DatabaseScratchTrackFieldsOnboardingType extends Registerable {
  getIcons() {
    return {
      [LongTextFieldType.getType()]: new LongTextFieldType().iconClass,
      [NumberFieldType.getType()]: new NumberFieldType().iconClass,
      [DateFieldType.getType()]: new DateFieldType().iconClass,
      [BooleanFieldType.getType()]: new BooleanFieldType().iconClass,
      [DurationFieldType.getType()]: new DurationFieldType().iconClass,
      [URLFieldType.getType()]: new URLFieldType().iconClass,
      [EmailFieldType.getType()]: new EmailFieldType().iconClass,
      [RatingFieldType.getType()]: new RatingFieldType().iconClass,
      [SingleSelectFieldType.getType()]: new SingleSelectFieldType().iconClass,
      [PhoneNumberFieldType.getType()]: new PhoneNumberFieldType().iconClass,
    }
  }

  static getType() {
    return 'database_scratch_track'
  }

  getOwnFields() {
    const icons = this.getIcons()
    return [
      {
        name: this.$t('databaseScratchTrackFieldsStep.fields.description'),
        props: {
          name: this.$t('databaseScratchTrackFieldsStep.fields.description'),
          type: LongTextFieldType.getType(),
        },
        icon: icons[LongTextFieldType.getType()],
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
          number_decimal_places: 2,
          number_negative: true,
        },
        icon: icons[NumberFieldType.getType()],
        rows: [0, -500, 131.35],
      },
      {
        name: this.$t('databaseScratchTrackFieldsStep.fields.date'),
        props: {
          name: this.$t('databaseScratchTrackFieldsStep.fields.date'),
          type: DateFieldType.getType(),
          date_format: 'ISO',
        },
        icon: icons[DateFieldType.getType()],
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
        icon: icons[BooleanFieldType.getType()],
        rows: [true, false, true],
      },
      {
        name: this.$t('databaseScratchTrackFieldsStep.fields.duration'),
        props: {
          name: this.$t('databaseScratchTrackFieldsStep.fields.duration'),
          type: DurationFieldType.getType(),
          duration_format: 'h:mm:ss',
        },
        icon: icons[DurationFieldType.getType()],
        rows: [100, 1000, 10000],
      },
      {
        name: this.$t('databaseScratchTrackFieldsStep.fields.url'),
        props: {
          name: this.$t('databaseScratchTrackFieldsStep.fields.url'),
          type: URLFieldType.getType(),
        },
        icon: icons[URLFieldType.getType()],
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
        icon: icons[EmailFieldType.getType()],
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
          max_value: 5,
        },
        icon: icons[RatingFieldType.getType()],
        rows: [3, 1, 5],
      },
    ]
  }

  getFields() {
    return {}
  }

  afterFieldCreated(field, response) {
    const fieldHandler = fieldHandlerRegistry[field.props.type]
    if (fieldHandler) {
      field.rows = fieldHandler(field, response)
    }
  }
}

export class DatabaseScratchTrackProjectFieldsOnboardingType extends DatabaseScratchTrackFieldsOnboardingType {
  static getType() {
    return 'database_scratch_track_fields_projects'
  }

  getFields() {
    const icons = this.getIcons()
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
        icon: icons[SingleSelectFieldType.getType()],
        rows: selectOptions,
      },
      kickoffDate: {
        props: {
          name: this.$t('databaseScratchTrackFieldsStep.fields.kickoffDate'),
          type: DateFieldType.getType(),
          date_format: 'ISO',
        },
        icon: icons[DateFieldType.getType()],
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
        icon: icons[DateFieldType.getType()],
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
          number_decimal_places: 0,
          number_negative: false,
        },
        icon: icons[NumberFieldType.getType()],
        rows: [500, 1000, 3000],
      },
      completed: {
        props: {
          name: this.$t('databaseScratchTrackFieldsStep.fields.completed'),
          type: BooleanFieldType.getType(),
        },
        icon: icons[BooleanFieldType.getType()],
        rows: [true, false, false],
      },
      notes: {
        props: {
          name: this.$t('databaseScratchTrackFieldsStep.fields.notes'),
          type: LongTextFieldType.getType(),
        },
        icon: icons[LongTextFieldType.getType()],
        rows: [
          this.$t('databaseScratchTrackFieldsStep.projects.row1.notes'),
          this.$t('databaseScratchTrackFieldsStep.projects.row2.notes'),
          this.$t('databaseScratchTrackFieldsStep.projects.row3.notes'),
        ],
      },
    }
  }
}

export class DatabaseScratchTrackTeamFieldsOnboardingType extends DatabaseScratchTrackFieldsOnboardingType {
  static getType() {
    return 'database_scratch_track_fields_teams'
  }

  getFields() {
    const icons = this.getIcons()
    const selectOptions = [
      {
        id: 1,
        value: this.$t('databaseScratchTrackFieldsStep.teams.roles.designer'),
        color: 'gray',
      },
      {
        id: 2,
        value: this.$t('databaseScratchTrackFieldsStep.teams.roles.developer'),
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
        icon: icons[SingleSelectFieldType.getType()],
        rows: selectOptions,
      },
      phone: {
        props: {
          name: this.$t('databaseScratchTrackFieldsStep.fields.phone'),
          type: PhoneNumberFieldType.getType(),
        },
        icon: icons[SingleSelectFieldType.getType()],
        rows: ['(508) 398-0845', '(803) 996-6704', '(269) 445-2068'],
      },
      email: {
        props: {
          name: this.$t('databaseScratchTrackFieldsStep.fields.email'),
          type: EmailFieldType.getType(),
        },
        icon: icons[EmailFieldType.getType()],
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
        icon: icons[BooleanFieldType.getType()],
        rows: [true, false, true],
      },
    }
  }
}

export class DatabaseScratchTrackTaskFieldsOnboardingType extends DatabaseScratchTrackFieldsOnboardingType {
  static getType() {
    return 'database_scratch_track_fields_tasks'
  }

  getFields() {
    const icons = this.getIcons()
    return {
      estimatedDays: {
        props: {
          name: this.$t('databaseScratchTrackFieldsStep.fields.estimatedDays'),
          type: NumberFieldType.getType(),
          number_decimal_places: 0,
          number_negative: false,
        },
        icon: icons[NumberFieldType.getType()],
        rows: [2, 7, 13],
      },
      completed: {
        props: {
          name: this.$t('databaseScratchTrackFieldsStep.fields.completed'),
          type: BooleanFieldType.getType(),
        },
        icon: icons[BooleanFieldType.getType()],
        rows: [true, false, false],
      },
      description: {
        props: {
          name: this.$t('databaseScratchTrackFieldsStep.fields.description'),
          type: LongTextFieldType.getType(),
        },
        icon: icons[LongTextFieldType.getType()],
        rows: [
          this.$t('databaseScratchTrackFieldsStep.tasks.row1.description'),
          this.$t('databaseScratchTrackFieldsStep.tasks.row2.description'),
          this.$t('databaseScratchTrackFieldsStep.tasks.row3.description'),
        ],
      },
    }
  }
}

export class DatabaseScratchTrackCampaignFieldsOnboardingType extends DatabaseScratchTrackFieldsOnboardingType {
  static getType() {
    return 'database_scratch_track_fields_campaigns'
  }

  getFields() {
    const icons = this.getIcons()
    return {
      description: {
        props: {
          name: this.$t('databaseScratchTrackFieldsStep.fields.description'),
          type: LongTextFieldType.getType(),
        },
        icon: icons[LongTextFieldType.getType()],
        rows: [
          this.$t('databaseScratchTrackFieldsStep.campaigns.row1.description'),
          this.$t('databaseScratchTrackFieldsStep.campaigns.row2.description'),
          this.$t('databaseScratchTrackFieldsStep.campaigns.row3.description'),
        ],
      },
      startDate: {
        props: {
          name: this.$t('databaseScratchTrackFieldsStep.fields.startDate'),
          type: DateFieldType.getType(),
          date_format: 'ISO',
        },
        icon: icons[DateFieldType.getType()],
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
        icon: icons[DateFieldType.getType()],
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
          number_decimal_places: 2,
          number_negative: false,
        },
        icon: icons[NumberFieldType.getType()],
        rows: [12000, 30000, 2000],
      },
    }
  }
}

export class DatabaseScratchTrackCustomFieldsOnboardingType extends DatabaseScratchTrackFieldsOnboardingType {
  static getType() {
    return 'database_scratch_track_fields_custom'
  }

  getFields() {
    const icons = this.getIcons()
    return {
      date: {
        props: {
          name: this.$t('databaseScratchTrackFieldsStep.fields.date'),
          type: DateFieldType.getType(),
          date_format: 'ISO',
        },
        icon: icons[DateFieldType.getType()],
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
          number_decimal_places: 0,
          number_negative: true,
        },
        icon: icons[NumberFieldType.getType()],
        rows: [500, -1000, 3000],
      },
      completed: {
        props: {
          name: this.$t('databaseScratchTrackFieldsStep.fields.completed'),
          type: BooleanFieldType.getType(),
        },
        icon: icons[BooleanFieldType.getType()],
        rows: [true, false, false],
      },
      description: {
        props: {
          name: this.$t('databaseScratchTrackFieldsStep.fields.description'),
          type: LongTextFieldType.getType(),
        },
        icon: icons[LongTextFieldType.getType()],
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
  }
}
