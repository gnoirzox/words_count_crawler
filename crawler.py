import logging

from bs4 import BeautifulSoup
import aiohttp
import validators

logging.basicConfig(format='%(asctime)s %(message)s')
logger = logging.getLogger(__name__)


def url_path_is_valid(url_path: str) -> bool:
    url_is_valid = False

    if validators.url(url_path):
        url_is_valid = True

    return url_is_valid


async def get_url_content(url: str) -> str:
    async with aiohttp.ClientSession(raise_for_status=True) as session:
        async with session.get(url) as response:
            if response.ok:
                result = await response.text()
                return result


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
