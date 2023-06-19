from collections import defaultdict
from datetime import date, datetime, timedelta
from decimal import Decimal
from math import ceil, floor
from typing import Any, Dict, Optional, Tuple, Union

from django.db.models import DateField, DateTimeField, IntegerField, Q
from django.db.models.functions import Extract, Length, TruncDate

import pytz
from dateutil import parser
from dateutil.relativedelta import relativedelta

from baserow.contrib.database.fields.field_filters import (
    FILTER_TYPE_AND,
    AnnotatedQ,
    FilterBuilder,
    OptionallyAnnotatedQ,
    filename_contains_filter,
)
from baserow.contrib.database.fields.field_types import (
    BooleanFieldType,
    CreatedOnFieldType,
    DateFieldType,
    EmailFieldType,
    FileFieldType,
    FormulaFieldType,
    LastModifiedFieldType,
    LinkRowFieldType,
    LongTextFieldType,
    MultipleCollaboratorsFieldType,
    MultipleSelectFieldType,
    NumberFieldType,
    PhoneNumberFieldType,
    RatingFieldType,
    SingleSelectFieldType,
    TextFieldType,
    URLFieldType,
)
from baserow.contrib.database.fields.models import Field
from baserow.contrib.database.fields.registries import field_type_registry
from baserow.contrib.database.formula import (
    BaserowFormulaBooleanType,
    BaserowFormulaCharType,
    BaserowFormulaDateType,
    BaserowFormulaNumberType,
    BaserowFormulaTextType,
)
from baserow.core.models import WorkspaceUser

from .registries import ViewFilterType

DATE_FILTER_EMPTY_VALUE = ""
DATE_FILTER_TIMEZONE_SEPARATOR = "?"


class NotViewFilterTypeMixin:
    def default_filter_on_exception(self):
        return Q()

    def get_filter(self, *args, **kwargs):
        return ~super().get_filter(*args, **kwargs)


class EqualViewFilterType(ViewFilterType):
    """
    The equal filter compared the field value to the filter value. It must be the same.
    It is compatible with models.CharField, models.TextField, models.BooleanField ('1'
    is True), models.IntegerField and models.DecimalField. It will probably also be
    compatible with other fields, but these have been tested.
    """

    type = "equal"
    compatible_field_types = [
        TextFieldType.type,
        LongTextFieldType.type,
        URLFieldType.type,
        NumberFieldType.type,
        RatingFieldType.type,
        EmailFieldType.type,
        PhoneNumberFieldType.type,
        FormulaFieldType.compatible_with_formula_types(
            BaserowFormulaTextType.type,
            BaserowFormulaCharType.type,
            BaserowFormulaNumberType.type,
        ),
    ]

    def get_filter(self, field_name, value, model_field, field):
        value = value.strip()

        # If an empty value has been provided we do not want to filter at all.
        if value == "":
            return Q()

        # Check if the model_field accepts the value.
        try:
            model_field.get_prep_value(value)
            return Q(**{field_name: value})
        except Exception:
            return self.default_filter_on_exception()


class NotEqualViewFilterType(NotViewFilterTypeMixin, EqualViewFilterType):
    type = "not_equal"


class FilenameContainsViewFilterType(ViewFilterType):
    """
    The filename contains filter checks if the filename's visible name contains the
    provided filter value. It is only compatible with fields.JSONField which contain
    a list of File JSON Objects.
    """

    type = "filename_contains"
    compatible_field_types = [FileFieldType.type]

    def get_filter(self, *args):
        return filename_contains_filter(*args)


class HasFileTypeViewFilterType(ViewFilterType):
    """
    The file field type column contains an array of objects with details related to
    the uploaded user files. Every object always contains the property `is_image`
    that indicates if the user file is an image. Using the Django contains lookup,
    we can check if there is at least one object where the `is_image` is True. If the
    filter value is `image`, there must at least be one object where the `is_image`
    is true. If the filter value is `document` there must at least be one object
    where the `is_image` is false. If an unsupported filter value is provided, we don't
    want to filter on anything.
    """

    type = "has_file_type"
    compatible_field_types = [FileFieldType.type]

    def get_filter(self, field_name, value, model_field, field):
        value = value.strip()
        is_image = value == "image"
        is_document = value == "document"

        if is_document or is_image:
            return Q(**{f"{field_name}__contains": [{"is_image": is_image}]})
        else:
            return Q()


