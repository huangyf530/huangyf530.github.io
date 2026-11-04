import json
from datetime import datetime
import logging
import os
from pathlib import Path
import time

import requests


logger = logging.getLogger("Scholar")
REQUEST_TIMEOUT = (10, 30)  # Connect and read timeouts, in seconds.


class ScholarAPIError(RuntimeError):
    """A safe-to-log error without request URLs, API keys, or response bodies."""


def _fetch_author_page(params, retry_num):
    """Retry only a bounded number of times, without exposing API credentials."""
    reason = "request failed"
    for attempt in range(1, retry_num + 1):
        logger.info("[%s / %s] Try to get author information", attempt, retry_num)
        try:
            response = requests.get(
                "https://serpapi.com/search", params=params, timeout=REQUEST_TIMEOUT
            )
            response.raise_for_status()
            payload = response.json()
        except requests.exceptions.HTTPError as error:
            status = error.response.status_code if error.response is not None else None
            reason = "HTTP {}".format(status) if status is not None else "HTTP error"
            if status is not None and 400 <= status < 500 and status not in (408, 429):
                raise ScholarAPIError("SerpAPI request rejected ({})".format(reason)) from None
        except ValueError:
            # requests.JSONDecodeError is also a RequestException.
            reason = "invalid JSON response"
        except requests.exceptions.RequestException:
            # Exception text can contain the full request URL, including api_key.
            reason = "network request failed"
        else:
            if not isinstance(payload, dict):
                raise ScholarAPIError("SerpAPI returned an invalid response object")
            if "error" in payload:
                # API error messages can echo request parameters. Never log them.
                raise ScholarAPIError("SerpAPI returned an API error; check credentials, quota, and author ID")
            return payload

        logger.warning("SerpAPI attempt %s failed: %s", attempt, reason)
        if attempt < retry_num:
            time.sleep(min(2 ** (attempt - 1), 8))

    raise ScholarAPIError(
        "SerpAPI request failed after {} attempts ({})".format(retry_num, reason)
    )


def query_google_scholar_author(author_id, api_key, num=20, retry_num=10):
    """Fetch all author pages, or raise instead of returning partial results."""
    if not author_id or not api_key:
        raise ScholarAPIError("GOOGLE_SCHOLAR_ID and SERPAPI_KEY must be set")
    if num < 1 or retry_num < 1:
        raise ScholarAPIError("num and retry_num must be positive")

    author_info = None
    articles_info = []
    citation_info = None
    seen_article_ids = set()

    while True:
        logger.info("Already have %s articles, continue to search", len(articles_info))
        params = {
            "engine": "google_scholar_author",
            "author_id": author_id,
            "api_key": api_key,
            "hl": "en",
            "start": len(articles_info),
            "num": num,
        }
        payload = _fetch_author_page(params, retry_num)
        page_articles = payload.get("articles", [])
        if not isinstance(page_articles, list):
            raise ScholarAPIError("SerpAPI returned an invalid articles list")
        if author_info is None:
            author_info = payload.get("author")
            citation_info = payload.get("cited_by")
            if not isinstance(author_info, dict) or not isinstance(citation_info, dict):
                raise ScholarAPIError("SerpAPI response is missing author or citation data")

        page_ids = set()
        for article in page_articles:
            if not isinstance(article, dict) or not isinstance(article.get("citation_id"), str):
                raise ScholarAPIError("SerpAPI returned an article without a valid citation ID")
            if not article["citation_id"]:
                raise ScholarAPIError("SerpAPI returned an article without a valid citation ID")
            page_ids.add(article["citation_id"])
        if page_articles and not page_ids.difference(seen_article_ids):
            raise ScholarAPIError("SerpAPI pagination stopped making progress")
        seen_article_ids.update(page_ids)
        articles_info.extend(page_articles)
        logger.info("Get author info and %s articles information", len(page_articles))
        if len(page_articles) < num:
            return author_info, articles_info, citation_info


def build_results(author, articles, citations):
    """Keep the existing JSON format consumed by the homepage and badge."""
    gs_data = {"updated": str(datetime.now())}
    gs_data.update(author)
    gs_data["citations"] = citations
    try:
        gs_data["citedby"] = citations["table"][0]["citations"]["all"]
        gs_data["publications"] = {}
        for article in articles:
            publication = dict(article)
            publication["num_citations"] = article["cited_by"]["value"]
            gs_data["publications"][article["citation_id"]] = publication
    except (KeyError, IndexError, TypeError):
        raise ScholarAPIError("SerpAPI response is missing required citation fields") from None
    shieldio_data = {
        "schemaVersion": 1,
        "label": "citations",
        "message": str(gs_data["citedby"]),
    }
    return gs_data, shieldio_data


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
    )
    try:
        author_id = os.environ.get("GOOGLE_SCHOLAR_ID", "").strip()
        api_key = os.environ.get("SERPAPI_KEY", "").strip()
        author, articles, citations = query_google_scholar_author(author_id, api_key, num=100)
        gs_data, shieldio_data = build_results(author, articles, citations)
        # Fetch and validate every page before creating or overwriting output.
        results = Path("results")
        results.mkdir(exist_ok=True)
        with (results / "gs_data.json").open("w", encoding="utf-8") as outfile:
            json.dump(gs_data, outfile, ensure_ascii=False, indent=2)
        with (results / "gs_data_shieldsio.json").open("w", encoding="utf-8") as outfile:
            json.dump(shieldio_data, outfile, ensure_ascii=False, indent=2)
    except ScholarAPIError as error:
        logger.error("Google Scholar crawl failed: %s", error)
        return 1
    except OSError:
        logger.error("Cannot write Google Scholar result files")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
