"""Offline regression tests: no real credentials or network requests are used."""
import contextlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch

import requests


SCRIPT = Path(__file__).with_name("main.py")
SPEC = importlib.util.spec_from_file_location("scholar_crawler", SCRIPT)
crawler = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(crawler)
FAKE_KEY = "fake-secret-must-not-appear"
AUTHOR = {"name": "Test Author", "author_id": "test-author"}
CITATIONS = {"table": [{"citations": {"all": 42}}]}


def article(number):
    return {
        "citation_id": "test-author:paper-{}".format(number),
        "title": "Paper {}".format(number),
        "cited_by": {"value": number},
    }


def response(articles=(), **fields):
    result = Mock(spec=requests.Response)
    result.json.return_value = {
        "author": AUTHOR,
        "cited_by": CITATIONS,
        "articles": list(articles),
        **fields,
    }
    return result


def http_error(status):
    result = response()
    result.status_code = status
    result.raise_for_status.side_effect = requests.HTTPError(
        "https://serpapi.com/search?api_key=" + FAKE_KEY, response=result
    )
    return result


class CrawlerTests(unittest.TestCase):
    def setUp(self):
        # Any unexpected request is intercepted, so these tests cannot call SerpAPI.
        self.get = self.enterContext(patch.object(crawler.requests, "get"))
        self.sleep = self.enterContext(patch.object(crawler.time, "sleep"))

    def query(self, **kwargs):
        return crawler.query_google_scholar_author("test-author", FAKE_KEY, **kwargs)

    def test_import_does_not_query_or_require_environment(self):
        with patch.dict(os.environ, {}, clear=True):
            module = importlib.util.module_from_spec(SPEC)
            SPEC.loader.exec_module(module)
        self.get.assert_not_called()

    def test_multiple_pages_preserve_articles_and_offsets(self):
        self.get.side_effect = [response([article(1), article(2)]), response([article(3)])]
        author, articles, citations = self.query(num=2)
        self.assertEqual(author, AUTHOR)
        self.assertEqual(citations, CITATIONS)
        self.assertEqual(articles, [article(1), article(2), article(3)])
        self.assertEqual([call.kwargs["params"]["start"] for call in self.get.call_args_list], [0, 2])
        for call in self.get.call_args_list:
            self.assertEqual(call.kwargs["timeout"], (10, 30))
            self.assertEqual(call.kwargs["params"]["api_key"], FAKE_KEY)
        self.sleep.assert_not_called()

    def test_exact_full_page_stops_at_empty_next_page(self):
        self.get.side_effect = [response([article(1)]), response()]
        self.assertEqual(len(self.query(num=1)[1]), 1)
        self.assertEqual(self.get.call_count, 2)

    def test_empty_author_has_no_publications(self):
        self.get.return_value = response()
        self.assertEqual(self.query()[1], [])
        self.assertEqual(self.get.call_count, 1)

    def test_timeout_retries_are_bounded_and_do_not_leak_key(self):
        self.get.side_effect = requests.Timeout("failed ?api_key=" + FAKE_KEY)
        with self.assertLogs("Scholar", level="WARNING") as logs:
            with self.assertRaises(crawler.ScholarAPIError) as error:
                self.query(retry_num=3)
        self.assertEqual(self.get.call_count, 3)
        self.assertEqual([call.args[0] for call in self.sleep.call_args_list], [1, 2])
        self.assertNotIn(FAKE_KEY, str(error.exception) + " ".join(logs.output))

    def test_transient_network_failure_recovers(self):
        self.get.side_effect = [requests.ConnectionError("api_key=" + FAKE_KEY), response([article(1)])]
        self.assertEqual(len(self.query(retry_num=2)[1]), 1)
        self.sleep.assert_called_once_with(1)

    def test_transient_http_failures_retry(self):
        for status in (408, 429, 500, 503):
            with self.subTest(status=status):
                self.get.reset_mock()
                self.get.side_effect = [http_error(status), response()]
                self.assertEqual(self.query(retry_num=2)[1], [])
                self.assertEqual(self.get.call_count, 2)

    def test_permanent_http_errors_fail_without_retry_or_key(self):
        for status in (400, 401, 403, 404):
            with self.subTest(status=status):
                self.get.reset_mock()
                self.get.return_value = http_error(status)
                with self.assertRaises(crawler.ScholarAPIError) as error:
                    self.query()
                self.assertEqual(self.get.call_count, 1)
                self.assertNotIn(FAKE_KEY, str(error.exception))
        self.sleep.assert_not_called()

    def test_backoff_is_capped(self):
        self.get.side_effect = requests.Timeout()
        with self.assertRaises(crawler.ScholarAPIError):
            self.query(retry_num=6)
        self.assertEqual([call.args[0] for call in self.sleep.call_args_list], [1, 2, 4, 8, 8])

    def test_later_page_failure_does_not_return_partial_data(self):
        self.get.side_effect = [response([article(1)]), requests.Timeout(), requests.Timeout()]
        with self.assertRaises(crawler.ScholarAPIError):
            self.query(num=1, retry_num=2)
        self.assertEqual(self.get.call_count, 3)

    def test_invalid_json_is_bounded(self):
        invalid = response()
        invalid.json.side_effect = requests.exceptions.JSONDecodeError("bad JSON", "api_key=" + FAKE_KEY, 0)
        self.get.return_value = invalid
        with self.assertRaises(crawler.ScholarAPIError) as error:
            self.query(retry_num=2)
        self.assertEqual(self.get.call_count, 2)
        self.assertNotIn(FAKE_KEY, str(error.exception))

    def test_api_error_is_safely_reported(self):
        self.get.return_value = response(error="Invalid api_key=" + FAKE_KEY)
        with self.assertRaises(crawler.ScholarAPIError) as error:
            self.query()
        self.assertEqual(self.get.call_count, 1)
        self.assertNotIn(FAKE_KEY, str(error.exception))

    def test_malformed_response_fails_clearly(self):
        for payload in ([], {}, {"author": AUTHOR}, {"author": AUTHOR, "cited_by": CITATIONS, "articles": None}):
            with self.subTest(payload=payload):
                self.get.return_value = response()
                self.get.return_value.json.return_value = payload
                with self.assertRaises(crawler.ScholarAPIError):
                    self.query()

    def test_repeated_full_page_cannot_loop_forever(self):
        self.get.return_value = response([article(1)])
        with self.assertRaisesRegex(crawler.ScholarAPIError, "progress"):
            self.query(num=1)
        self.assertEqual(self.get.call_count, 2)

    def test_invalid_publication_is_rejected(self):
        for bad_article in (None, {}, {"citation_id": ""}, {"citation_id": []}):
            with self.subTest(article=bad_article):
                self.get.return_value = response([bad_article])
                with self.assertRaises(crawler.ScholarAPIError):
                    self.query()

    def test_invalid_inputs_do_not_make_requests(self):
        for kwargs in ({"num": 0}, {"retry_num": 0}):
            with self.assertRaises(crawler.ScholarAPIError):
                self.query(**kwargs)
        self.get.assert_not_called()

    def test_output_schema_is_preserved(self):
        source_article = article(2)
        data, badge = crawler.build_results(AUTHOR, [source_article], CITATIONS)
        self.assertEqual(data["name"], AUTHOR["name"])
        self.assertEqual(data["citations"], CITATIONS)
        self.assertEqual(data["citedby"], 42)
        self.assertIn("updated", data)
        self.assertEqual(data["publications"][source_article["citation_id"]], {**source_article, "num_citations": 2})
        self.assertNotIn("num_citations", source_article)
        self.assertEqual(badge, {"schemaVersion": 1, "label": "citations", "message": "42"})

    def test_missing_citation_fields_fail_before_writing(self):
        for citations in ({}, {"table": []}, {"table": None}):
            with self.subTest(citations=citations):
                with self.assertRaises(crawler.ScholarAPIError):
                    crawler.build_results(AUTHOR, [article(1)], citations)
        with self.assertRaises(crawler.ScholarAPIError):
            crawler.build_results(AUTHOR, [{"citation_id": "test"}], CITATIONS)

    def run_main(self, directory):
        with patch.dict(os.environ, {"GOOGLE_SCHOLAR_ID": "test-author", "SERPAPI_KEY": FAKE_KEY}, clear=True):
            with contextlib.chdir(directory):
                return crawler.main()

    def test_main_writes_expected_files(self):
        self.get.return_value = response([article(1)])
        with tempfile.TemporaryDirectory() as directory:
            self.assertEqual(self.run_main(directory), 0)
            data = json.loads((Path(directory) / "results/gs_data.json").read_text())
            badge = json.loads((Path(directory) / "results/gs_data_shieldsio.json").read_text())
            self.assertEqual(data["publications"]["test-author:paper-1"]["num_citations"], 1)
            self.assertEqual(badge["message"], "42")

    def test_failure_preserves_existing_files_and_logs_no_key(self):
        self.get.return_value = response(error="api_key=" + FAKE_KEY)
        with tempfile.TemporaryDirectory() as directory:
            results = Path(directory) / "results"
            results.mkdir()
            for name in ("gs_data.json", "gs_data_shieldsio.json"):
                (results / name).write_text("old data")
            with self.assertLogs("Scholar", level="ERROR") as logs:
                self.assertEqual(self.run_main(directory), 1)
            self.assertNotIn(FAKE_KEY, " ".join(logs.output))
            self.assertEqual([p.read_text() for p in results.iterdir()], ["old data", "old data"])

    def test_cli_missing_secrets_exits_nonzero_without_traceback(self):
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run(
                [sys.executable, str(SCRIPT)], cwd=directory, env={},
                text=True, capture_output=True, timeout=10,
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn("GOOGLE_SCHOLAR_ID and SERPAPI_KEY must be set", result.stderr)
            self.assertNotIn("Traceback", result.stderr)
            self.assertFalse((Path(directory) / "results").exists())


if __name__ == "__main__":
    unittest.main()
