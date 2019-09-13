import pytest

from rest_framework import status
from rest_framework.exceptions import APIException

from baserow.api.v0.decorators import map_exceptions


class TemporaryException(Exception):
    pass


def test_map_exceptions():
    @map_exceptions({
        TemporaryException: 'ERROR_TEMPORARY'
    })
    def test_1():
        raise TemporaryException

    with pytest.raises(APIException) as api_exception_1:
        test_1()

    assert api_exception_1.value.detail['error'] == 'ERROR_TEMPORARY'
    assert api_exception_1.value.detail['detail'] == ''
    assert api_exception_1.value.status_code == status.HTTP_400_BAD_REQUEST

    @map_exceptions({
        TemporaryException: ('ERROR_TEMPORARY_2', 404, 'Another message')
    })
    def test_2():
        raise TemporaryException

    with pytest.raises(APIException) as api_exception_2:
        test_2()

    assert api_exception_2.value.detail['error'] == 'ERROR_TEMPORARY_2'
    assert api_exception_2.value.detail['detail'] == 'Another message'
    assert api_exception_2.value.status_code == status.HTTP_404_NOT_FOUND

    @map_exceptions({
        TemporaryException: 'ERROR_TEMPORARY_3'
    })
    def test_3():
        pass

    test_3()