class ContainsViewFilterType(ViewFilterType):
    """
    The contains filter checks if the field value contains the provided filter value.
    It is compatible with models.CharField and models.TextField.
    """

    type = "contains"
    compatible_field_types = [
        TextFieldType.type,
        LongTextFieldType.type,
        URLFieldType.type,
        EmailFieldType.type,
        PhoneNumberFieldType.type,
        DateFieldType.type,
        LastModifiedFieldType.type,
        CreatedOnFieldType.type,
        SingleSelectFieldType.type,
        MultipleSelectFieldType.type,
        NumberFieldType.type,
        FormulaFieldType.compatible_with_formula_types(
            BaserowFormulaTextType.type,
            BaserowFormulaCharType.type,
            BaserowFormulaNumberType.type,
            BaserowFormulaDateType.type,
        ),
    ]

    def get_filter(self, field_name, value, model_field, field) -> OptionallyAnnotatedQ:
        # Check if the model_field accepts the value.
        try:
            field_type = field_type_registry.get_by_model(field)
            return field_type.contains_query(field_name, value, model_field, field)
        except Exception:
            return self.default_filter_on_exception()


class ContainsWordViewFilterType(ViewFilterType):
    """
    The contains word filter checks if the field value contains the provided filter
    value as a whole word, and not as a substring. It is compatible with
    models.CharField and models.TextField.
    """

    type = "contains_word"
    compatible_field_types = [
        TextFieldType.type,
        LongTextFieldType.type,
        URLFieldType.type,
        EmailFieldType.type,
        SingleSelectFieldType.type,
        MultipleSelectFieldType.type,
        FormulaFieldType.compatible_with_formula_types(
            BaserowFormulaTextType.type,
            BaserowFormulaCharType.type,
        ),
    ]

    def get_filter(self, field_name, value, model_field, field) -> OptionallyAnnotatedQ:
        # Check if the model_field accepts the value.
        try:
            field_type = field_type_registry.get_by_model(field)
            return field_type.contains_word_query(field_name, value, model_field, field)
        except Exception:
            return self.default_filter_on_exception()


class DoesntContainWordViewFilterType(
    NotViewFilterTypeMixin, ContainsWordViewFilterType
):
    type = "doesnt_contain_word"


class ContainsNotViewFilterType(NotViewFilterTypeMixin, ContainsViewFilterType):
    type = "contains_not"


class LengthIsGreaterThanViewFilterType(ViewFilterType):
    """
    The length is greater than filter checks if the fields character
    length is greater than x
    """

    type = "length_is_greater_than"
    compatible_field_types = [
        TextFieldType.type,
        LongTextFieldType.type,
        URLFieldType.type,
        EmailFieldType.type,
        PhoneNumberFieldType.type,
    ]

    def get_filter(self, field_name, value, model_field, field):
        if value == 0:
            return Q()

        try:
            return AnnotatedQ(
                annotation={f"{field_name}_len": Length(field_name)},
                q={f"{field_name}_len__gt": int(value)},
            )
        except ValueError:
            return self.default_filter_on_exception()


class LengthIsLowerThanViewFilterType(ViewFilterType):
    """
    The length is lower than filter checks if the fields character
    length is less than x
    """

    type = "length_is_lower_than"
    compatible_field_types = [
        TextFieldType.type,
        LongTextFieldType.type,
        URLFieldType.type,
        EmailFieldType.type,
        PhoneNumberFieldType.type,
    ]

    def get_filter(self, field_name, value, model_field, field):
        if value == 0:
            return Q()

        try:
            return AnnotatedQ(
                annotation={f"{field_name}_len": Length(field_name)},
                q={f"{field_name}_len__lt": int(value)},
            )
        except ValueError:
            return self.default_filter_on_exception()


class HigherThanViewFilterType(ViewFilterType):
    """
    The higher than filter checks if the field value is higher than the filter value.
    It only works if a numeric number is provided. It is at compatible with
    models.IntegerField and models.DecimalField.
    """

    type = "higher_than"
    compatible_field_types = [
        NumberFieldType.type,
        RatingFieldType.type,
        FormulaFieldType.compatible_with_formula_types(
            BaserowFormulaNumberType.type,
        ),
    ]

    def get_filter(self, field_name, value, model_field, field):
        value = value.strip()

        # If an empty value has been provided we do not want to filter at all.
        if value == "":
            return Q()

        if isinstance(model_field, IntegerField) and value.find(".") != -1:
            decimal = Decimal(value)
            value = floor(decimal)

        # Check if the model_field accepts the value.
        try:
            model_field.get_prep_value(value)
            return Q(**{f"{field_name}__gt": value})
        except Exception:
            return self.default_filter_on_exception()


