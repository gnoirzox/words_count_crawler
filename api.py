import logging
from typing import Optional

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from aiohttp import ClientConnectionError, ClientResponseError,\
    ContentTypeError

import crawler
import utils

logging.basicConfig(format='%(asctime)s %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()


@app.get("/get_text/{url:path}")
async def retrieve_url_content(url: str, order: Optional[str] = None):
    if not utils.url_path_is_valid(url):
        return {"error": "The given url is not valid"}

    try:
        response_content = await crawler.get_url_content(url)
    except ContentTypeError as e:
        logger.exception(
            "A ContentTypeError occured when trying"
            f" to access to the url {url};"
            f" with error: {e}"
        )

        return JSONResponse(
            status_code=415,
            content={
                "error": f"A content type error occured with the url: {url};"
                " please check that the url is providing"
                " the expected HTML content."
            }
        )
    except ClientResponseError as e:
        logger.exception(
            "A ClientResponseError occured when trying"
            f" to access to the url {url}"
            f" with the message: {e.message}; and status: {e.status}")

        return JSONResponse(
            status_code=e.status,
            content={
                "error": f"An error occured with the url: {url};"
                " please check that the provided url is valid."
            }
        )

    except ClientConnectionError as e:
        logger.exception(
            "A ClientConnectionError occured when trying"
            f" to access to the url {url}"
            f" with the error: {e}")

        return JSONResponse(
            status_code=400,
            content={
                "error": f"A connection error occured with the url: {url};"
                " please check that the provided url is valid."
            }
        )
    except Exception as e:
        logger.exception(
            f"An Exception occured when trying to access to the url {url}"
            f" with the message: {e}")

        return JSONResponse(
            status_code=500,
            content={
                "error": "An internal error occured."
            }
        )

    text = crawler.extract_text_from_html(response_content)
    words_counts = crawler.count_words_from_sentences(text)
    words_counts_list = utils.transform_words_counts_order(words_counts, order)

    return {"words_counts": words_counts_list}


@app.get("/health", status_code=status.HTTP_200_OK)
async def health_endpoint():
    return {"status": "healthy"}
