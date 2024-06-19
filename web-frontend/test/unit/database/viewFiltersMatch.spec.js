import { TestApp } from '@baserow/test/helpers/testApp'
import moment from '@baserow/modules/core/moment'
import {
  MultipleSelectHasFilterType,
  MultipleSelectHasNotFilterType,
  HasFileTypeViewFilterType,
  FilesLowerThanViewFilterType,
  LengthIsLowerThanViewFilterType,
  LinkRowContainsFilterType,
  LinkRowNotContainsFilterType,
  IsEvenAndWholeViewFilterType,
  HigherThanViewFilterType,
  HigherThanOrEqualViewFilterType,
  LowerThanViewFilterType,
  LowerThanOrEqualViewFilterType,
  IsInRangeViewFilterType,
  SingleSelectIsAnyOfViewFilterType,
  SingleSelectIsNoneOfViewFilterType,
  DateIsBeforeMultiStepViewFilterType,
  DateIsAfterMultiStepViewFilterType,
  DateIsOnOrAfterMultiStepViewFilterType,
  DateIsOnOrBeforeMultiStepViewFilterType,
  DateIsEqualMultiStepViewFilterType,
  DateIsNotEqualMultiStepViewFilterType,
  DateIsWithinMultiStepViewFilterType,
  // DEPRECATED
  DateEqualsCurrentWeekViewFilterType,
  DateEqualsCurrentMonthViewFilterType,
  DateEqualsCurrentYearViewFilterType,
  DateBeforeOrEqualViewFilterType,
  DateBeforeViewFilterType,
  DateBeforeTodayViewFilterType,
  DateAfterDaysAgoViewFilterType,
  DateAfterViewFilterType,
  DateAfterOrEqualViewFilterType,
  DateAfterTodayViewFilterType,
  DateEqualViewFilterType,
  DateNotEqualViewFilterType,
  DateEqualsTodayViewFilterType,
  DateWithinDaysViewFilterType,
  DateWithinWeeksViewFilterType,
  DateWithinMonthsViewFilterType,
  DateEqualsDaysAgoViewFilterType,
  DateEqualsYearsAgoViewFilterType,
} from '@baserow/modules/database/viewFilters'
import {
  DurationFieldType,
  NumberFieldType,
  FormulaFieldType,
  SingleSelectFieldType,
} from '@baserow/modules/database/fieldTypes'

const dateBeforeCases = [
  {
    rowValue: '2021-08-10T21:59:37.940086Z',
    filterValue: 'Europe/Berlin?2021-08-11',
    expected: true,
  },
  {
    rowValue: '2021-08-10',
    filterValue: 'Europe/Berlin?2021-08-11',
    expected: true,
  },
  {
    rowValue: '2021-08-11',
    filterValue: 'Europe/Berlin?2021-08-11',
    expected: false,
  },
  {
    rowValue: '2021-08-10T22:59:37.940086Z',
    filterValue: 'Europe/London?2021-08-11',
    expected: true,
  },
  {
    rowValue: '2021-08-10T22:01:37.940086Z',
    filterValue: 'Europe/Berlin?2021-08-11',
    expected: false,
  },
  {
    rowValue: '2021-08-10T23:01:37.940086Z',
    filterValue: 'Europe/London?2021-08-11',
    expected: false,
  },
  {
    rowValue: '2021-08-10T23:59:37.940086Z',
    filterValue: 'UTC?2021-08-11',
    expected: true,
  },
  {
    rowValue: '2021-08-10',
    filterValue: 'UTC?2021-08-11',
    expected: true,
  },
  {
    rowValue: '2021-08-11T00:01:37.940086Z',
    filterValue: 'UTC?2021-08-11',
    expected: false,
  },
  {
    rowValue: '2021-08-11',
    filterValue: 'UTC?2021-08-11',
    expected: false,
  },
]

const dateAfterCases = [
  {
    rowValue: '2021-08-11T22:01:37.940086Z',
    filterValue: 'Europe/Berlin?2021-08-11',
    expected: true,
  },
  {
    rowValue: '2021-08-12',
    filterValue: 'Europe/Berlin?2021-08-11',
    expected: true,
  },
  {
    rowValue: '2021-08-10',
    filterValue: 'Europe/Berlin?2021-08-11',
    expected: false,
  },
  {
    rowValue: '2021-08-11T23:01:37.940086Z',
    filterValue: 'Europe/Berlin?2021-08-11',
    expected: true,
  },
  {
    rowValue: '2021-08-11T21:59:37.940086Z',
    filterValue: 'Europe/Berlin?2021-08-11',
    expected: false,
  },
  {
    rowValue: '2021-08-11T22:59:37.940086Z',
    filterValue: 'Europe/Berlin?2021-08-11',
    expected: true,
  },
  {
    rowValue: '2021-08-12T00:01:37.940086Z',
    filterValue: 'UTC?2021-08-11',
    expected: true,
  },
  {
    rowValue: '2021-08-12',
    filterValue: 'Europe/Berlin?2021-08-11',
    expected: true,
  },
  {
    rowValue: '2021-08-11T23:59:37.940086Z',
    filterValue: 'UTC?2021-08-11',
    expected: false,
  },
  {
    rowValue: '2021-08-11',
    filterValue: 'UTC?2021-08-11',
    expected: false,
  },
]

const dateBeforeOrEqualCases = [
  {
    rowValue: '2021-08-10T21:59:37.940086Z',
    filterValue: 'Europe/Berlin?2021-08-11',
    expected: true,
  },
  {
    rowValue: '2021-08-10',
    filterValue: 'Europe/Berlin?2021-08-11',
    expected: true,
  },
  {
    rowValue: '2021-08-11',
    filterValue: 'Europe/Berlin?2021-08-11',
    expected: true,
  },
  {
    rowValue: '2021-08-10T22:59:37.940086Z',
    filterValue: 'Europe/London?2021-08-11',
    expected: true,
  },
  {
    rowValue: '2021-08-10T22:01:37.940086Z',
    filterValue: 'Europe/Berlin?2021-08-10',
    expected: false,
  },
  {
    rowValue: '2021-08-10T23:01:37.940086Z',
    filterValue: 'Europe/London?2021-08-10',
    expected: false,
  },
  {
    rowValue: '2021-08-10T23:59:37.940086Z',
    filterValue: 'UTC?2021-08-11',
    expected: true,
  },
  {
    rowValue: '2021-08-10',
    filterValue: 'UTC?2021-08-11',
    expected: true,
  },
  {
    rowValue: '2021-08-11T00:01:37.940086Z',
    filterValue: 'UTC?2021-08-10',
    expected: false,
  },
  {
    rowValue: '2021-08-11',
    filterValue: 'UTC?2021-08-10',
    expected: false,
  },
]