class LowerThanViewFilterType(ViewFilterType):
    """
    The lower than filter checks if the field value is lower than the filter value.
    It only works if a numeric number is provided. It is at compatible with
    models.IntegerField and models.DecimalField.
    """

    type = "lower_than"
    compatible_field_types = [
        NumberFieldType.type,
        RatingFieldType.type,
        FormulaFieldType.compatible_with_formula_types(
            BaserowFormulaNumberType.type,
        ),
    ]

    def get_filter(self, field_name, value, model_field, field):
        value = value.strip()

        # If an empty value has been provided we do not want to filter at all.
        if value == "":
            return Q()

        if isinstance(model_field, IntegerField) and value.find(".") != -1:
            decimal = Decimal(value)
            value = ceil(decimal)

        # Check if the model_field accepts the value.
        try:
            model_field.get_prep_value(value)
            return Q(**{f"{field_name}__lt": value})
        except Exception:
            return self.default_filter_on_exception()


class TimezoneAwareDateViewFilterType(ViewFilterType):
    compatible_field_types = [
        DateFieldType.type,
        LastModifiedFieldType.type,
        CreatedOnFieldType.type,
        FormulaFieldType.compatible_with_formula_types(BaserowFormulaDateType.type),
    ]

    def is_empty_filter(self, filter_value: str) -> bool:
        return filter_value == DATE_FILTER_EMPTY_VALUE

    def get_filter_date(
        self, filter_value: str, timezone: pytz.BaseTzInfo
    ) -> Union[datetime, date]:
        """
        Parses the provided filter value and returns a date or datetime object
        that can be used to compare with the field value.

        :param filter_value: The value that has been provided by the user.
        :param timezone: The timezone that should be used to convert the date to
            an aware date.
        :raises ValueError: If the provided value is not valid.
        :raise OverflowError: If the provided value is out of range.
        :raise ParserError: If the provided value is not a valid date to parse.
        :return: a date or an aware datetime that should be used to compare with
            the field value.
        """

        try:
            return parser.isoparser().parse_isodate(filter_value)
        except ValueError:
            datetime_value = parser.isoparse(filter_value)
            if datetime_value.tzinfo is None:
                return timezone.localize(datetime_value)
            return datetime_value.astimezone(timezone)

    def get_filter_query_dict(
        self, field_name: str, aware_filter_date: Union[datetime, date], now: datetime
    ) -> Dict:
        """
        Returns a dictionary that can be used to create a Q object.

        :param field_name: The name of the field that should be used in the
            query.
        :param aware_filter_date: The date that should be used to compare with
            the field value.
        :param now: The current aware datetime that can be used to compare with
            the field value.
        """

        raise NotImplementedError()

    def _split_optional_timezone_and_filter_value(
        self, field, filter_value, separator
    ) -> Tuple[Optional[str], Optional[str]]:
        if separator in filter_value:  # specific timezone provided by the filter
            try:
                timezone_value, filter_value = filter_value.split(separator)
                return timezone_value, filter_value
            except ValueError:
                # the separator was included multiple times, we don't know what to do
                return None, None
        elif filter_value in pytz.all_timezones:
            # only a timezone value was provided with no filter value
            return filter_value, None
        else:
            # default to the fields timezone if any and the provided value
            return field.date_force_timezone, filter_value

    def split_timezone_and_filter_value(
        self, field, filter_value, separator=DATE_FILTER_TIMEZONE_SEPARATOR
    ) -> Tuple[pytz.BaseTzInfo, str]:
        """
        Splits the timezone and the value from the provided value. If the value
        does not contain a timezone then the default timezone will be used.

        :param field: The field that is being filtered.
        :param filter_value: The value that has been provided by the user.
        :param separator: The separator that is used to split the timezone and
            the value.
        :return: A tuple containing the timezone and the filter_value string.
        """

        (
            user_timezone_str,
            parsed_filter_value,
        ) = self._split_optional_timezone_and_filter_value(
            field, filter_value, separator
        )

        python_timezone = (
            pytz.timezone(user_timezone_str)
            if user_timezone_str is not None
            else pytz.UTC
        )

        validated_filter_value = (
            parsed_filter_value
            if parsed_filter_value is not None
            else DATE_FILTER_EMPTY_VALUE
        )

        return python_timezone, validated_filter_value

    def get_filter(
        self, field_name: str, value: str, model_field, field: Field
    ) -> Union[Q, AnnotatedQ]:
        """
        Returns a Q object that can be used to filter the provided field.

        :param field_name: The name of the field that should be used in the
            query.
        :param value: The value that has been provided by the user.
        :param model_field: The Django model field of the database table that is
            being filtered.
        :param field: The Baserow field instance containing the metadata related
            to the field.
        :return: A Q object that can be used to filter the provided field.
        """

        try:
            timezone, filter_value = self.split_timezone_and_filter_value(
                field, value.strip()
            )
            if self.is_empty_filter(filter_value):
                return Q()

            filter_date = self.get_filter_date(filter_value, timezone)
        except (
            OverflowError,
            ValueError,
            parser.ParserError,
            pytz.UnknownTimeZoneError,
        ):
            return Q(pk__in=[])

        annotation = {}
        query_field_name = field_name

        if isinstance(model_field, DateTimeField):
            if not isinstance(filter_date, datetime):
                query_field_name = f"{field_name}_tzdate"
                annotation[query_field_name] = TruncDate(field_name, tzinfo=timezone)

        elif isinstance(model_field, DateField) and isinstance(filter_date, datetime):
            filter_date = filter_date.date()

        query_dict = {
            f"{field_name}__isnull": False,  # makes `NotViewFilterTypeMixin` work with timezones
            **self.get_filter_query_dict(
                query_field_name, filter_date, datetime.now(timezone)
            ),
        }
        return AnnotatedQ(annotation=annotation, q=query_dict)


