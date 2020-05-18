from baserow.core.emails import BaseEmailMessage
from django.utils.translation import gettext as _


class ResetPasswordEmail(BaseEmailMessage):
    subject = _('Reset password')
    template_name = 'baserow/core/user/reset_password.html'

    def __init__(self, user, reset_url, *args, **kwargs):
        self.reset_url = reset_url
        self.user = user
        super().__init__(*args, **kwargs)

    def get_context(self):
        context = super().get_context()
        context.update(user=self.user, reset_url=self.reset_url)
        return context
