import os


def test_db_exits(db_path: str):
    assert os.path.exists(db_path)
