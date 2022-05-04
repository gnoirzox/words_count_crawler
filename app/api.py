import logging
from typing import Optional

from aiohttp import ClientConnectionError, ClientResponseError,\
    ContentTypeError
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi


import crawler
import utils
import openapi_schema

logging.basicConfig(format='%(asctime)s %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()


def my_schema():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
       title="Words counter api",
       version="1.0.0",
       description="Words count webpage crawling api",
       routes=app.routes,
    )

    openapi_schema["info"] = {
        "title": "Words counter API",
        "description": "Words count webpage crawling api",
        "version": "1.0.0"
    }

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = my_schema


@app.get("/words_count/{url:path}", responses={
    **openapi_schema.words_count_responses})
async def retrieve_words_count_from_url_content(
        url: str, order: Optional[str] = None):
    """
    Retrieve words counts from an external url with content-type 'text/html'

    The returned JSON object is a list of words with their attached
    count number and is ordered depending on the optional order query parameter
    ("alphabetical", "asc_count", "desc_count")
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

    if order and order not in {"alphabetical", "asc_count", "desc_count"}:
        return JSONResponse(
            status_code=422,
            content={
                "error": "The given order value is not valid;"
                " please ensure that the given order is"
                " one of the following values:"
                " 'alphabetical', 'asc_count' or 'desc_count'"
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
