import pytest

import miniature_happiness


@pytest.fixture(scope="session")
def app():
    return miniature_happiness.create_app()
