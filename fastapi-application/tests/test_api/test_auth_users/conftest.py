import pytest

from utils.limiter import limiter


@pytest.fixture(autouse=True)
def reset_limiter():
    """
    Сбрасывает счётчики лимитов перед каждым тестом.
    """
    limiter.reset()
    yield
    limiter.reset()