const dateAfterOrEqualCases = [
  {
    rowValue: '2021-08-11T22:01:37.940086Z',
    filterValue: 'Europe/Berlin?2021-08-11',
    expected: true,
  },
  {
    rowValue: '2021-08-12',
    filterValue: 'Europe/Berlin?2021-08-11',
    expected: true,
  },
  {
    rowValue: '2021-08-10',
    filterValue: 'Europe/Berlin?2021-08-09',
    expected: true,
  },
  {
    rowValue: '2021-08-11T23:01:37.940086Z',
    filterValue: 'Europe/Berlin?2021-08-11',
    expected: true,
  },
  {
    rowValue: '2021-08-11T21:59:37.940086Z',
    filterValue: 'Europe/Berlin?2021-08-12',
    expected: false,
  },
  {
    rowValue: '2021-08-10T22:59:37.940086Z',
    filterValue: 'Europe/Berlin?2021-08-12',
    expected: false,
  },
  {
    rowValue: '2021-08-12T00:01:37.940086Z',
    filterValue: 'UTC?2021-08-11',
    expected: true,
  },
  {
    rowValue: '2021-08-12',
    filterValue: 'Europe/Berlin?2021-08-11',
    expected: true,
  },
  {
    rowValue: '2021-08-11T23:59:37.940086Z',
    filterValue: 'UTC?2021-08-12',
    expected: false,
  },
  {
    rowValue: '2021-08-11',
    filterValue: 'UTC?2021-08-12',
    expected: false,
  },
]

const dateEqualCases = [
  {
    rowValue: '2021-08-11T21:59:37.940086Z',
    filterValue: 'Europe/Berlin?2021-08-11',
    expected: true,
  },
  {
    rowValue: '2021-08-11',
    filterValue: 'Europe/Berlin?2021-08-11',
    expected: true,
  },
  {
    rowValue: '2021-08-11T22:59:37.940086Z',
    filterValue: 'Europe/London?2021-08-11',
    expected: true,
  },
  {
    rowValue: '2021-08-10T22:01:37.940086Z',
    filterValue: 'Europe/Berlin?2021-08-11',
    expected: true,
  },
  {
    rowValue: '2021-08-10T23:01:37.940086Z',
    filterValue: 'Europe/London?2021-08-11',
    expected: true,
  },
  {
    rowValue: '2021-08-10T21:59:37.940086Z',
    filterValue: 'Europe/Berlin?2021-08-11',
    expected: false,
  },
  {
    rowValue: '2021-08-10T22:59:37.940086Z',
    filterValue: 'Europe/London?2021-08-11',
    expected: false,
  },
  {
    rowValue: '2021-08-11T23:59:37.940086Z',
    filterValue: 'UTC?2021-08-11',
    expected: true,
  },
  {
    rowValue: '2021-08-11',
    filterValue: 'CET?2021-08-11',
    expected: true,
  },
  {
    rowValue: '2021-08-11T00:01:37.940086Z',
    filterValue: 'UTC?2021-08-11',
    expected: true,
  },
  {
    rowValue: '2021-08-12T00:01:37.940086Z',
    filterValue: 'UTC?2021-08-11',
    expected: false,
  },
  {
    rowValue: '2021-08-12',
    filterValue: 'UTC?2021-08-11',
    expected: false,
  },
]

const dateNotEqualCases = [
  {
    rowValue: '2021-08-11T22:30:37.940086Z',
    filterValue: 'Europe/Berlin?2021-08-11',
    expected: true,
  },
  {
    rowValue: '2021-08-11T21:30:37.940086Z',
    filterValue: 'Europe/Berlin?2021-08-11',
    expected: false,
  },
  {
    rowValue: '2021-08-12',
    filterValue: 'Europe/Berlin?2021-08-11',
    expected: true,
  },
  {
    rowValue: '2021-08-11',
    filterValue: 'Europe/Berlin?2021-08-11',
    expected: false,
  },
  {
    rowValue: '2021-08-11T23:30:37.940086Z',
    filterValue: 'Europe/London?2021-08-11',
    expected: true,
  },
  {
    rowValue: '2021-08-10T22:01:37.940086Z',
    filterValue: 'Europe/Berlin?2021-08-11',
    expected: false,
  },
  {
    rowValue: '2021-08-10T23:01:37.940086Z',
    filterValue: 'Europe/London?2021-08-11',
    expected: false,
  },
  {
    rowValue: '2021-08-11T23:59:37.940086Z',
    filterValue: 'UTC?2021-08-12',
    expected: true,
  },
  {
    rowValue: '2021-08-13T00:01:37.940086Z',
    filterValue: 'UTC?2021-08-12',
    expected: true,
  },
  {
    rowValue: '2021-08-10',
    filterValue: 'UTC?2021-08-11',
    expected: true,
  },
  {
    rowValue: '2021-08-12',
    filterValue: 'UTC?2021-08-11',
    expected: true,
  },
  {
    rowValue: '2021-08-11T22:59:37.940086Z',
    filterValue: 'UTC?2021-08-11',
    expected: false,
  },
  {
    rowValue: '2021-08-11',
    filterValue: 'UTC?2021-08-11',
    expected: false,
  },
]

const dateToday = [
  {
    rowValue: moment().utc().format(),
    filterValue: 'Europe/Berlin',
    expected: true,
  },
  {
    rowValue: '1970-08-11T23:30:37.940086Z',
    filterValue: 'Europe/Berlin',
    expected: false,
  },
]

const dateBeforeToday = [
  {
    rowValue: moment().utc().format(),
    filterValue: 'Europe/Berlin',
    expected: false,
  },
  {
    rowValue: moment().subtract(1, 'day').utc().format(),
    filterValue: 'Europe/Berlin',
    expected: true,
  },
  {
    rowValue: moment().add(1, 'day').utc().format(),
    filterValue: 'Europe/Berlin',
    expected: false,
  },
]

const dateAfterToday = [
  {
    rowValue: moment().utc().format(),
    filterValue: 'Europe/Berlin',
    expected: false,
  },
  {
    rowValue: moment().subtract(1, 'day').utc().format(),
    filterValue: 'Europe/Berlin',
    expected: false,
  },
  {
    rowValue: moment().add(1, 'day').utc().format(),
    filterValue: 'Europe/Berlin',
    expected: true,
  },
]