class DateEqualViewFilterType(TimezoneAwareDateViewFilterType):
    """
    The date filter parses the provided value as date and checks if the field value is
    the same date. It only works if a valid ISO date is provided as value and it is
    only compatible with models.DateField and models.DateTimeField.
    """

    type = "date_equal"

    def get_filter_query_dict(
        self, field_name: str, aware_filter_date: Union[date, datetime], now: datetime
    ) -> Dict:
        return {field_name: aware_filter_date}


class DateBeforeViewFilterType(TimezoneAwareDateViewFilterType):
    """
    The date before filter parses the provided filter value as date and checks if the
    field value is before this date (lower than).
    It is an extension of the BaseDateFieldLookupFilter
    """

    type = "date_before"

    def get_filter_query_dict(
        self, field_name: str, aware_filter_date: Union[date, datetime], now: datetime
    ) -> Dict[str, Any]:
        return {f"{field_name}__lt": aware_filter_date}


class DateBeforeOrEqualViewFilterType(TimezoneAwareDateViewFilterType):
    """
    This filter parses the provided value as date and checks if the field value
    is before or equal.
    """

    type = "date_before_or_equal"

    def get_filter_query_dict(
        self, field_name: str, aware_filter_date: Union[date, datetime], now: datetime
    ) -> Dict[str, Any]:
        return {f"{field_name}__lte": aware_filter_date}


class DateAfterViewFilterType(TimezoneAwareDateViewFilterType):
    """
    The after date filter parses the provided filter value as date and checks if
    the field value is after this date (greater than).
    It is an extension of the BaseDateFieldLookupFilter
    """

    type = "date_after"

    def get_filter_query_dict(
        self, field_name: str, aware_filter_date: Union[date, datetime], now: datetime
    ) -> Dict[str, Any]:
        return {f"{field_name}__gt": aware_filter_date}


class DateAfterOrEqualViewFilterType(TimezoneAwareDateViewFilterType):
    """
    This filter parses the provided value as date and checks if the field value
    is after or equal.
    """

    type = "date_after_or_equal"

    def get_filter_query_dict(
        self, field_name: str, aware_filter_date: Union[date, datetime], now: datetime
    ) -> Dict[str, Any]:
        return {f"{field_name}__gte": aware_filter_date}


class DateEqualsDayOfMonthViewFilterType(TimezoneAwareDateViewFilterType):
    """
    The day of month filter checks if the field number value
    matches the date's day of the month value.
    """

    type = "date_equals_day_of_month"

    def get_filter(
        self, field_name: str, value: str, model_field, field: Field
    ) -> Union[Q, AnnotatedQ]:
        try:
            timezone, filter_value = self.split_timezone_and_filter_value(
                field, value.strip()
            )
            if self.is_empty_filter(filter_value):
                return Q()

            day_of_month = int(filter_value)
            if day_of_month < 1 or day_of_month > 31:
                raise ValueError

        except (ValueError, pytz.UnknownTimeZoneError):
            return Q(pk__in=[])

        if field.date_include_time:  # filter on a datetime field
            annotated_field_name = f"{field_name}_day_of_month_tz"
            return AnnotatedQ(
                annotation={annotated_field_name: Extract(field_name, "day", timezone)},
                q={annotated_field_name: day_of_month},
            )
        else:  # filter on a date field
            return Q(**{f"{field_name}__day": day_of_month})


class EmptyFilterValueMixin:
    def is_empty_filter(self, filter_value: str) -> bool:
        return False


class DateEqualsTodayViewFilterType(
    EmptyFilterValueMixin, TimezoneAwareDateViewFilterType
):
    """
    The today filter checks if the field value matches with today's date.
    """

    type = "date_equals_today"

    def get_filter_date(
        self, filter_value: str, timezone: pytz.BaseTzInfo
    ) -> Union[datetime, date]:
        return datetime.now(tz=timezone).date()

    def get_filter_query_dict(
        self, field_name: str, aware_filter_date: Union[date, datetime], now: datetime
    ) -> Dict:
        return {field_name: aware_filter_date}


