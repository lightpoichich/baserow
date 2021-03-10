from faker import Faker

from .settings import SettingsFixtures
from .user import UserFixtures
from .user_file import UserFileFixtures
from .group import GroupFixtures
from .application import ApplicationFixtures
from .table import TableFixtures
from .view import ViewFixtures
from .field import FieldFixtures
from .token import TokenFixtures


class Fixtures(SettingsFixtures, UserFixtures, UserFileFixtures, GroupFixtures,
               ApplicationFixtures, TableFixtures, ViewFixtures, FieldFixtures,
               TokenFixtures):
    fake = Faker()
