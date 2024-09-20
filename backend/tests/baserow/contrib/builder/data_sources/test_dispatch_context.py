from unittest.mock import MagicMock, PropertyMock, patch

from django.http import HttpRequest

import pytest
from rest_framework.request import Request

from baserow.contrib.builder.data_sources.builder_dispatch_context import (
    FEATURE_FLAG_EXCLUDE_UNUSED_FIELDS,
    BuilderDispatchContext,
)


def test_dispatch_context_page_range():
    request = MagicMock()
    request.GET = {"offset": 42, "count": 42}

    dispatch_context = BuilderDispatchContext(request, None)

    assert dispatch_context.range(None) == [42, 42]

    request.GET = {"offset": "foo", "count": "bar"}

    dispatch_context = BuilderDispatchContext(request, None)

    assert dispatch_context.range(None) == [0, 20]

    request.GET = {"offset": "-20", "count": "-10"}

    dispatch_context = BuilderDispatchContext(request, None)

    assert dispatch_context.range(None) == [0, 1]


def test_dispatch_context_search_query():
    request = HttpRequest()
    request.GET["search_query"] = "foobar"
    dispatch_context = BuilderDispatchContext(request, None)
    assert dispatch_context.search_query() == "foobar"


def test_dispatch_context_filters():
    request = HttpRequest()
    filter_data = {
        "groups": [],
        "filter_type": "AND",
        "filters": [
            {
                "field": 123,
                "type": "contains",
                "value": "Alexa",
            }
        ],
    }
    request.GET["filters"] = filter_data
    dispatch_context = BuilderDispatchContext(request, None)
    assert dispatch_context.filters() == filter_data


def test_dispatch_context_sortings():
    request = HttpRequest()
    request.GET["order_by"] = "-field_1,-field_2"
    dispatch_context = BuilderDispatchContext(request, None)
    assert dispatch_context.sortings() == "-field_1,-field_2"


@pytest.mark.django_db
@patch(
    "baserow.contrib.builder.data_sources.builder_dispatch_context.get_formula_field_names"
)
def test_dispatch_context_page_from_context(mock_get_field_names, data_fixture):
    mock_get_field_names.return_value = {"all": {}, "external": {}, "internal": {}}

    user = data_fixture.create_user()
    page = data_fixture.create_builder_page(user=user)
    request = Request(HttpRequest())
    request.user = user

    dispatch_context = BuilderDispatchContext(
        request, page, offset=0, count=5, use_field_names=True
    )
    dispatch_context.annotated_data = "foobar"

    dispatch_context.cache = {"key": "value"}
    new_dispatch_context = BuilderDispatchContext.from_context(
        dispatch_context, offset=5, count=1
    )
    assert getattr(new_dispatch_context, "annotated_data", None) is None
    assert new_dispatch_context.cache == {"key": "value"}
    assert new_dispatch_context.request == request
    assert new_dispatch_context.page == page
    assert new_dispatch_context.offset == 5
    assert new_dispatch_context.count == 1
    assert new_dispatch_context.field_names == {
        "all": {},
        "external": {},
        "internal": {},
    }


@pytest.mark.parametrize(
    "feature_flag_is_set,use_field_names",
    (
        [False, True],
        [True, True],
        [False, False],
        [True, False],
    ),
)
@patch(
    "baserow.contrib.builder.data_sources.builder_dispatch_context.get_formula_field_names"
)
@patch("baserow.contrib.builder.data_sources.builder_dispatch_context.settings")
def test_builder_dispatch_context_field_names_computed_on_feature_flag(
    mock_settings, mock_get_formula_field_names, feature_flag_is_set, use_field_names
):
    """
    Test the BuilderDispatchContext::field_names property.

    Ensure that the field_names property is computed only when the feature
    flag is on.
    """

    feature_flags = []
    if feature_flag_is_set:
        feature_flags.append(FEATURE_FLAG_EXCLUDE_UNUSED_FIELDS)

    # The override_settings() helper doesn't seem to work in this case, so this
    # manually mocks out the FEATURE_FLAGS config.
    type(mock_settings).FEATURE_FLAGS = PropertyMock(return_value=feature_flags)

    mock_field_names = MagicMock()
    mock_get_formula_field_names.return_value = mock_field_names

    mock_request = MagicMock()
    mock_page = MagicMock()

    dispatch_context = BuilderDispatchContext(
        mock_request, mock_page, use_field_names=use_field_names
    )

    if feature_flag_is_set and use_field_names:
        assert dispatch_context.field_names == mock_field_names
        mock_get_formula_field_names.assert_called_once_with(
            mock_request.user, mock_page
        )
    else:
        assert dispatch_context.field_names is None
        mock_get_formula_field_names.assert_not_called()