const dateInThisWeek = [
  {
    rowValue: '2022-05-29',
    filterValue: 'Europe/Berlin',
    expected: false,
  },
  {
    rowValue: '2022-05-29T12:00:00.000000Z',
    filterValue: 'Europe/Berlin',
    expected: false,
  },
  {
    rowValue: '2022-05-30',
    filterValue: 'Europe/Berlin',
    expected: true,
  },
  {
    rowValue: '2022-05-30T12:00:00.000000Z',
    filterValue: 'Europe/Berlin',
    expected: true,
  },
  {
    rowValue: '2022-06-05T12:00:00.000000Z',
    filterValue: 'Europe/Berlin',
    expected: true,
  },
  {
    rowValue: '2022-06-06T12:00:00.000000Z',
    filterValue: 'Europe/Berlin',
    expected: false,
  },
]

const dateInThisMonth = [
  {
    rowValue: '2022-05-01T12:00:00.000000Z',
    filterValue: 'Europe/Berlin?',
    expected: false,
  },
  {
    rowValue: '2022-05-31T21:59:00.000000Z',
    filterValue: 'Europe/Berlin?',
    expected: false,
  },
  {
    rowValue: '2022-06-01T12:00:00.000000Z',
    filterValue: 'Europe/Berlin?',
    expected: true,
  },
  {
    rowValue: '2022-06-30T21:59:00.000000Z',
    filterValue: 'Europe/Berlin?',
    expected: true,
  },
  {
    rowValue: '2022-07-01T00:01:00.000000Z',
    filterValue: 'Europe/Berlin?',
    expected: false,
  },
  {
    rowValue: '2022-05-31T23:59:00.000000Z',
    filterValue: 'Europe/London?',
    expected: true,
  },
]

const dateInThisYear = [
  {
    rowValue: '2021-06-01T12:00:00.000000Z',
    filterValue: 'Europe/Berlin?',
    expected: false,
  },
  {
    rowValue: '2022-06-01T12:00:00.000000Z',
    filterValue: 'Europe/Berlin?',
    expected: true,
  },
]

const dateWithinDays = [
  {
    rowValue: moment().tz('Europe/Berlin').add(1, 'days').format(),
    filterValue: 'Europe/Berlin?1',
    expected: true,
  },
  {
    rowValue: '1970-08-11T23:30:37.940086Z',
    filterValue: 'Europe/Berlin?2',
    expected: false,
  },
  {
    rowValue: moment().utc().add(2, 'days').format(),
    filterValue: 'UTC?3',
    expected: true,
  },
  {
    rowValue: moment().utc().format(),
    filterValue: '?1',
    expected: true,
  },
  {
    rowValue: moment().utc().format(),
    filterValue: 'UTC?1',
    expected: true,
  },
  {
    rowValue: moment().utc().format(),
    filterValue: '?',
    expected: true,
  },
  {
    rowValue: moment().utc().subtract(1, 'days').format(),
    filterValue: '?',
    expected: true,
  },
  {
    rowValue: moment().utc().subtract(1, 'days').format(),
    filterValue: '',
    expected: true,
  },
]

const dateWithinWeeks = [
  {
    rowValue: moment().tz('Europe/Berlin').add(5, 'days').format(),
    filterValue: 'Europe/Berlin?1',
    expected: true,
  },
  {
    rowValue: '1970-08-11T23:30:37.940086Z',
    filterValue: 'Europe/Berlin?2',
    expected: false,
  },
  {
    rowValue: moment().utc().add(20, 'days').format(),
    filterValue: 'UTC?3',
    expected: true,
  },
  {
    rowValue: moment().utc().format(),
    filterValue: '?1',
    expected: true,
  },
  {
    rowValue: moment().utc().format(),
    filterValue: 'UTC?1',
    expected: true,
  },
  {
    rowValue: moment().utc().format(),
    filterValue: '?1',
    expected: true,
  },
  {
    rowValue: moment().utc().subtract(1, 'days').format(),
    filterValue: '?1',
    expected: false,
  },
  {
    rowValue: moment().utc().subtract(1, 'days').format(),
    filterValue: '',
    expected: true,
  },
]

const dateWithinMonths = [
  {
    rowValue: moment().tz('Europe/Berlin').add(20, 'days').format(),
    filterValue: 'Europe/Berlin?1',
    expected: true,
  },
  {
    rowValue: '1970-08-11T23:30:37.940086Z',
    filterValue: 'Europe/Berlin?2',
    expected: false,
  },
  {
    rowValue: moment().utc().add(80, 'days').format(),
    filterValue: 'UTC?3',
    expected: true,
  },
  {
    rowValue: moment().utc().format(),
    filterValue: '?1',
    expected: true,
  },
  {
    rowValue: moment().utc().format(),
    filterValue: 'UTC?1',
    expected: true,
  },
  {
    rowValue: moment().utc().format(),
    filterValue: '?',
    expected: true,
  },
  {
    rowValue: moment().utc().subtract(1, 'days').format(),
    filterValue: '?',
    expected: true,
  },
  {
    rowValue: moment().utc().subtract(1, 'days').format(),
    filterValue: '',
    expected: true,
  },
]

const dateDaysAgo = [
  {
    rowValue: moment().utc().tz('Europe/Berlin').subtract(1, 'days').format(),
    filterValue: 'Europe/Berlin?1',
    expected: true,
  },
  {
    rowValue: '1970-08-11T23:30:37.940086Z',
    filterValue: 'Europe/Berlin?2',
    expected: false,
  },
  {
    rowValue: moment().utc().subtract(3, 'days').format(),
    filterValue: 'UTC?3',
    expected: true,
  },
  {
    rowValue: moment().utc().format(),
    filterValue: '?1',
    expected: false,
  },
  {
    rowValue: moment().utc().format(),
    filterValue: 'UTC?1',
    expected: false,
  },
  {
    rowValue: moment().utc().format(),
    filterValue: '?',
    expected: true,
  },
  {
    rowValue: moment().utc().subtract(1, 'days').format(),
    filterValue: '?',
    expected: true,
  },
  {
    rowValue: moment().utc().subtract(1, 'days').format(),
    filterValue: '',
    expected: true,
  },
]

const dateMonthsAgo = [
  {
    rowValue: moment().tz('Europe/Berlin').subtract(1, 'months').format(),
    filterValue: 'Europe/Berlin?1',
    expected: true,
  },
  {
    rowValue: '1970-08-11T23:30:37.940086Z',
    filterValue: 'Europe/Berlin?2',
    expected: false,
  },
  {
    rowValue: moment().utc().subtract(3, 'months').format(),
    filterValue: 'UTC?3',
    expected: true,
  },
  {
    rowValue: moment().utc().format(),
    filterValue: '?1',
    expected: false,
  },
  {
    rowValue: moment().utc().format(),
    filterValue: 'UTC?1',
    expected: false,
  },
  {
    rowValue: moment().utc().format(),
    filterValue: '?',
    expected: true,
  },
  {
    rowValue: moment().utc().subtract(1, 'months').format(),
    filterValue: '?1',
    expected: true,
  },
  {
    rowValue: moment().utc().subtract(1, 'months').format(),
    filterValue: '',
    expected: true,
  },
]

