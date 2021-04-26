import pytest

from baserow.api.utils import validate_data
from baserow_premium.api.user_admin.serializers import PartialAdminUserSerializer


@pytest.mark.django_db
def test_serializer():
    username = "email@address.com"
    data = validate_data(
        PartialAdminUserSerializer, {"id": 1, "username": username}, partial=True
    )
    assert data["username"] == username
    password = "abcdefghijk"
    data = validate_data(
        PartialAdminUserSerializer, {"id": 1, "password": password}, partial=True
    )
    assert data == {}
