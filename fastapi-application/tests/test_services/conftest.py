import pytest

from io import BytesIO
from fastapi import UploadFile
from starlette.datastructures import Headers


@pytest.fixture
def mock_upload_file() -> UploadFile:
    """
    Создаёт реалистичный UploadFile для тестов.
    Использует BytesIO для имитации загруженного файла.
    """
    file = UploadFile(
        filename="test_image.jpg",
        file=BytesIO(b"fake image content"),
        headers=Headers({"content-type": "image/jpeg"}),
    )
    return file
