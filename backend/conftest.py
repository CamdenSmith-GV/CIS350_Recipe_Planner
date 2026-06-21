import pytest
import pymongo


@pytest.fixture(scope="session")
def mongodb():
    """
    Connects to the real database once for the whole test run, pings it to make
    sure we can reach it, then gives the connection to any test that needs.
    """
    client = pymongo.MongoClient(
        "mongodb+srv://calihanw_db_user:popcorn@cluster.ivrzvu1.mongodb.net/"
    )
    assert client.admin.command("ping")["ok"] != 0.0
    yield client
    client.close()


@pytest.fixture
def rollback_session(mongodb):
    """
    Wraps a test in a transaction so any writes get undone afterwards, that way
    our tests never leave junk data in the real database.
    """
    session = mongodb.start_session()
    session.start_transaction()
    try:
        yield session
    finally:
        session.abort_transaction()
