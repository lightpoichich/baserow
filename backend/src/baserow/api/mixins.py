from baserow.core.exceptions import UnknownFieldProvided


class UnknownFieldRaisesExceptionSerializerMixin:
    def validate(self, data):
        if hasattr(self, "initial_data"):
            unknown_keys = set(self.initial_data.keys()) - set(self.fields.keys())
            if unknown_keys:
                raise UnknownFieldProvided(
                    f"Received unknown fields: {unknown_keys}. Please check "
                    "the api documentation and only provide "
                    "valid fields."
                )

        return data
