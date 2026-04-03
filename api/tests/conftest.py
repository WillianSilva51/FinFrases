import os
import pytest

os.environ["MONGO_URI"] = "mongodb://localhost:27017/testdb"
os.environ["API_KEY"] = "fake_test_key"


@pytest.fixture(autouse=True, scope="session")
def setup_test_env():
    pass
