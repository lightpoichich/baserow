from django.db import transaction
from itsdangerous.exc import BadSignature, SignatureExpired

from django.conf import settings

from drf_spectacular.utils import extend_schema

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.views import (
    ObtainJSONWebToken as RegularObtainJSONWebToken,
    RefreshJSONWebToken as RegularRefreshJSONWebToken,
    VerifyJSONWebToken as RegularVerifyJSONWebToken
)

from baserow.api.decorators import map_exceptions, validate_body
from baserow.api.errors import BAD_TOKEN_SIGNATURE, EXPIRED_TOKEN_SIGNATURE
from baserow.api.schemas import get_error_schema
from baserow.core.user.handler import UserHandler
from baserow.core.user.exceptions import (
    UserAlreadyExist, UserNotFound, InvalidPassword
)

from .serializers import (
    RegisterSerializer, UserSerializer, SendResetPasswordEmailBodyValidationSerializer,
    ResetPasswordBodyValidationSerializer, ChangePasswordBodyValidationSerializer,
    NormalizedEmailWebTokenSerializer,
)
from .errors import (
    ERROR_ALREADY_EXISTS, ERROR_USER_NOT_FOUND, ERROR_INVALID_OLD_PASSWORD
)
from .schemas import create_user_response_schema, authenticate_user_schema


jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class ObtainJSONWebToken(RegularObtainJSONWebToken):
    """
    A slightly modified version of the ObtainJSONWebToken that uses an email as
    username and normalizes that email address using the normalize_email_address
    utility function.
    """

    serializer_class = NormalizedEmailWebTokenSerializer

    @extend_schema(
        tags=['User'],
        operation_id='token_auth',
        description=(
            'Authenticates an existing user based on their username, which is their '
            'email address, and their password. If successful a JWT token will be '
            'generated that can be used to authorize for other endpoints that require '
            'authorization. The token will be valid for {valid} minutes, so it has to '
            'be refreshed using the **token_refresh** endpoint before that '
            'time.'.format(
                valid=int(settings.JWT_AUTH['JWT_EXPIRATION_DELTA'].seconds / 60)
            )
        ),
        responses={
            200: authenticate_user_schema,
            400: {
                'description': 'A user with the provided username and password is '
                               'not found.'
            }
        },
        auth=[None]
    )
    def post(self, *args, **kwargs):
        return super().post(*args, **kwargs)


class RefreshJSONWebToken(RegularRefreshJSONWebToken):
    @extend_schema(
        tags=['User'],
        operation_id='token_refresh',
        description=(
            'Refreshes an existing JWT token. If the the token is valid, a new '
            'token will be included in the response. It will be valid for {valid} '
            'minutes.'.format(
                valid=int(settings.JWT_AUTH['JWT_EXPIRATION_DELTA'].seconds / 60)
            )
        ),
        responses={
            200: authenticate_user_schema,
            400: {'description': 'The token is invalid or expired.'}
        },
        auth=[None]
    )
    def post(self, *args, **kwargs):
        return super().post(*args, **kwargs)


class VerifyJSONWebToken(RegularVerifyJSONWebToken):
    @extend_schema(
        tags=['User'],
        operation_id='token_verify',
        description='Verifies if the a token is still valid.',
        responses={
            200: authenticate_user_schema,
            400: {'description': 'The token is invalid or expired.'}
        },
        auth=[None]
    )
    def post(self, *args, **kwargs):
        return super().post(*args, **kwargs)


class UserView(APIView):
    permission_classes = (AllowAny,)

    @extend_schema(
        tags=['User'],
        request=RegisterSerializer,
        operation_id='create_user',
        description=(
            'Creates a new user based on the provided values. If desired an '
            'authentication token can be generated right away. After creating an '
            'account the initial group containing a database is created.'
        ),
        responses={
            200: create_user_response_schema,
            400: get_error_schema([
                'ERROR_ALREADY_EXISTS',
                'ERROR_REQUEST_BODY_VALIDATION'
            ])
        },
        auth=[None]
    )
    @transaction.atomic
    @map_exceptions({
        UserAlreadyExist: ERROR_ALREADY_EXISTS
    })
    @validate_body(RegisterSerializer)
    def post(self, request, data):
        """Registers a new user."""

        user = UserHandler().create_user(name=data['name'], email=data['email'],
                                         password=data['password'])

        response = {'user': UserSerializer(user).data}

        if data['authenticate']:
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            response.update(token=token)

        return Response(response)


class SendResetPasswordEmailView(APIView):
    permission_classes = (AllowAny,)

    @extend_schema(
        tags=['User'],
        request=SendResetPasswordEmailBodyValidationSerializer,
        operation_id='send_password_reset_email',
        description=(
            'Sends an email containing the password reset link to the email address '
            'of the user. This will only be done if a user is found with the given '
            'email address. The endpoint will not fail if the email address is not '
            'found. The link is going to the valid for {valid} hours.'.format(
                valid=int(settings.RESET_PASSWORD_TOKEN_MAX_AGE / 60 / 60)
            )
        ),
        responses={
            204: None
        },
        auth=[None]
    )
    @transaction.atomic
    @validate_body(SendResetPasswordEmailBodyValidationSerializer)
    def post(self, request, data):
        """
        If the email is found, an email containing the password reset link is send to
        the user.
        """

        handler = UserHandler()

        try:
            user = handler.get_user(email=data['email'])
            handler.send_reset_password_email(user, data['base_url'])
        except UserNotFound:
            pass

        return Response('', status=204)


class ResetPasswordView(APIView):
    permission_classes = (AllowAny,)

    @extend_schema(
        tags=['User'],
        request=ResetPasswordBodyValidationSerializer,
        operation_id='reset_password',
        description=(
            'Changes the password of a user if the reset token is valid. The '
            '**send_password_reset_email** endpoint sends an email to the user '
            'containing the token. That token can be used to change the password '
            'here without providing the old password.'
        ),
        responses={
            204: None,
            400: get_error_schema([
                'BAD_TOKEN_SIGNATURE', 'EXPIRED_TOKEN_SIGNATURE',
                'ERROR_USER_NOT_FOUND', 'ERROR_REQUEST_BODY_VALIDATION'
            ])
        },
        auth=[None]
    )
    @transaction.atomic
    @map_exceptions({
        BadSignature: BAD_TOKEN_SIGNATURE,
        SignatureExpired: EXPIRED_TOKEN_SIGNATURE,
        UserNotFound: ERROR_USER_NOT_FOUND
    })
    @validate_body(ResetPasswordBodyValidationSerializer)
    def post(self, request, data):
        """Changes users password if the provided token is valid."""

        handler = UserHandler()
        handler.reset_password(data['token'], data['password'])

        return Response('', status=204)


class ChangePasswordView(APIView):
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        tags=['User'],
        request=ChangePasswordBodyValidationSerializer,
        operation_id='change_password',
        description=(
            'Changes the password of an authenticated user, but only if the old '
            'password matches.'
        ),
        responses={
            204: None,
            400: get_error_schema([
                'ERROR_INVALID_OLD_PASSWORD',
                'ERROR_REQUEST_BODY_VALIDATION'
            ])
        }
    )
    @transaction.atomic
    @map_exceptions({
        InvalidPassword: ERROR_INVALID_OLD_PASSWORD,
    })
    @validate_body(ChangePasswordBodyValidationSerializer)
    def post(self, request, data):
        """Changes the authenticated user's password if the old password is correct."""

        handler = UserHandler()
        handler.change_password(request.user, data['old_password'],
                                data['new_password'])

        return Response('', status=204)
