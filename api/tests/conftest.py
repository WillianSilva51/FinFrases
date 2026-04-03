import os
import pytest


@pytest.fixture(autouse=True, scope="session")
def setup_test_env():
    os.environ["MONGO_URI"] = "mongodb://localhost:27017/testdb"
    os.environ["API_KEY"] = "fake_test_key"
