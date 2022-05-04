import aiohttp

import pytest
from unittest.mock import MagicMock

from app.api import retrieve_words_count_from_url_content


@pytest.mark.asyncio
async def test_retrieve_words_count_from_url_content_invalid_url():
    response = await retrieve_words_count_from_url_content("hello1234")

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_retrieve_words_count_from_url_content_invalid_order():
    response = await retrieve_words_count_from_url_content(
        "https://example.com", order="hello1234")

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_retrieve_words_count_from_url_content_content_type_error():
    mock_session = aiohttp.ClientSession
    mock_session.get = MagicMock()
    mock_session.get.return_value.__aenter__.side_effect = \
        aiohttp.ContentTypeError(
            request_info=aiohttp.RequestInfo(
                url="", headers={},
                real_url="", method="GET"),
            history=()
        )

    response = await retrieve_words_count_from_url_content(
        "https://example.com")

    assert response.status_code == 415


@pytest.mark.asyncio
async def test_retrieve_words_count_from_url_client_response_error():
    mock_session = aiohttp.ClientSession
    mock_session.get = MagicMock()
    mock_session.get.return_value.__aenter__.side_effect = \
        aiohttp.ClientResponseError(
            request_info=aiohttp.RequestInfo(
                url="", headers={},
                real_url="", method="GET"),
            history=(),
            status=404,
            message="Not found."
        )

    response = await retrieve_words_count_from_url_content(
        "https://example.com")

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_retrieve_words_count_from_url_client_connection_error():
    mock_session = aiohttp.ClientSession
    mock_session.get = MagicMock()
    mock_session.get.return_value.__aenter__.side_effect = \
        aiohttp.ClientConnectionError()

    response = await retrieve_words_count_from_url_content(
        "https://example.com")

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_retrieve_words_count_from_url_raise_exception():
    mock_session = aiohttp.ClientSession
    mock_session.get = MagicMock()
    mock_session.get.return_value.__aenter__.side_effect = Exception()

    response = await retrieve_words_count_from_url_content(
        "https://example.com")

    assert response.status_code == 500
