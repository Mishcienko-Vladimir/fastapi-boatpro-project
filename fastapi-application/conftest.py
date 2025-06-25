import os


# Изменяет переменную окружения на TEST, при запуске тестов через pytest.
os.environ["MODE"] = "TEST"