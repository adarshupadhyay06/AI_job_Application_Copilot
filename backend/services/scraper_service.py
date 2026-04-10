from __future__ import annotations

import re


def scrape_job_post(url: str) -> dict[str, str]:
    import requests
    from bs4 import BeautifulSoup

    response = requests.get(
        url,
        timeout=20,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0 Safari/537.36"
            )
        },
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    title = (soup.title.string or "").strip() if soup.title else "Job Opening"

    paragraphs = [element.get_text(" ", strip=True) for element in soup.find_all(["p", "li", "h1", "h2", "h3"])]
    text = "\n".join(chunk for chunk in paragraphs if chunk)
    text = re.sub(r"\n{2,}", "\n", text).strip()

    return {
        "title": title,
        "content": text[:15000],
    }
