from datetime import datetime

import arxiv
import pytest

from aquarius.tools.arxiv_fetch import fetch_arxiv_articles


@pytest.fixture
def mock_arxiv_search(monkeypatch):
    class MockResult:
        def __init__(self, title, summary, authors, entry_id):
            class Author:
                def __init__(self, name):
                    self.name = name

            self.title = title
            self.summary = summary
            self.authors = [Author(name) for name in authors]
            self.entry_id = entry_id

    class MockSearch:
        def __init__(self, query, max_results, sort_by):
            self.query = query
            self.max_results = max_results
            self.sort_by = sort_by

        def results(self):
            return [
                MockResult(
                    title="Paper 1",
                    summary="Summary 1",
                    authors=["Author 1", "Author 2"],
                    entry_id="https://arxiv.org/abs/1234.56789",
                ),
                MockResult(
                    title="Paper 2",
                    summary="Summary 2",
                    authors=["Author 3"],
                    entry_id="https://arxiv.org/abs/9876.54321",
                ),
            ]

    monkeypatch.setattr(arxiv, "Search", MockSearch)


def test_fetch_arxiv_articles(mock_arxiv_search):
    query = "machine learning"
    articles = fetch_arxiv_articles(query, max_results=2)

    assert len(articles) == 2

    assert articles[0]["title"] == "Paper 1"
    assert articles[0]["summary"] == "Summary 1"
    assert articles[0]["authors"] == "Author 1, Author 2"
    assert articles[0]["url"] == "https://arxiv.org/abs/1234.56789"

    assert articles[1]["title"] == "Paper 2"
    assert articles[1]["summary"] == "Summary 2"
    assert articles[1]["authors"] == "Author 3"
    assert articles[1]["url"] == "https://arxiv.org/abs/9876.54321"
