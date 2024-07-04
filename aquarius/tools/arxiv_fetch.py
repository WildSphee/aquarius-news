from datetime import datetime, timedelta
from typing import Dict, List

import arxiv


def fetch_arxiv_articles(query: str, max_results: int = 5) -> List[Dict[str, str]]:
    """
    Fetches arXiv articles about a certain topic over the last week.

    Attributes:
        query (str): The paper topics to search for.
        max_results (int): The maximum number of articles to fetch. Default 5.

    Returns:
        List[Dict[str, str]]: A list of dictionaries containing article details.
    """
    # last 7 days
    now = datetime.now()
    one_week_ago = now - timedelta(days=7)

    start_date = one_week_ago.strftime("%Y%m%d%H%M%S")
    end_date = now.strftime("%Y%m%d%H%M%S")
    search_query = f"({query}) AND submittedDate:[{start_date} TO {end_date}]"

    # Fetch articles
    search = arxiv.Search(
        query=search_query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate,
    )

    articles = []
    for result in search.results():
        articles.append(
            {
                "title": result.title,
                "summary": result.summary,
                "authors": ", ".join([author.name for author in result.authors]),
                "url": result.entry_id,
            }
        )

    return articles
