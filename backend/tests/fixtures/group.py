from baserow.core.models import Group, GroupUser


class GroupFixtures:
    def create_group(self, **kwargs):
        user = kwargs.pop('user', None)
        users = kwargs.pop('users', [])

        if user:
            users.insert(0, user)

        kwargs.setdefault('name', self.fake.name())
        group = Group.objects.create(**kwargs)

        for user in users:
            self.create_user_group(group=group, user=user, order=0)

        return group

    def create_user_group(self, **kwargs):
        kwargs.setdefault('group', self.create_group())
        kwargs.setdefault('user', self.create_user())
        kwargs.setdefault('order', 0)
        return GroupUser.objects.create(**kwargs)
