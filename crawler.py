import aiohttp
from bs4 import BeautifulSoup


async def get_url_content(url: str) -> str:
    async with aiohttp.ClientSession(raise_for_status=True) as session:
        async with session.get(url) as response:
            if response.ok and response.content_type == "text/html":
                result = await response.text()
                return result
            elif response.ok and response.content_type != "text/html":
                raise aiohttp.ContentTypeError(
                    request_info=aiohttp.RequestInfo(
                        url=url, headers=response.headers,
                        real_url=url, method="GET"),
                    history=())


def extract_text_from_html(html_content: str) -> list:
    soup = BeautifulSoup(html_content, "html.parser")
    body = soup.body
    text_content = []

    for string in body.strings:
        stripped_string = string.lstrip().rstrip()\
            .strip(".").strip("?").strip("!").strip(",")\
            .strip(";")
        if len(stripped_string) > 0:
            stripped_string_list = stripped_string.split()
            text_content.extend(stripped_string_list)

    return text_content


def count_words_from_sentences(sentences: list[str]) -> dict:
    words_counts = {}

    for word in sentences:
        lowered_word = word.lower()
        stripped_word = lowered_word.lstrip().rstrip()\
            .strip(",").strip(";")\
            .strip(".").strip("?").strip("!")\
            .strip("'").strip("\"").strip("(")\
            .strip(")").strip("[").strip("]")
        if stripped_word in words_counts.keys():
            words_counts[stripped_word] += 1
        else:
            words_counts[stripped_word] = 1

    return words_counts
