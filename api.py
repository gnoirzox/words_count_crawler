import logging
from typing import Optional

from fastapi import FastAPI, status
from aiohttp import ClientResponseError

import crawler

logging.basicConfig(format='%(asctime)s %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()


@app.get("/get_text/{url:path}")
async def retrieve_url_content(url: str, order: Optional[str] = None):
    if not crawler.url_path_is_valid(url):
        return {"error": "The given url is not valid"}

    try:
        response_content = await crawler.get_url_content(url)
    except ClientResponseError as e:
        logger.exception(
            "A ClientResponseError occured when trying"
            f" to access to the url {url}"
            f" with the message: {e.message}; and status: {e.status}")

        return {"error": f"An error occured with the url: {url};"
                " please check that the provided url is valid."}
    except Exception as e:
        logger.exception(
            f"An Exception occured when trying to access to the url {url}"
            f" with the message: {e}")

    text = crawler.extract_text_from_html(response_content)
    words_counts = crawler.count_words_from_sentences(text)

    if order and order in {"alphabetical", "desc_count", "asc_count"}:
        if order == "alphabetical":
            words_counts = sorted(
                words_counts.items(), key=lambda item: item[0])
        elif order == "desc_count":
            words_counts = sorted(
                words_counts.items(),
                key=lambda item: item[1],
                reverse=True
            )
        elif order == "asc_count":
            words_counts = sorted(
                words_counts.items(), key=lambda item: item[1])
    else:
        words_counts = list(words_counts.items())

    return {"words_counts": words_counts}


@app.get("/health", status_code=status.HTTP_200_OK)
async def health_endpoint():
    return {"status": "healthy"}
