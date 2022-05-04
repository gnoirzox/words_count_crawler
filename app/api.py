import logging
from typing import Optional

from aiohttp import ClientConnectionError, ClientResponseError,\
    ContentTypeError
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

import crawler
import utils

logging.basicConfig(format='%(asctime)s %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()

words_count_responses = {
    200: {"description": "Everything went well"},
    400: {
        "description": "A connection error occured with the given url"
    },
    404: {"description": "The distant url is not available at the moment"},
    415: {"description": "A content type error occured with the given url"},
    422: {
        "description": "An error occured due to one of the given parameters"
        " (url or order)"
    },
    500: {"description": "An internal error occured"}
}


@app.get("/words_count/{url:path}", responses={**words_count_responses})
async def retrieve_words_count_from_url_content(
        url: str, order: Optional[str] = None):
    """
    Retrieve words counts from an external url with content-type 'text/html'

    The returned JSON object returns a list of words with their attached
    count number and order depending on the optionall order query parameter
    ("alphabetical", "desc_count", "asc_count")
    """
    if not utils.url_path_is_valid(url):
        return JSONResponse(
            status_code=422,
            content={
                "error": "The given url is not valid;"
                " please ensure that the given url starts"
                " either with 'http' or 'https'."
            }
        )

    if order and order not in {"alphabetical", "desc_count", "asc_count"}:
        return JSONResponse(
            status_code=422,
            content={
                "error": "The given order value is not valid;"
                " please ensure that the given order is"
                " one of the following values:"
                " 'alphabetical', 'desc_count' or 'asc_count'"
            }
        )

    try:
        response_content = await crawler.get_url_content(url)
    except ContentTypeError as e:
        logger.exception(
            "A ContentTypeError occured when trying"
            f" to access to the url {url};"
            f" with error: {e}."
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
            f" with the message: {e.message}; and status: {e.status}.")

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
            f" with the error: {e}.")

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
            f" with the error: {e}.")

        return JSONResponse(
            status_code=500,
            content={
                "error": "An internal error occured."
            }
        )

    extracted_text = crawler.extract_text_from_html(response_content)
    words_counts_dict = crawler.count_words_from_sentences(extracted_text)
    words_counts_list = utils.transform_words_counts_order(
        words_counts_dict, order)

    return {"words_counts": words_counts_list}


@app.get("/health", status_code=status.HTTP_200_OK)
async def health_endpoint():
    return {"status": "healthy"}
