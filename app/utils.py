from typing import Optional

import validators


def url_path_is_valid(url_path: str) -> bool:
    url_is_valid = False

    if validators.url(url_path):
        url_is_valid = True

    return url_is_valid


def transform_words_counts_order(
        words_counts: dict, order: Optional[str] = None) -> list:
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
        # If the order value is not set, then just returned an unordered list
        words_counts = list(words_counts.items())

    return words_counts
