from __future__ import annotations

from dataclasses import dataclass

import requests
import streamlit as st
from bs4 import BeautifulSoup

TIMEOUT = 10  # seconds per HTTP request

# ---------------------------------------------------------------------------
# Data models
# ---------------------------------------------------------------------------

@dataclass
class Quote:
    text: str
    author: str
    tags: str


@dataclass
class Book:
    title: str
    price: str
    rating: str
    availability: str


@dataclass
class HNStory:
    rank: int
    title: str
    score: int
    comments: int
    url: str


# ---------------------------------------------------------------------------
# Scrapers
# ---------------------------------------------------------------------------

RATING_MAP = {
    "One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5,
}


def scrape_quotes(max_results: int = 20) -> list[Quote]:
    """Scrape quotes from quotes.toscrape.com (paginates as needed)."""
    results: list[Quote] = []
    page = 1
    while len(results) < max_results:
        try:
            r = requests.get(
                f"http://quotes.toscrape.com/page/{page}/", timeout=TIMEOUT
            )
            r.raise_for_status()
        except requests.RequestException as exc:
            raise RuntimeError(f"Failed to fetch quotes page {page}: {exc}") from exc

        soup = BeautifulSoup(r.text, "html.parser")
        items = soup.select("div.quote")
        if not items:
            break  # no more pages

        for item in items:
            if len(results) >= max_results:
                break
            text_el = item.select_one("span.text")
            author_el = item.select_one("small.author")
            tag_els = item.select("a.tag")
            results.append(
                Quote(
                    text=text_el.get_text(strip=True) if text_el else "",
                    author=author_el.get_text(strip=True) if author_el else "Unknown",
                    tags=", ".join(t.get_text(strip=True) for t in tag_els),
                )
            )
        page += 1

    return results


def scrape_books(max_results: int = 20) -> list[Book]:
    """Scrape books from books.toscrape.com (paginates as needed)."""
    results: list[Book] = []
    page = 1
    while len(results) < max_results:
        url = (
            "http://books.toscrape.com/catalogue/page-{}.html".format(page)
            if page > 1
            else "http://books.toscrape.com/"
        )
        try:
            r = requests.get(url, timeout=TIMEOUT)
            r.raise_for_status()
        except requests.RequestException as exc:
            raise RuntimeError(f"Failed to fetch books page {page}: {exc}") from exc

        soup = BeautifulSoup(r.text, "html.parser")
        items = soup.select("article.product_pod")
        if not items:
            break

        for item in items:
            if len(results) >= max_results:
                break
            title_el = item.select_one("h3 > a")
            price_el = item.select_one("p.price_color")
            rating_el = item.select_one("p.star-rating")
            avail_el = item.select_one("p.availability")

            rating_word = (
                rating_el["class"][1] if rating_el and len(rating_el["class"]) > 1 else "One"
            )
            stars = RATING_MAP.get(rating_word, 0)

            results.append(
                Book(
                    title=title_el["title"] if title_el else "Unknown",
                    price=price_el.get_text(strip=True) if price_el else "N/A",
                    rating="★" * stars + "☆" * (5 - stars),
                    availability=(
                        avail_el.get_text(strip=True) if avail_el else "Unknown"
                    ),
                )
            )
        page += 1

    return results


def scrape_hackernews(max_results: int = 30) -> list[HNStory]:
    """Scrape top stories from Hacker News front page."""
    try:
        r = requests.get("https://news.ycombinator.com/", timeout=TIMEOUT)
        r.raise_for_status()
    except requests.RequestException as exc:
        raise RuntimeError(f"Failed to fetch Hacker News: {exc}") from exc

    soup = BeautifulSoup(r.text, "html.parser")
    title_rows = soup.select("tr.athing")
    results: list[HNStory] = []

    for row in title_rows[:max_results]:
        rank_el = row.select_one("span.rank")
        title_el = row.select_one("span.titleline > a")

        # Next sibling row has score + comments
        subtext_row = row.find_next_sibling("tr")
        score = 0
        comments = 0
        if subtext_row:
            score_el = subtext_row.select_one("span.score")
            comment_els = subtext_row.select("a")
            if score_el:
                score = int("".join(filter(str.isdigit, score_el.get_text())))
            # Last <a> in subtext usually contains comment count
            for a in reversed(comment_els):
                txt = a.get_text(strip=True)
                if "comment" in txt:
                    comments = int("".join(filter(str.isdigit, txt)) or "0")
                    break

        results.append(
            HNStory(
                rank=int("".join(filter(str.isdigit, rank_el.get_text())) or "0")
                if rank_el
                else len(results) + 1,
                title=title_el.get_text(strip=True) if title_el else "Unknown",
                score=score,
                comments=comments,
                url=title_el["href"] if title_el else "#",
            )
        )

    return results