const dateYearsAgo = [
  {
    rowValue: moment().tz('Europe/Berlin').subtract(1, 'years').format(),
    filterValue: 'Europe/Berlin?1',
    expected: true,
  },
  {
    rowValue: '1970-08-11T23:30:37.940086Z',
    filterValue: 'Europe/Berlin?2',
    expected: false,
  },
  {
    rowValue: moment().utc().subtract(3, 'years').format(),
    filterValue: 'UTC?3',
    expected: true,
  },
  {
    rowValue: moment().utc().format(),
    filterValue: '?1',
    expected: false,
  },
  {
    rowValue: moment().utc().format(),
    filterValue: 'UTC?1',
    expected: false,
  },
  {
    rowValue: moment().utc().format(),
    filterValue: '?0',
    expected: true,
  },
  {
    rowValue: moment().utc().subtract(1, 'years').format(),
    filterValue: 'UTC?1',
    expected: true,
  },
  {
    rowValue: moment().utc().subtract(1, 'years').format(),
    filterValue: '?1',
    expected: true,
  },
]

const multipleSelectValuesHas = [
  {
    rowValue: [
      { id: 155, value: 'A', color: 'green' },
      { id: 154, value: 'B', color: 'green' },
    ],
    filterValue: 154,
    expected: true,
  },
  {
    rowValue: [
      { id: 155, value: 'A', color: 'green' },
      { id: 154, value: 'B', color: 'green' },
    ],
    filterValue: 200,
    expected: false,
  },
  {
    rowValue: [
      { id: 155, value: 'A', color: 'green' },
      { id: 154, value: 'B', color: 'green' },
    ],
    filterValue: 'wrong_type',
    expected: true,
  },
]

const multipleSelectValuesHasNot = [
  {
    rowValue: [
      { id: 155, value: 'A', color: 'green' },
      { id: 154, value: 'B', color: 'green' },
    ],
    filterValue: 154,
    expected: false,
  },
  {
    rowValue: [
      { id: 155, value: 'A', color: 'green' },
      { id: 154, value: 'B', color: 'green' },
    ],
    filterValue: 200,
    expected: true,
  },
  {
    rowValue: [
      { id: 155, value: 'A', color: 'green' },
      { id: 154, value: 'B', color: 'green' },
    ],
    filterValue: 'wrong_type',
    expected: true,
  },
]

const lengthIsLowerThanCases = [
  {
    rowValue: 'bill',
    filterValue: 0,
    expected: true,
  },
  {
    rowValue: 'bill',
    filterValue: 1,
    expected: false,
  },
  {
    rowValue: 'bill',
    filterValue: 4,
    expected: false,
  },
  {
    rowValue: 'bill',
    filterValue: 5,
    expected: true,
  },
  {
    rowValue: 'bill',
    filterValue: 'a',
    expected: true,
  },
]

/**
 * SingleSelectIsAnyOfViewFilterType and SingleSelectIsNoneOfViewFilterType test values.
 *
 * In case of SingleSelectIsNoneOfViewFilterType we expect negation of .expected
 */
const singleSelectValuesInFilterCases = [
  {
    rowValue: { id: 1 },
    filterValue: '1,2',
    is_any_of: true,
    is_none_of: false,
  },
  {
    rowValue: { id: 2 },
    filterValue: '1,2',
    is_any_of: true,
    is_none_of: false,
  },
  {
    rowValue: { id: 3 },
    filterValue: '1,2',
    is_any_of: false,
    is_none_of: true,
  },
  {
    rowValue: { id: 4 },
    filterValue: '1,2',
    is_any_of: false,
    is_none_of: true,
  },
  {
    rowValue: { id: 5 },
    filterValue: '1',
    is_any_of: false,
    is_none_of: true,
  },
  {
    rowValue: { id: 5 },
    filterValue: '1, 5',
    is_any_of: true,
    is_none_of: false,
  },
  {
    rowValue: { id: 5 },
    filterValue: '',
    is_any_of: true,
    is_none_of: true,
  },
  {
    rowValue: null,
    filterValue: '',
    is_any_of: true,
    is_none_of: true,
  },
  {
    rowValue: { id: 1 },
    filterValue: '',
    is_any_of: true,
    is_none_of: true,
  },
  {
    rowValue: { id: 1 },
    filterValue: 'test,test2',
    is_any_of: false,
    is_none_of: true,
  },
  {
    rowValue: { id: 1 },
    filterValue: '1,test2',
    is_any_of: true,
    is_none_of: false,
  },
]

describe('(DEPRECATED) Date in this week, month and year tests', () => {
  let testApp = null
  let dateNowSpy

  beforeAll(() => {
    testApp = new TestApp()
    // Wed Jun 01 2022 00:00:00 UTC
    dateNowSpy = jest.spyOn(Date, 'now').mockImplementation(() => 1654041600000)
  })

  afterAll(() => {
    dateNowSpy.mockRestore()
  })

  afterEach(() => {
    testApp.afterEach()
  })

  test.each(dateInThisWeek)(
    '(DEPRECATED) DateInThisWeek with timezone.',
    (values) => {
      const result = new DateEqualsCurrentWeekViewFilterType({
        app: testApp,
      }).matches(values.rowValue, values.filterValue, {
        date_include_time: true,
      })
      expect(result).toBe(values.expected)
    }
  )

  test.each(dateInThisWeek)('DateInThisWeek with timezone.', (values) => {
    const result = new DateIsEqualMultiStepViewFilterType({
      app: testApp,
    }).matches(values.rowValue, `${values.filterValue}??this_week`, {
      date_include_time: true,
    })
    expect(result).toBe(values.expected)
  })

  test.each(dateInThisWeek)(
    '(DEPRECATED) DateInThisWeek without timezone.',
    (values) => {
      const result = new DateEqualsCurrentWeekViewFilterType({
        app: testApp,
      }).matches(values.rowValue, values.filterValue, {})
      expect(result).toBe(values.expected)
    }
  )

  test.each(dateInThisWeek)('DateInThisWeek without timezone.', (values) => {
    const result = new DateIsEqualMultiStepViewFilterType({
      app: testApp,
    }).matches(values.rowValue, `${values.filterValue}??this_week`, {})
    expect(result).toBe(values.expected)
  })

  test.each(dateInThisMonth)('(DEPRECATED) DateInThisMonth', (values) => {
    const result = new DateEqualsCurrentMonthViewFilterType({
      app: testApp,
    }).matches(values.rowValue, values.filterValue, {})
    expect(result).toBe(values.expected)
  })

  test.each(dateInThisMonth)('DateInThisMonth', (values) => {
    const result = new DateIsEqualMultiStepViewFilterType({
      app: testApp,
    }).matches(values.rowValue, `${values.filterValue}?this_month`, {})
    expect(result).toBe(values.expected)
  })

  test.each(dateInThisYear)('(DEPRECATED) DateInThisYear', (values) => {
    const result = new DateEqualsCurrentYearViewFilterType({
      app: testApp,
    }).matches(values.rowValue, values.filterValue, {})
    expect(result).toBe(values.expected)
  })

  test.each(dateInThisYear)('DateInThisYear', (values) => {
    const result = new DateIsEqualMultiStepViewFilterType({
      app: testApp,
    }).matches(values.rowValue, `${values.filterValue}?this_year`, {})
    expect(result).toBe(values.expected)
  })
})

