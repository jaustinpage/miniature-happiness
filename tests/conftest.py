import pytest

from miniature_happiness import create_app


@pytest.fixture(scope="session")
def app():
    return create_app()
