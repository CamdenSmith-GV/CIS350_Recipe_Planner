def test_mongodb_fixture(mongodb):
    """
    Checks that we can actually reach the database by pinging it.
    Passes if the connection string is valid and the database responds.
    """
    assert mongodb.admin.command("ping")["ok"] > 0
