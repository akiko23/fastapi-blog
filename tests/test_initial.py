import os


def test_db_exits(db_path: str) -> None:
    assert os.path.exists(db_path)
