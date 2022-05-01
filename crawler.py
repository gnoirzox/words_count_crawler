import logging

from bs4 import BeautifulSoup
import requests
import validators

logging.basicConfig(format='%(asctime)s %(message)s')
logger = logging.getLogger(__name__)


def url_path_is_valid(url_path: str) -> bool:
    url_is_valid = False

    if validators.url(url_path):
        url_is_valid = True

    return url_is_valid


def get_url_content(url: str) -> str:
    try:
        response = requests.get(url)

        if response.status_code == requests.codes.ok:
            return response.text
        else:
            logger.error(
                f"We got an unexpected error message for the url {url}"
                f" with HTTP status code: {response.status_code}")
    except Exception as e:
        logger.exception(
            f"An error occured when trying to access to the url {url}"
            f" with the message: {e}")


def extract_text_from_html(html_content: str) -> list:
    soup = BeautifulSoup(html_content, "html.parser")
    body = soup.body
    text_content = []

    for string in body.strings:
        stripped_string = string.lstrip().rstrip()\
            .strip(".").strip("?").strip("!").strip(",")\
            .strip(";").strip("'").strip("\"")
        if len(stripped_string) > 0:
            text_content.append(stripped_string)

    return text_content


def count_words_from_sentences(sentences: list[str]) -> dict:
    words_counts = {}

    for sentence in sentences:
        sentence_list = sentence.split()
        for word in sentence_list:
            stripped_word = word.lstrip().rstrip()
            if stripped_word in words_counts.keys():
                words_counts[stripped_word] += 1
            else:
                words_counts[stripped_word] = 1

    return words_counts
