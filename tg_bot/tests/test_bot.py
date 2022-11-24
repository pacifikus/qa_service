import pytest
import requests

from tg_bot.main import TableRow, format_answer, get_result_from_api, start_search


class MockResponse:
    @property
    def text(self):
        return """{
"docs": [{"post_id": 1, "text": "test", "_score": 1.5, "vector": [], "url": "test"}],
"query_time": 0.01,
"num_found": 1,
"query_embedding": [[1, 2, 3]]}"""


class MockEmptyResponse:
    @property
    def text(self):
        return """{
"docs": [],
"query_time": [],
"num_found": 0,
"query_embedding": []}"""


@pytest.mark.parametrize(
    "input_data, expected",
    [
        (
            [
                TableRow("Test_question_1", 1.5, "www.test_question_1.com"),
                TableRow("Test_question_2", 1.5, "www.test_question_2.com"),
            ],
            """```+-------------------------+-------+
    |          Result         | Score |
    +-------------------------+-------+
    |     Test_question_1     |  1.5  |
    | www.test_question_1.com |       |
    |                         |       |
    |     Test_question_2     |  1.5  |
    | www.test_question_2.com |       |
    |                         |       |
    +-------------------------+-------+```""",
        ),
        (
            [
                TableRow("Test_question_1", 1.5, "www.test_question_1.com"),
            ],
            """```+-------------------------+-------+
    |          Result         | Score |
    +-------------------------+-------+
    |     Test_question_1     |  1.5  |
    | www.test_question_1.com |       |
    |                         |       |
    +-------------------------+-------+```""",
        ),
    ],
)
def test_format_answer(input_data, expected):
    result = format_answer(input_data)
    assert result == expected


def test_get_result_from_api(monkeypatch):
    def mock_post(url, json, headers):
        return MockResponse()

    monkeypatch.setattr(requests, "post", mock_post)
    result = get_result_from_api("test", "test", 5, "test")
    assert len(result) == 4
    assert all(result)


def test_start_search_zero_found(monkeypatch):
    def mock_post(url, json, headers):
        return MockEmptyResponse()

    monkeypatch.setattr(requests, "post", mock_post)
    result = start_search("test")
    assert result == "I can't find anything :с Try again, please"


def test_start_search(monkeypatch):
    def mock_post(url, json, headers):
        return MockResponse()

    monkeypatch.setattr(requests, "post", mock_post)
    result = start_search("test")
    assert type(result) == list
    assert len(result) == 1
    assert type(result[0]) == TableRow