# ---------------------------------------------------------------------------
# Streamlit UI
# ---------------------------------------------------------------------------

SITE_OPTIONS = {
    "Quotes (quotes.toscrape.com)": "quotes",
    "Books (books.toscrape.com)": "books",
    "Hacker News (news.ycombinator.com)": "hn",
}


def render_quotes(quotes: list[Quote]) -> None:
    st.subheader(f"💬 Quotes — {len(quotes)} results")
    for q in quotes:
        with st.container(border=True):
            st.markdown(f"> {q.text}")
            st.caption(f"— **{q.author}** | Tags: {q.tags or 'none'}")


def render_books(books: list[Book]) -> None:
    st.subheader(f"📚 Books — {len(books)} results")
    st.dataframe(
        [
            {
                "Title": b.title,
                "Price": b.price,
                "Rating": b.rating,
                "Availability": b.availability,
            }
            for b in books
        ],
        use_container_width=True,
        hide_index=True,
    )


def render_hn(stories: list[HNStory]) -> None:
    st.subheader(f"🔥 Hacker News — {len(stories)} stories")
    st.dataframe(
        [
            {
                "Rank": s.rank,
                "Title": s.title,
                "Score": s.score,
                "Comments": s.comments,
                "URL": s.url,
            }
            for s in stories
        ],
        use_container_width=True,
        hide_index=True,
        column_config={
            "URL": st.column_config.LinkColumn("URL", display_text="Open ↗"),
        },
    )


def main() -> None:
    st.set_page_config(page_title="Web Scraper", page_icon="🕷️", layout="wide")
    st.title("🕷️ Interactive Web Scraper")

    # --- Sidebar controls ---
    st.sidebar.header("⚙️ Scrape Settings")

    selected_labels = st.sidebar.multiselect(
        "Sites to scrape",
        options=list(SITE_OPTIONS.keys()),
        default=list(SITE_OPTIONS.keys())[:1],
    )

    max_results = st.sidebar.slider(
        "Max results per site", min_value=5, max_value=50, value=10, step=5
    )

    scrape_btn = st.sidebar.button("🚀 Scrape", type="primary", use_container_width=True)

    st.sidebar.markdown("---")
    st.sidebar.caption(
        "Sites used for scraping practice:\n"
        "- [quotes.toscrape.com](http://quotes.toscrape.com)\n"
        "- [books.toscrape.com](http://books.toscrape.com)\n"
        "- [Hacker News](https://news.ycombinator.com)"
    )

    if not selected_labels:
        st.info("Select at least one site from the sidebar, then click **Scrape**.")
        return

    if not scrape_btn:
        st.info("Configure settings in the sidebar and click **🚀 Scrape** to begin.")
        return

    selected_keys = [SITE_OPTIONS[lbl] for lbl in selected_labels]

    for key in selected_keys:
        if key == "quotes":
            with st.spinner("Scraping quotes.toscrape.com…"):
                try:
                    quotes = scrape_quotes(max_results)
                    render_quotes(quotes)
                except RuntimeError as exc:
                    st.error(f"Quotes scraping failed: {exc}")

        elif key == "books":
            with st.spinner("Scraping books.toscrape.com…"):
                try:
                    books = scrape_books(max_results)
                    render_books(books)
                except RuntimeError as exc:
                    st.error(f"Books scraping failed: {exc}")

        elif key == "hn":
            with st.spinner("Scraping Hacker News…"):
                try:
                    stories = scrape_hackernews(max_results)
                    render_hn(stories)
                except RuntimeError as exc:
                    st.error(f"Hacker News scraping failed: {exc}")


if __name__ == "__main__":
    main()