class DateBeforeTodayViewFilterType(
    EmptyFilterValueMixin, TimezoneAwareDateViewFilterType
):
    """
    The before today filter checks if the field value is before today's date.
    """

    type = "date_before_today"

    def get_filter_date(
        self, filter_value: str, timezone: pytz.BaseTzInfo
    ) -> Union[datetime, date]:
        return (datetime.now(tz=timezone) - timedelta(days=1)).date()

    def get_filter_query_dict(
        self, field_name: str, aware_filter_date: Union[date, datetime], now: datetime
    ) -> Dict:
        return {f"{field_name}__lte": aware_filter_date}


class DateAfterTodayViewFilterType(
    EmptyFilterValueMixin, TimezoneAwareDateViewFilterType
):
    """
    The after today filter checks if the field value is after today's date.
    """

    type = "date_after_today"

    def get_filter_date(
        self, filter_value: str, timezone: pytz.BaseTzInfo
    ) -> Union[datetime, date]:
        return (datetime.now(tz=timezone) + timedelta(days=1)).date()

    def get_filter_query_dict(
        self, field_name: str, aware_filter_date: Union[date, datetime], now: datetime
    ) -> Dict:
        return {f"{field_name}__gte": aware_filter_date}


class DateEqualsCurrentWeekViewFilterType(
    EmptyFilterValueMixin, TimezoneAwareDateViewFilterType
):
    """
    The current week filter works as a subset of today filter and checks if the
    field value falls into current week.
    """

    type = "date_equals_week"

    def get_filter_date(
        self, filter_value: str, timezone: pytz.BaseTzInfo
    ) -> Union[datetime, date]:
        return datetime.now(tz=timezone).date()

    def get_filter_query_dict(
        self, field_name: str, aware_filter_date: Union[date, datetime], now: datetime
    ) -> Dict:
        week_of_year = aware_filter_date.isocalendar().week
        return {
            f"{field_name}__week": week_of_year,
            f"{field_name}__year": aware_filter_date.year,
        }


class DateEqualsCurrentMonthViewFilterType(
    EmptyFilterValueMixin, TimezoneAwareDateViewFilterType
):
    """
    The current month filter works as a subset of today filter and checks if the
    field value falls into current month.
    """

    type = "date_equals_month"

    def get_filter_date(
        self, filter_value: str, timezone: pytz.BaseTzInfo
    ) -> Union[datetime, date]:
        return datetime.now(tz=timezone).date()

    def get_filter_query_dict(
        self, field_name: str, aware_filter_date: Union[date, datetime], now: datetime
    ) -> Dict:
        return {
            f"{field_name}__month": aware_filter_date.month,
            f"{field_name}__year": aware_filter_date.year,
        }


class DateEqualsCurrentYearViewFilterType(
    EmptyFilterValueMixin, TimezoneAwareDateViewFilterType
):
    """
    The current month filter works as a subset of today filter and checks if the
    field value falls into current year.
    """

    type = "date_equals_year"

    def get_filter_date(
        self, filter_value: str, timezone: pytz.BaseTzInfo
    ) -> Union[datetime, date]:
        return datetime.now(tz=timezone).date()

    def get_filter_query_dict(
        self, field_name: str, aware_filter_date: Union[date, datetime], now: datetime
    ) -> Dict:
        return {f"{field_name}__year": aware_filter_date.year}


def get_is_within_filter_query_dict(
    field_name: str, aware_filter_date: Union[date, datetime], now: datetime
) -> Dict:
    """
    The utility function checks if the field value is between today's date and
    the date specified in the filter value and returns the query dict.
    It ensure that the filter works correctly even if the filter date is before
    today's date.
    """

    op1, op2 = ("lte", "gte") if aware_filter_date >= now.date() else ("gte", "lte")

    return {
        f"{field_name}__{op1}": aware_filter_date,
        f"{field_name}__{op2}": now.date(),
    }


class DateIsWithinXDaysViewFilterType(TimezoneAwareDateViewFilterType):
    """
    Is within X days filter checks if the field value is between today's date
    and the number of days specified in the filter.

    The value of the filter is expected to be a string like "Europe/Rome?1". It
    uses character ? as separator between the timezone and the number of days.
    """

    type = "date_within_days"

    def get_filter_date(
        self, filter_value: str, timezone: pytz.BaseTzInfo
    ) -> Union[datetime, date]:
        """
        Zero days means today, one day means today and tomorrow, and so on.
        """

        number_of_days = int(filter_value)

        filter_date = datetime.now(tz=timezone) + relativedelta(days=number_of_days)
        return filter_date.date()

    def get_filter_query_dict(
        self, field_name: str, aware_filter_date: Union[date, datetime], now: datetime
    ) -> Dict:
        return get_is_within_filter_query_dict(field_name, aware_filter_date, now)


