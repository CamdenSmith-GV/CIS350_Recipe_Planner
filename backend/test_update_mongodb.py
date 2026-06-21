def test_update_mongodb(mongodb, rollback_session):
    """
    Inserts a document into the real database, reads it back to confirm it saved,
    then the rollback_session undoes it so nothing is left behind.
    """
    my_collection = mongodb["recipe_database"]["recipes"]
    my_collection.insert_one(
        {
            "_id": "bad_document",
            "description": (
                "If this still exists, then transactions are not working."
            ),
        },
        session=rollback_session,
    )
    assert (
        my_collection.find_one(
            {"_id": "bad_document"}, session=rollback_session
        )
        is not None
    )
