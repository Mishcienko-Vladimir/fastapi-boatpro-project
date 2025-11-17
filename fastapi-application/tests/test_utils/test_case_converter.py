import pytest

from utils.case_converter import camel_case_to_snake_case


@pytest.mark.parametrize(
    "input_str, expected",
    [
        ("SomeSDK", "some_sdk"),
        ("RServoDrive", "r_servo_drive"),
        ("SDKDemo", "sdk_demo"),
        ("HTMLParser", "html_parser"),
        ("iPhone", "i_phone"),
        ("XMLHttpRequest", "xml_http_request"),
        ("A", "a"),
        ("simple", "simple"),
        ("CamelCase", "camel_case"),
        ("", ""),
        ("_Leading", "__leading"),
        ("trailing_", "trailing_"),
    ],
)
def test_camel_case_to_snake_case(
    input_str: str,
    expected: str,
):
    """
    Тест конвертации из CamelCase в snake_case.
    """
    assert camel_case_to_snake_case(input_str) == expected