const linkRowContainsCases = [
  {
    rowValue: [{ value: 'bill' }],
    filterValue: '',
    expected: true,
  },
  {
    rowValue: [{ value: 'bill' }],
    filterValue: 'bi',
    expected: true,
  },
  {
    rowValue: [{ value: 'some other name' }],
    filterValue: 'bill',
    expected: false,
  },
  {
    rowValue: [{ value: 'some other name' }, { value: 'bill' }],
    filterValue: 'bill',
    expected: true,
  },
  {
    rowValue: [{ value: 'BILL' }],
    filterValue: 'bill',
    expected: true,
  },
  {
    rowValue: [{ value: 'bill' }],
    filterValue: 'BILL',
    expected: true,
  },
]

const linkRowNotContainsCases = [
  {
    rowValue: [{ value: 'bill' }],
    filterValue: '',
    expected: true,
  },
  {
    rowValue: [{ value: 'bill' }],
    filterValue: 'bi',
    expected: false,
  },
  {
    rowValue: [{ value: 'some other name' }],
    filterValue: 'bill',
    expected: true,
  },
  {
    rowValue: [{ value: 'some other name' }, { value: 'bill' }],
    filterValue: 'bill',
    expected: false,
  },
  {
    rowValue: [{ value: 'BILL' }],
    filterValue: 'bill',
    expected: false,
  },
  {
    rowValue: [{ value: 'bill' }],
    filterValue: 'BILL',
    expected: false,
  },
]

const dateDaysAfterValidCases = [
  {
    rowValue: moment.utc().subtract(5, 'days').format(),
    filterValue: 'UTC?10',
    expected: true,
  },
  {
    rowValue: moment.utc().subtract(10, 'days').format(),
    filterValue: 'UTC?10',
    expected: true,
  },
  {
    rowValue: moment.utc().subtract(21, 'days').format(),
    filterValue: 'UTC?30',
    expected: true,
  },
  {
    rowValue: moment.utc().subtract(10, 'days').add(5, 'hours').format(),
    filterValue: 'Europe/Berlin?10',
    expected: true,
  },
]

const dateDaysAfterInvalidCases = [
  {
    rowValue: moment.utc().subtract(15, 'days').format(),
    filterValue: 'UTC?10',
    expected: false,
  },
  {
    rowValue: null,
    filterValue: 'UTC?15',
    expected: false,
  },
  {
    rowValue: moment.utc().subtract(5, 'days').format(),
    filterValue: 'UTC?-10',
    expected: false,
  },
  {
    rowValue: moment.utc().subtract(20, 'days').format(),
    filterValue: 'Europe/Berlin?10',
    expected: false,
  },
  {
    rowValue: moment.utc().subtract(10, 'days').add(5, 'hours').format(),
    filterValue: 'UTC?abc',
    expected: false,
  },
  {
    rowValue: moment.utc().subtract(10, 'days').add(5, 'hours').format(),
    filterValue: 'UTC? ',
    expected: false,
  },
]

// When this filter is applied, it should return even AND whole numbers:
const numberIsEvenAndWholeCases = [
  {
    rowValue: 2,
    expected: true,
  },
  {
    rowValue: 2.2,
    expected: false,
  },
  {
    rowValue: 3.0,
    expected: false,
  },
  {
    rowValue: 3.3,
    expected: false,
  },
  {
    rowValue: 4.0,
    expected: true,
  },
  {
    rowValue: null,
    expected: false,
  },
]

const durationHigherThanCases = [
  {
    rowValue: null,
    filterValue: '1:01',
    context: { field: { duration_format: 'h:mm' } },
    expected: false,
  },
  {
    rowValue: 60,
    filterValue: '0:01',
    context: { field: { duration_format: 'h:mm' } },
    expected: false,
  },
  {
    rowValue: 120,
    filterValue: '0:01',
    context: { field: { duration_format: 'h:mm' } },
    expected: true,
  },
  {
    rowValue: 61, // will be rounded to 0:01
    filterValue: 60,
    context: { field: { duration_format: 'h:mm' } },
    expected: false,
  },
  {
    rowValue: 61,
    filterValue: 60,
    context: { field: { duration_format: 'h:mm:ss' } },
    expected: true,
  },
  {
    rowValue: 864001,
    filterValue: '24:00:00',
    context: { field: { duration_format: 'h:mm:ss' } },
    expected: true,
  },
]

const durationLowerThanCases = [
  {
    rowValue: null,
    filterValue: '1:01',
    context: { field: { duration_format: 'h:mm' } },
    expected: false,
  },
  {
    rowValue: 20,
    filterValue: '0:01',
    context: { field: { duration_format: 'h:mm' } },
    expected: true,
  },
  {
    rowValue: 120,
    filterValue: '0:01',
    context: { field: { duration_format: 'h:mm' } },
    expected: false,
  },
  {
    rowValue: 61, // will be rounded to 0:01
    filterValue: 60,
    context: { field: { duration_format: 'h:mm' } },
    expected: false,
  },
  {
    rowValue: 59,
    filterValue: 60,
    context: { field: { duration_format: 'h:mm:ss' } },
    expected: true,
  },
  {
    rowValue: 86399,
    filterValue: '24:00:00',
    context: { field: { duration_format: 'h:mm:ss' } },
    expected: true,
  },
]

const numberValueIsHigherThanCases = [
  {
    rowValue: 2,
    filterValue: 0,
    expected: true,
  },
  {
    rowValue: null,
    filterValue: 0,
    expected: false,
  },
  {
    rowValue: 0,
    filterValue: '0',
    expected: false,
  },
]

const numberValueIsHigherThanOrEqualCases = [
  {
    rowValue: 2,
    filterValue: 3,
    expected: false,
  },
  {
    rowValue: 2,
    filterValue: 0,
    expected: true,
  },
  {
    rowValue: null,
    filterValue: 0,
    expected: false,
  },
  {
    rowValue: 1,
    filterValue: '-1',
    expected: true,
  },
  {
    rowValue: 0,
    filterValue: '0',
    expected: true,
  },
  {
    rowValue: -1,
    filterValue: '-1',
    expected: true,
  },
  {
    rowValue: -1,
    filterValue: '0',
    expected: false,
  },
]

