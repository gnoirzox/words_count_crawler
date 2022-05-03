import pytest

import utils


@pytest.fixture
def words_counts_dict():
    return {
        "tell": 2, "the": 1, "audience": 1,
        "what": 2, "you're": 1, "going": 1,
        "to": 1, "say": 2, "it": 1, "then": 1,
        "them": 1, "you've": 1, "said": 1
    }


def test_url_path_is_valid_true():
    assert utils.url_path_is_valid("https://www.bbc.co.uk") is True
    assert utils.url_path_is_valid("http://www.dw.com") is True


def test_url_path_is_valid_false():
    assert utils.url_path_is_valid("tps://www.bbc.co.uk") is False
    assert utils.url_path_is_valid("www.bbc.co.uk") is False
    assert utils.url_path_is_valid("www23243") is False


def test_transform_words_counts_order(words_counts_dict):
    assert utils.transform_words_counts_order(
        words_counts_dict, order=None) == [
        ("tell", 2), ("the", 1), ("audience", 1), ("what", 2), ("you're", 1),
        ("going", 1), ("to", 1), ("say", 2), ("it", 1), ("then", 1),
        ("them", 1), ("you've", 1), ("said", 1)
    ]


def test_transform_words_counts_order_ascending(words_counts_dict):
    assert utils.transform_words_counts_order(
        words_counts_dict, order="asc_count") == [
        ("the", 1), ("audience", 1), ("you're", 1),
        ("going", 1), ("to", 1), ("it", 1), ("then", 1),
        ("them", 1), ("you've", 1), ("said", 1),
        ("tell", 2), ("what", 2), ("say", 2)
    ]


def test_transform_words_counts_order_descending(words_counts_dict):
    assert utils.transform_words_counts_order(
        words_counts_dict, order="desc_count") == [
        ("tell", 2), ("what", 2), ("say", 2), ("the", 1),
        ("audience", 1), ("you're", 1),
        ("going", 1), ("to", 1), ("it", 1), ("then", 1),
        ("them", 1), ("you've", 1), ("said", 1)
    ]


def test_transform_words_counts_order_alphabetical(words_counts_dict):
    assert utils.transform_words_counts_order(
        words_counts_dict, order="alphabetical") == [
        ("audience", 1), ("going", 1), ("it", 1),
        ("said", 1), ("say", 2), ("tell", 2),
        ("the", 1), ("them", 1), ("then", 1), ("to", 1),
        ("what", 2), ("you're", 1), ("you've", 1)
    ]