class DateIsWithinXWeeksViewFilterType(TimezoneAwareDateViewFilterType):
    """
    Is within X weeks filter checks if the field value is between today's date
    and the number of weeks specified in the filter.

    The value of the filter is expected to be a string like "Europe/Rome?1". It
    uses character ? as separator between the timezone and the number of days.
    """

    type = "date_within_weeks"

    def get_filter_date(
        self, filter_value: str, timezone: pytz.BaseTzInfo
    ) -> Union[datetime, date]:
        """
        Since zero weeks can be confusing, we raise an error if the number of
        weeks is 0. One week means today + 1 week inclusive, and so on.
        """

        number_of_weeks = int(filter_value)
        if number_of_weeks == 0:
            raise ValueError("Number of weeks cannot be 0")

        filter_date = datetime.now(tz=timezone) + relativedelta(weeks=number_of_weeks)
        return filter_date.date()

    def get_filter_query_dict(
        self, field_name: str, aware_filter_date: Union[date, datetime], now: datetime
    ) -> Dict:
        return get_is_within_filter_query_dict(field_name, aware_filter_date, now)


class DateIsWithinXMonthsViewFilterType(TimezoneAwareDateViewFilterType):
    """
    Is within X months filter checks if the field value is between today's date
    and the number of months specified in the filter.

    The value of the filter is expected to be a string like "Europe/Rome?1". It
    uses character ? as separator between the timezone and the number of days.
    """

    type = "date_within_months"

    def get_filter_date(
        self, filter_value: str, timezone: pytz.BaseTzInfo
    ) -> Union[datetime, date]:
        """
        Since zero months can be confusing, we raise an error if the number of
        months is 0. One month means today + 1 month inclusive, and so on. E.g.
        if today is 2023-01-31, within 1 month means within 2020-02-28
        inclusive.
        """

        number_of_months = int(filter_value)
        if number_of_months == 0:
            raise ValueError("Number of months cannot be 0")

        filter_date = datetime.now(tz=timezone) + relativedelta(months=number_of_months)
        return filter_date.date()

    def get_filter_query_dict(
        self, field_name: str, aware_filter_date: Union[date, datetime], now: datetime
    ) -> Dict:
        return get_is_within_filter_query_dict(field_name, aware_filter_date, now)


class DateEqualsDaysAgoViewFilterType(TimezoneAwareDateViewFilterType):
    """
    The "number of days ago" filter checks if the field value matches with today's
    date minus the specified number of days.

    The value of the filter is expected to be a string like "Europe/Rome?1".
    It uses character ? as separator between the timezone and the number of days.
    """

    type = "date_equals_days_ago"

    def get_filter_date(
        self, filter_value: str, timezone: pytz.BaseTzInfo
    ) -> Union[datetime, date]:
        filter_date = datetime.now(tz=timezone) - timedelta(days=int(filter_value))
        return filter_date.date()

    def get_filter_query_dict(
        self, field_name: str, aware_filter_date: Union[date, datetime], now: datetime
    ) -> Dict:
        return {field_name: aware_filter_date}


class DateEqualsMonthsAgoViewFilterType(TimezoneAwareDateViewFilterType):
    """
    The "number of months ago" filter checks if the field value's month is within
    the specified "months ago" based on the current date.

    The value of the filter is expected to be a string like "Europe/Rome?1".
    It uses character ? as separator between the timezone and the number of months.
    """

    type = "date_equals_months_ago"

    def get_filter_date(
        self, filter_value: str, timezone: pytz.BaseTzInfo
    ) -> Union[datetime, date]:
        filter_date = datetime.now(tz=timezone) + relativedelta(
            months=-int(filter_value)
        )
        return filter_date.date()

    def get_filter_query_dict(
        self, field_name: str, aware_filter_date: Union[date, datetime], now: datetime
    ) -> Dict:
        return {
            f"{field_name}__year": aware_filter_date.year,
            f"{field_name}__month": aware_filter_date.month,
        }


class DateEqualsYearsAgoViewFilterType(TimezoneAwareDateViewFilterType):
    """
    The "is years ago" filter checks if the field value's year is within
    the specified "years ago" based on the current date.

    The value of the filter is expected to be a string like "Europe/Rome?1".
    It uses character ? as separator between the timezone and the number of months.
    """

    type = "date_equals_years_ago"

    def get_filter_date(
        self, filter_value: str, timezone: pytz.BaseTzInfo
    ) -> Union[datetime, date]:
        filter_date = datetime.now(tz=timezone) + relativedelta(
            years=-int(filter_value)
        )
        return filter_date.date()

    def get_filter_query_dict(
        self, field_name: str, aware_filter_date: Union[date, datetime], now: datetime
    ) -> Dict:
        return {f"{field_name}__year": aware_filter_date.year}


