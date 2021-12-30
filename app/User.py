"""User Model."""

from masonite.authentication import Authenticates
from masoniteorm.models import Model


class User(Model, Authenticates):
    """User Model."""

    __fillable__ = ["name", "email", "password"]

    __auth__ = "email"
