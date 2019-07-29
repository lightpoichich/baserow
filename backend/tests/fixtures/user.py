from django.contrib.auth import get_user_model


User = get_user_model()


class UserFixtures:
    def create_user(self, **kwargs):
        kwargs.setdefault('email', self.fake.email())
        kwargs.setdefault('username', kwargs['email'])
        kwargs.setdefault('first_name', self.fake.name())
        kwargs.setdefault('password', 'password')

        user = User(**kwargs)
        user.set_password(kwargs['password'])
        user.save()

        return user