class DateNotEqualViewFilterType(NotViewFilterTypeMixin, DateEqualViewFilterType):
    type = "date_not_equal"


class SingleSelectEqualViewFilterType(ViewFilterType):
    """
    The single select equal filter accepts a select option id as filter value. This
    filter is only compatible with the SingleSelectFieldType field type.
    """

    type = "single_select_equal"
    compatible_field_types = [SingleSelectFieldType.type]

    def get_filter(self, field_name, value, model_field, field):
        value = value.strip()

        if value == "":
            return Q()

        try:
            int(value)
            return Q(**{f"{field_name}_id": value})
        except Exception:
            return Q()

    def set_import_serialized_value(self, value, id_mapping):
        try:
            value = int(value)
        except ValueError:
            return ""

        return str(id_mapping["database_field_select_options"].get(value, ""))


class SingleSelectNotEqualViewFilterType(
    NotViewFilterTypeMixin, SingleSelectEqualViewFilterType
):
    type = "single_select_not_equal"


class BooleanViewFilterType(ViewFilterType):
    """
    The boolean filter tries to convert the provided filter value to a boolean and
    compares that to the field value. If for example '1' is provided then only field
    value with True are going to be matched. This filter is compatible with
    models.BooleanField.
    """

    type = "boolean"
    compatible_field_types = [
        BooleanFieldType.type,
        FormulaFieldType.compatible_with_formula_types(
            BaserowFormulaBooleanType.type,
        ),
    ]

    def get_filter(self, field_name, value, model_field, field):
        value = value.strip().lower()
        value = value in [
            "y",
            "t",
            "o",
            "yes",
            "true",
            "on",
            "1",
        ]

        # Check if the model_field accepts the value.
        # noinspection PyBroadException
        try:
            model_field.get_prep_value(value)
            return Q(**{field_name: value})
        except Exception:
            return Q()


class ManyToManyHasBaseViewFilter(ViewFilterType):
    """
    The many to many base filter accepts a relationship ID. It filters the queryset so
    that only rows that have a relationship with the provided ID will remain. So if for
    example '10' is provided, then only rows where the many to many field has a
    relationship to a foreignkey with the ID of 10.
    """

    def get_filter(self, field_name, value, model_field, field):
        value = value.strip()

        try:
            remote_field = model_field.remote_field
            remote_model = remote_field.model
            return Q(
                **{
                    "id__in": remote_model.objects.filter(
                        **{"id": int(value)}
                    ).values_list(f"{remote_field.related_name}__id", flat=True)
                }
            )
        except ValueError:
            return Q()


class LinkRowHasViewFilterType(ManyToManyHasBaseViewFilter):
    """
    The link row has filter accepts the row ID of the related table as value.
    """

    type = "link_row_has"
    compatible_field_types = [LinkRowFieldType.type]

    def get_preload_values(self, view_filter):
        """
        This method preloads the display name of the related value. This prevents a
        lot of API requests if the view has a lot of `link_row_has` filters. It will
        also make sure that the display name is visible for read only previews.
        """

        name = None
        related_row_id = None

        try:
            related_row_id = int(view_filter.value)
        except ValueError:
            pass

        if related_row_id:
            field = view_filter.field.specific
            table = field.link_row_table
            primary_field = table.field_set.get(primary=True)
            model = table.get_model(
                field_ids=[], fields=[primary_field], add_dependencies=False
            )

            try:
                name = str(model.objects.get(pk=related_row_id))
            except model.DoesNotExist:
                pass

        return {"display_name": name}


class LinkRowHasNotViewFilterType(NotViewFilterTypeMixin, LinkRowHasViewFilterType):
    """
    The link row has filter accepts the row ID of the related table as value. It
    filters the queryset so that only rows that don't have a relationship with the
    provided row ID will remain. So if for example '10' is provided, then only rows
    where the link row field does not have a relationship with the row '10' persists.
    """

    type = "link_row_has_not"


class LinkRowContainsViewFilterType(ViewFilterType):
    type = "link_row_contains"
    compatible_field_types = [LinkRowFieldType.type]

    def get_filter(self, field_name, value, model_field, field) -> OptionallyAnnotatedQ:
        related_primary_field = field.get_related_primary_field().specific
        related_primary_field_type = field_type_registry.get_by_model(
            related_primary_field
        )
        model = field.table.get_model()
        related_primary_field_model_field = related_primary_field_type.get_model_field(
            related_primary_field
        )

        subquery = (
            FilterBuilder(FILTER_TYPE_AND)
            .filter(
                related_primary_field_type.contains_query(
                    f"{field_name}__{related_primary_field.db_column}",
                    value,
                    related_primary_field_model_field,
                    related_primary_field,
                )
            )
            .apply_to_queryset(model.objects)
            .values_list("id", flat=True)
        )

        return Q(
            **{f"id__in": subquery},
        )


