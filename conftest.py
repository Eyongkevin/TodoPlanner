import pytest


@pytest.fixture(autouse=True)
def give_db_access(db):
    pass
