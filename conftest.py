import pytest

from users.models import User


@pytest.fixture
def user1(User):
    return User.objects.create_user(
        username="user1",
        email="user1@example.com",
        password="user1password",
    )


@pytest.fixture
def user2(User):
    return User.objects.create_user(
        username="user2",
        email="user2@example.com",
        password="user2password",
    )


@pytest.fixture
def user3(User):
    return User.objects.create_user(
        username="user3",
        email="user3@example.com",
        password="user3password",
    )
