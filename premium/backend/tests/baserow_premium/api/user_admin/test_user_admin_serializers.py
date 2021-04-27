from baserow.api.utils import validate_data
from baserow_premium.api.user_admin.serializers import AdminUserSerializer


def test_serializer_accepts_single_fields_to_update():
    username = "email@address.com"
    data = validate_data(
        AdminUserSerializer, {"id": 1, "username": username}, partial=True
    )
    assert data["username"] == username


def test_serializer_accepts_password_but_does_not_return_it():
    password = "abcdefghijk"
    data = validate_data(
        AdminUserSerializer, {"id": 1, "password": password}, partial=True
    )
    assert data == {}