class LinkRowNotContainsViewFilterType(
    NotViewFilterTypeMixin, LinkRowContainsViewFilterType
):
    type = "link_row_not_contains"

    def get_filter(self, field_name, value, model_field, field) -> OptionallyAnnotatedQ:
        if value == "":
            return Q()

        return super().get_filter(field_name, value, model_field, field)


class MultipleSelectHasViewFilterType(ManyToManyHasBaseViewFilter):
    """
    The multiple select has filter accepts the ID of the select_option to filter for
    and filters the rows where the multiple select field has the provided select_option.
    """

    type = "multiple_select_has"
    compatible_field_types = [MultipleSelectFieldType.type]

    def set_import_serialized_value(self, value, id_mapping):
        try:
            value = int(value)
        except ValueError:
            return ""

        return str(id_mapping["database_field_select_options"].get(value, ""))


class MultipleSelectHasNotViewFilterType(
    NotViewFilterTypeMixin, MultipleSelectHasViewFilterType
):
    """
    The multiple select has filter accepts the ID of the select_option to filter for
    and filters the rows where the multiple select field does not have the provided
    select_option.
    """

    type = "multiple_select_has_not"


class MultipleCollaboratorsHasViewFilterType(ManyToManyHasBaseViewFilter):
    """
    The multiple collaborators has filter accepts the ID of the user to filter for
    and filters the rows where the multiple collaborators field has the provided user.
    """

    type = "multiple_collaborators_has"
    compatible_field_types = [MultipleCollaboratorsFieldType.type]

    COLLABORATORS_KEY = f"available_collaborators"

    def get_export_serialized_value(self, value, id_mapping):
        if self.COLLABORATORS_KEY not in id_mapping:
            workspace_id = id_mapping.get("workspace_id", None)
            if workspace_id is None:
                return value

            id_mapping[self.COLLABORATORS_KEY] = defaultdict(list)

            workspaceusers_from_workspace = WorkspaceUser.objects.filter(
                workspace_id=workspace_id
            ).select_related("user")

            for workspaceuser in workspaceusers_from_workspace:
                id_mapping[self.COLLABORATORS_KEY][
                    str(workspaceuser.user.id)
                ] = workspaceuser.user.email

        return id_mapping[self.COLLABORATORS_KEY].get(value, "")

    def set_import_serialized_value(self, value, id_mapping):
        workspace_id = id_mapping.get("workspace_id", None)
        if workspace_id is None:
            return ""

        if self.COLLABORATORS_KEY not in id_mapping:
            id_mapping[self.COLLABORATORS_KEY] = defaultdict(list)
            workspaceusers_from_workspace = WorkspaceUser.objects.filter(
                workspace_id=workspace_id
            ).select_related("user")
            for workspaceuser in workspaceusers_from_workspace:
                id_mapping[self.COLLABORATORS_KEY][str(workspaceuser.user.email)] = str(
                    workspaceuser.user.id
                )
        return id_mapping[self.COLLABORATORS_KEY].get(value, "")


class MultipleCollaboratorsHasNotViewFilterType(
    NotViewFilterTypeMixin, MultipleCollaboratorsHasViewFilterType
):
    """
    The multiple collaborators has not filter accepts the ID of the user to filter for
    and filters the rows where the field does not have the provided user.
    """

    type = "multiple_collaborators_has_not"


class EmptyViewFilterType(ViewFilterType):
    """
    The empty filter checks if the field value is empty, this can be '', null,
    [] or anything. It is compatible with all fields
    """

    type = "empty"
    compatible_field_types = [
        TextFieldType.type,
        LongTextFieldType.type,
        URLFieldType.type,
        NumberFieldType.type,
        RatingFieldType.type,
        BooleanFieldType.type,
        DateFieldType.type,
        LastModifiedFieldType.type,
        CreatedOnFieldType.type,
        LinkRowFieldType.type,
        EmailFieldType.type,
        FileFieldType.type,
        SingleSelectFieldType.type,
        PhoneNumberFieldType.type,
        MultipleSelectFieldType.type,
        MultipleCollaboratorsFieldType.type,
        FormulaFieldType.compatible_with_formula_types(
            BaserowFormulaTextType.type,
            BaserowFormulaCharType.type,
            BaserowFormulaNumberType.type,
            BaserowFormulaDateType.type,
            BaserowFormulaBooleanType.type,
        ),
    ]

    def get_filter(self, field_name, value, model_field, field):
        field_type = field_type_registry.get_by_model(field)

        return field_type.empty_query(field_name, model_field, field)


class NotEmptyViewFilterType(NotViewFilterTypeMixin, EmptyViewFilterType):
    type = "not_empty"