const numberValueIsLowerThanCases = [
  {
    rowValue: 1,
    filterValue: '2',
    expected: true,
  },
  {
    rowValue: null,
    filterValue: 0,
    expected: false,
  },
  {
    rowValue: 0,
    filterValue: '0',
    expected: false,
  },
]

const numberValueIsLowerThanOrEqualCases = [
  {
    rowValue: 2,
    filterValue: 3,
    expected: true,
  },
  {
    rowValue: 2,
    filterValue: 0,
    expected: false,
  },
  {
    rowValue: null,
    filterValue: 0,
    expected: false,
  },
  {
    rowValue: 1,
    filterValue: '-1',
    expected: false,
  },
  {
    rowValue: 0,
    filterValue: '0',
    expected: true,
  },
  {
    rowValue: -1,
    filterValue: '-1',
    expected: true,
  },
  {
    rowValue: -1,
    filterValue: '0',
    expected: true,
  },
]

const numberValueIsInRangeCases = [
  {
    rowValue: 2,
    filterValue: '1?3',
    expected: true,
  },
  {
    rowValue: 2,
    filterValue: '1?2',
    expected: true,
  },
  {
    rowValue: 2,
    filterValue: '2?3',
    expected: true,
  },
  {
    rowValue: 2,
    filterValue: '2?2',
    expected: true,
  },
  {
    rowValue: 0,
    filterValue: '-1?1',
    expected: true,
  },
  {
    rowValue: -5,
    filterValue: '-10?-1',
    expected: true,
  },
  {
    rowValue: 10,
    filterValue: '1?2',
    expected: false,
  },
  {
    rowValue: 1,
    filterValue: '10?20',
    expected: false,
  },
  {
    rowValue: -5,
    filterValue: '1?-10',
    expected: false,
  },
  {
    rowValue: null,
    filterValue: '1?2',
    expected: false,
  }
]

