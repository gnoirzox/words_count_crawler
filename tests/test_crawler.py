import aiohttp

import pytest
from unittest.mock import MagicMock

import crawler


@pytest.fixture
def session_response():
    return """<html>
<meta></meta>
<body>
    <h2>Tell the audience</h2>
    <div>Tell the audience what you're going to say.</div>
    <p><span>Say it.</span> Then tell them what you've said.</p>
</body>
</html>"""


@pytest.mark.asyncio
async def test_get_url_content(session_response):
    mock_session = aiohttp.ClientSession
    mock_session.get = MagicMock()
    mock_session.get.return_value.__aenter__.return_value.ok = True
    mock_session.get.return_value.__aenter__.return_value.\
        content_type = "text/html"
    mock_session.get.return_value.__aenter__.return_value.\
        text.return_value = session_response

    response = await crawler.get_url_content("https://example.com")
    assert response == session_response


@pytest.mark.asyncio
async def test_get_url_content_raised_exception():
    mock_session = aiohttp.ClientSession
    mock_session.get = MagicMock()
    mock_session.get.return_value.__aenter__.return_value.ok = True
    mock_session.get.return_value.__aenter__.return_value.\
        content_type = "image/svg"

    with pytest.raises(aiohttp.ContentTypeError):
        await crawler.get_url_content("https://example.com")


def test_extract_text_from_html():
    html_content = """<html>
    <meta></meta>
    <body>
        <h2>Tell the audience</h2>
        <div>Tell the audience what you're going to say.</div>
        <p><span>Say it.</span> Then tell them what you've said.</p>
    </body>
</html>"""
    assert crawler.extract_text_from_html(html_content) == [
        "Tell", "the", "audience",
        "Tell", "the", "audience", "what", "you're", "going", "to", "say",
        "Say", "it", "Then", "tell", "them", "what", "you've", "said"
    ]


def test_extract_text_from_html_empty():
    html_content = "<html><meta></meta><body></body></html>"
    assert crawler.extract_text_from_html(html_content) == []


def test_count_words_from_sentences():
    sentences_list = [
        "Tell", "the", "audience",
        "Tell", "the", "audience", "what", "you're", "going", "to", "say",
        "Say", "it", "Then", "tell", "them", "what", "you've", "said"
    ]
    assert crawler.count_words_from_sentences(sentences_list) == {
        "tell": 3, "the": 2, "audience": 2, "what": 2, "you're": 1,
        "going": 1, "to": 1, "say": 2,
        "it": 1, "then": 1, "them": 1, "you've": 1, "said": 1
    }


def test_count_words_from_sentences_empty():
    assert crawler.count_words_from_sentences([]) == {}