describe('All Tests', () => {
  let testApp = null

  beforeAll(() => {
    testApp = new TestApp()
  })

  afterEach(() => {
    testApp.afterEach()
  })

  test.each(dateBeforeCases)('(DEPRECATED) BeforeViewFilter', (values) => {
    const result = new DateBeforeViewFilterType({ app: testApp }).matches(
      values.rowValue,
      values.filterValue,
      { date_include_time: true }
    )
    expect(result).toBe(values.expected)
  })

  test.each(dateBeforeCases)('BeforeViewFilter', (values) => {
    const result = new DateIsBeforeMultiStepViewFilterType({
      app: testApp,
    }).matches(values.rowValue, `${values.filterValue}?exact_date`, {
      date_include_time: true,
    })
    expect(result).toBe(values.expected)
  })

  test.each(dateBeforeOrEqualCases)(
    '(DEPRECATED) BeforeOrEqualViewFilter',
    (values) => {
      const result = new DateBeforeOrEqualViewFilterType({
        app: testApp,
      }).matches(values.rowValue, values.filterValue, {
        date_include_time: true,
      })
      expect(result).toBe(values.expected)
    }
  )

  test.each(dateBeforeOrEqualCases)('BeforeOrEqualViewFilter', (values) => {
    const result = new DateIsOnOrBeforeMultiStepViewFilterType({
      app: testApp,
    }).matches(values.rowValue, `${values.filterValue}?exact_date`, {
      date_include_time: true,
    })
    expect(result).toBe(values.expected)
  })

  test.each(dateAfterCases)('(DEPRECATED) AfterViewFilter', (values) => {
    const result = new DateAfterViewFilterType({ app: testApp }).matches(
      values.rowValue,
      values.filterValue,
      { date_include_time: true }
    )
    expect(result).toBe(values.expected)
  })

  test.each(dateAfterCases)('AfterViewFilter', (values) => {
    const result = new DateIsAfterMultiStepViewFilterType({
      app: testApp,
    }).matches(values.rowValue, `${values.filterValue}?exact_date`, {
      date_include_time: true,
    })
    expect(result).toBe(values.expected)
  })

  test.each(dateAfterOrEqualCases)(
    '(DEPRECATED) AfterOrEqualViewFilter',
    (values) => {
      const result = new DateAfterOrEqualViewFilterType({
        app: testApp,
      }).matches(values.rowValue, values.filterValue, {
        date_include_time: true,
      })
      expect(result).toBe(values.expected)
    }
  )

  test.each(dateAfterOrEqualCases)('AfterOrEqualViewFilter', (values) => {
    const result = new DateIsAfterMultiStepViewFilterType({
      app: testApp,
    }).matches(values.rowValue, `${values.filterValue}?exact_date`, {
      date_include_time: true,
    })
    expect(result).toBe(values.expected)
  })

  test.each(dateEqualCases)('(DEPRECATED) DateEqual', (values) => {
    const result = new DateEqualViewFilterType({ app: testApp }).matches(
      values.rowValue,
      values.filterValue,
      { date_include_time: true }
    )
    expect(result).toBe(values.expected)
  })

  test.each(dateEqualCases)('DateEqual', (values) => {
    const result = new DateIsEqualMultiStepViewFilterType({
      app: testApp,
    }).matches(values.rowValue, `${values.filterValue}?exact_date`, {
      date_include_time: true,
    })
    expect(result).toBe(values.expected)
  })

  test.each(dateNotEqualCases)('(DEPRECATED) DateNotEqual', (values) => {
    const result = new DateNotEqualViewFilterType({ app: testApp }).matches(
      values.rowValue,
      values.filterValue,
      { date_include_time: true }
    )

    expect(result).toBe(values.expected)
  })

  test.each(dateNotEqualCases)('DateNotEqual', (values) => {
    const result = new DateIsNotEqualMultiStepViewFilterType({
      app: testApp,
    }).matches(values.rowValue, `${values.filterValue}?exact_date`, {
      date_include_time: true,
    })
    expect(result).toBe(values.expected)
  })

  test.each(dateToday)('(DEPRECATED) DateToday', (values) => {
    const result = new DateEqualsTodayViewFilterType({ app: testApp }).matches(
      values.rowValue,
      values.filterValue,
      {}
    )
    expect(result).toBe(values.expected)
  })

  test.each(dateToday)('DateToday', (values) => {
    const result = new DateIsEqualMultiStepViewFilterType({
      app: testApp,
    }).matches(values.rowValue, `${values.filterValue}??today`, {})
    expect(result).toBe(values.expected)
  })

  test.each(dateBeforeToday)('(DEPRECATED) DateBeforeToday', (values) => {
    const result = new DateBeforeTodayViewFilterType({ app: testApp }).matches(
      values.rowValue,
      values.filterValue,
      {}
    )
    expect(result).toBe(values.expected)
  })

  test.each(dateBeforeToday)('DateBeforeToday', (values) => {
    const result = new DateIsBeforeMultiStepViewFilterType({
      app: testApp,
    }).matches(values.rowValue, `${values.filterValue}??today`, {})
    expect(result).toBe(values.expected)
  })

  test.each(dateAfterToday)('(DEPRECATED) DateAfterToday', (values) => {
    const result = new DateAfterTodayViewFilterType({ app: testApp }).matches(
      values.rowValue,
      values.filterValue,
      {}
    )
    expect(result).toBe(values.expected)
  })

  test.each(dateAfterToday)('DateAfterToday', (values) => {
    const result = new DateIsAfterMultiStepViewFilterType({
      app: testApp,
    }).matches(values.rowValue, `${values.filterValue}??today`, {})
    expect(result).toBe(values.expected)
  })

  test.each(dateWithinDays)('(DEPRECATED) DateWithinDays', (values) => {
    const result = new DateWithinDaysViewFilterType({
      app: testApp,
    }).matches(values.rowValue, values.filterValue, {})
    expect(result).toBe(values.expected)
  })

  test.each(dateWithinDays)('DateWithinDays', (values) => {
    const result = new DateIsWithinMultiStepViewFilterType({
      app: testApp,
    }).matches(values.rowValue, `${values.filterValue}?nr_days_from_now`, {})
    expect(result).toBe(values.expected)
  })

  test.each(dateWithinWeeks)('(DEPRECATED) DateWithinWeeks', (values) => {
    const result = new DateWithinWeeksViewFilterType({
      app: testApp,
    }).matches(values.rowValue, values.filterValue, {})
    expect(result).toBe(values.expected)
  })

  test.each(dateWithinWeeks)('DateWithinWeeks', (values) => {
    const result = new DateWithinWeeksViewFilterType({
      app: testApp,
    }).matches(values.rowValue, `${values.filterValue}?nr_weeks_from_now`, {})
    expect(result).toBe(values.expected)
  })

  test.each(dateWithinMonths)('(DEPRECATED) DateWithinMonths', (values) => {
    const result = new DateWithinMonthsViewFilterType({
      app: testApp,
    }).matches(values.rowValue, values.filterValue, {})
    expect(result).toBe(values.expected)
  })

  test.each(dateWithinMonths)('DateWithinMonths', (values) => {
    const result = new DateWithinMonthsViewFilterType({
      app: testApp,
    }).matches(values.rowValue, `${values.filterValue}?nr_months_from_now`, {})
    expect(result).toBe(values.expected)
  })

  test.each(dateDaysAgo)('(DEPRECATED) DateDaysAgo', (values) => {
    const result = new DateEqualsDaysAgoViewFilterType({
      app: testApp,
    }).matches(values.rowValue, values.filterValue, {})
    expect(result).toBe(values.expected)
  })

  test.each(dateDaysAgo)('DateDaysAgo', (values) => {
    const result = new DateIsEqualMultiStepViewFilterType({
      app: testApp,
    }).matches(values.rowValue, `${values.filterValue}?nr_days_ago`, {})
    expect(result).toBe(values.expected)
  })

  test.each(dateMonthsAgo)('DateMonthsAgo', (values) => {
    const result = new DateIsEqualMultiStepViewFilterType({
      app: testApp,
    }).matches(values.rowValue, `${values.filterValue}?nr_months_ago`, {})
    expect(result).toBe(values.expected)
  })

  test.each(dateYearsAgo)('(DEPRECATED) DateYearsAgo', (values) => {
    const result = new DateEqualsYearsAgoViewFilterType({
      app: testApp,
    }).matches(values.rowValue, values.filterValue, {})
    expect(result).toBe(values.expected)
  })

  test.each(dateYearsAgo)('DateYearsAgo', (values) => {
    const result = new DateIsEqualMultiStepViewFilterType({
      app: testApp,
    }).matches(values.rowValue, `${values.filterValue}?nr_years_ago`, {})
    expect(result).toBe(values.expected)
  })

  test.each(multipleSelectValuesHas)('MultipleSelect Has', (values) => {
    const result = new MultipleSelectHasFilterType().matches(
      values.rowValue,
      values.filterValue,
      {}
    )
    expect(result).toBe(values.expected)
  })

  test.each(multipleSelectValuesHasNot)('MultipleSelect Has Not', (values) => {
    const result = new MultipleSelectHasNotFilterType().matches(
      values.rowValue,
      values.filterValue,
      {}
    )
    expect(result).toBe(values.expected)
  })

  test.each(lengthIsLowerThanCases)(
    'LengthIsLowerThanViewFilterType',
    (values) => {
      const result = new LengthIsLowerThanViewFilterType().matches(
        values.rowValue,
        values.filterValue
      )
      expect(result).toBe(values.expected)
    }
  )

  test.each(linkRowContainsCases)('LinkRowContainsFilterType', (values) => {
    const result = new LinkRowContainsFilterType().matches(
      values.rowValue,
      values.filterValue
    )
    expect(result).toBe(values.expected)
  })

  test.each(linkRowNotContainsCases)(
    'LinkRowNotContainsFilterType',
    (values) => {
      const result = new LinkRowNotContainsFilterType().matches(
        values.rowValue,
        values.filterValue
      )
      expect(result).toBe(values.expected)
    }
  )

  test.each(dateDaysAfterValidCases)(
    '(DEPRECATED) DateDaysAfterValidFilterType',
    (values) => {
      const result = new DateAfterDaysAgoViewFilterType().matches(
        values.rowValue,
        values.filterValue
      )
      expect(result).toBe(values.expected)
    }
  )

  test.each(dateDaysAfterValidCases)(
    'DateDaysAfterValidFilterType',
    (values) => {
      const result = new DateIsOnOrAfterMultiStepViewFilterType().matches(
        values.rowValue,
        `${values.filterValue}?nr_days_ago`
      )
      expect(result).toBe(values.expected)
    }
  )

  test.each(dateDaysAfterInvalidCases)(
    '(DEPRECATED) DateDaysAfterInvalidFilterType',
    (values) => {
      const result = new DateAfterDaysAgoViewFilterType().matches(
        values.rowValue,
        values.filterValue
      )
      expect(result).toBe(values.expected)
    }
  )

  test.each(dateDaysAfterInvalidCases)(
    'DateDaysAfterInvalidFilterType',
    (values) => {
      const result = new DateIsOnOrAfterMultiStepViewFilterType().matches(
        values.rowValue,
        `${values.filterValue}?nr_days_ago`
      )
      expect(result).toBe(values.expected)
    }
  )

  test.each(numberIsEvenAndWholeCases)(
    'IsEvenAndWholeViewFilterType',
    (values) => {
      const result = new IsEvenAndWholeViewFilterType({
        app: testApp,
      }).matches(values.rowValue, values.filterValue, {})
      expect(result).toBe(values.expected)
    }
  )

  test('HasFileType contains image', () => {
    expect(new HasFileTypeViewFilterType().matches([], '', {})).toBe(true)
    expect(new HasFileTypeViewFilterType().matches([], 'image', {})).toBe(false)
    expect(new HasFileTypeViewFilterType().matches([], 'document', {})).toBe(
      false
    )
    expect(
      new HasFileTypeViewFilterType().matches([{ is_image: true }], 'image', {})
    ).toBe(true)
    expect(
      new HasFileTypeViewFilterType().matches(
        [{ is_image: true }],
        'document',
        {}
      )
    ).toBe(false)
    expect(
      new HasFileTypeViewFilterType().matches(
        [{ is_image: false }],
        'image',
        {}
      )
    ).toBe(false)
    expect(
      new HasFileTypeViewFilterType().matches(
        [{ is_image: false }],
        'document',
        {}
      )
    ).toBe(true)
    expect(
      new HasFileTypeViewFilterType().matches(
        [{ is_image: true }, { is_image: false }],
        'image',
        {}
      )
    ).toBe(true)
    expect(
      new HasFileTypeViewFilterType().matches(
        [{ is_image: true }, { is_image: false }],
        'document',
        {}
      )
    ).toBe(true)
  })

  test('FilesLowerThanFilterType', () => {
    expect(new FilesLowerThanViewFilterType().matches([], 0)).toBe(false)
    expect(
      new FilesLowerThanViewFilterType().matches(
        [
          { visible_name: 'test_file_1.txt' },
          { visible_name: 'test_file_2.txt' },
        ],
        2
      )
    ).toBe(false)
    expect(
      new FilesLowerThanViewFilterType().matches(
        [
          { visible_name: 'test_file_1.txt' },
          { visible_name: 'test_file_2.txt' },
        ],
        3
      )
    ).toBe(true)
  })

  test.each(durationHigherThanCases)(
    'DurationHigherThanFilterType',
    (values) => {
      const fieldType = new DurationFieldType({
        app: testApp,
      })
      const { field } = values.context
      const result = new HigherThanViewFilterType({ app: testApp }).matches(
        values.rowValue,
        values.filterValue,
        field,
        fieldType
      )
      expect(result).toBe(values.expected)
    }
  )

  test.each(durationLowerThanCases)('DurationLowerThanFilterType', (values) => {
    const app = testApp.getApp()
    const fieldType = new DurationFieldType({ app })
    const { field } = values.context
    const result = new LowerThanViewFilterType({ app }).matches(
      values.rowValue,
      values.filterValue,
      field,
      fieldType
    )
    expect(result).toBe(values.expected)
  })

  test.each(numberValueIsHigherThanCases)(
    'NumberHigherThanFilterType',
    (values) => {
      const app = testApp.getApp()
      const result = new HigherThanViewFilterType({ app }).matches(
        values.rowValue,
        values.filterValue,
        { type: 'number' },
        new NumberFieldType({ app })
      )
      expect(result).toBe(values.expected)
    }
  )

  test.each(numberValueIsHigherThanOrEqualCases)(
    'NumberHigherThanOrEqualFilterType',
    (values) => {
      const app = testApp.getApp()
      const result = new HigherThanOrEqualViewFilterType({ app }).matches(
        values.rowValue,
        values.filterValue,
        { type: 'number' },
        new NumberFieldType({ app })
      )
      expect(result).toBe(values.expected)
    }
  )

  test.each(numberValueIsHigherThanCases)(
    'FormulaNumberHigherThanFilterType',
    (values) => {
      const app = testApp.getApp()
      const result = new HigherThanViewFilterType({ app }).matches(
        values.rowValue,
        values.filterValue,
        { type: 'formula', formula_type: 'number' },
        new FormulaFieldType({ app })
      )
      expect(result).toBe(values.expected)
    }
  )

  test.each(numberValueIsLowerThanCases)(
    'NumberLowerThanFilterType',
    (values) => {
      const app = testApp.getApp()
      const result = new LowerThanViewFilterType({ app }).matches(
        values.rowValue,
        values.filterValue,
        { type: 'number' },
        new NumberFieldType({ app })
      )
      expect(result).toBe(values.expected)
    }
  )

  test.each(numberValueIsLowerThanOrEqualCases)(
    'NumberLowerThanOrEqualFilterType',
    (values) => {
      const app = testApp.getApp()
      const result = new LowerThanOrEqualViewFilterType({ app }).matches(
        values.rowValue,
        values.filterValue,
        { type: 'number' },
        new NumberFieldType({ app })
      )
      expect(result).toBe(values.expected)
    }
  )

  test.each(numberValueIsLowerThanCases)(
    'FormulaNumberLowerThanFilterType',
    (values) => {
      const app = testApp.getApp()
      const result = new LowerThanViewFilterType({ app }).matches(
        values.rowValue,
        values.filterValue,
        { type: 'formula', formula_type: 'number' },
        new FormulaFieldType({ app })
      )
      expect(result).toBe(values.expected)
    }
  )

  test.each(numberValueIsInRangeCases)(
    'NumberIsInRangeFilterType',
    (values) => {
      const app = testApp.getApp()
      const result = new IsInRangeViewFilterType({ app }).matches(
        values.rowValue,
        values.filterValue,
        { type: 'number' },
        new NumberFieldType({ app })
      )
      expect(result).toBe(values.expected)
    }
  )

  test.each(singleSelectValuesInFilterCases)(
    'SingleSelectIsAnyOfViewFilterType',
    (values) => {
      const fieldType = new SingleSelectFieldType()
      const field = {}
      const result = new SingleSelectIsAnyOfViewFilterType({
        app: testApp._app,
      }).matches(values.rowValue, values.filterValue, field, fieldType)
      expect(result).toBe(values.is_any_of)
    }
  )

  test.each(singleSelectValuesInFilterCases)(
    'SingleSelectIsNoneOfViewFilterType',
    (values) => {
      const fieldType = new SingleSelectFieldType()
      const field = {}
      const result = new SingleSelectIsNoneOfViewFilterType({
        app: testApp._app,
      }).matches(values.rowValue, values.filterValue, field, fieldType)
      expect(result).toBe(values.is_none_of)
    }
  )
})
