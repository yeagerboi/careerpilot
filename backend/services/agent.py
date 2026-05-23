"""
Job Hunter Agent Service — CareerPilot

Job search priority (AGENTS.md):
  1st  JSearch (RapidAPI)  — always try first, best BD/Dhaka coverage
  2nd  Remotive            — fallback for remote roles, no API key needed
  3rd  Tavily              — fallback for local BD sites incl. bdjobs.com

Caching: Upstash Redis, TTL 7200s.
NEVER use: Firecrawl, Adzuna, SerpAPI, ScraperAPI.
"""

import os
import json
import httpx
from services.cache import get_cached_jobs, cache_jobs
from services.fit_score import compute_fit_score
from services.searcher import hybrid_search

JSEARCH_API_KEY: str = os.environ.get("JSEARCH_API_KEY", "")
TAVILY_API_KEY: str  = os.environ.get("TAVILY_API_KEY", "")


# ---------------------------------------------------------------------------
# Source 1 — JSearch (RapidAPI)
# ---------------------------------------------------------------------------

async def _search_jsearch(query: str, location: str = "") -> list[dict]:
    url = "https://jsearch.p.rapidapi.com/search"
    params = {
        "query": f"{query} {location}".strip(),
        "num_pages": "1",
        "date_posted": "month",
    }
    headers = {
        "x-rapidapi-key": JSEARCH_API_KEY,
        "x-rapidapi-host": "jsearch.p.rapidapi.com",
    }
    async with httpx.AsyncClient(timeout=15) as client:
        resp = await client.get(url, params=params, headers=headers)
        resp.raise_for_status()
        data = resp.json()

    jobs = []
    for item in data.get("data", []):
        jobs.append({
            "title":       item.get("job_title", ""),
            "company":     item.get("employer_name", ""),
            "location":    item.get("job_city", "") or item.get("job_country", ""),
            "url":         item.get("job_apply_link", ""),
            "description": item.get("job_description", "")[:1000],
            "source":      "jsearch",
        })
    return jobs


# ---------------------------------------------------------------------------
# Source 2 — Remotive (remote roles, no key)
# ---------------------------------------------------------------------------

async def _search_remotive(query: str) -> list[dict]:
    url = "https://remotive.com/api/remote-jobs"
    params = {"search": query, "limit": 10}
    async with httpx.AsyncClient(timeout=15) as client:
        resp = await client.get(url, params=params)
        resp.raise_for_status()
        data = resp.json()

    jobs = []
    for item in data.get("jobs", []):
        jobs.append({
            "title":       item.get("title", ""),
            "company":     item.get("company_name", ""),
            "location":    item.get("candidate_required_location", "Remote"),
            "url":         item.get("url", ""),
            "description": item.get("description", "")[:1000],
            "source":      "remotive",
        })
    return jobs


# ---------------------------------------------------------------------------
# Source 3 — Tavily (BD sites fallback)
# ---------------------------------------------------------------------------

async def _search_tavily(query: str, location: str = "") -> list[dict]:
    url = "https://api.tavily.com/search"
    payload = {
        "api_key": TAVILY_API_KEY,
        "query": f"{query} jobs {location} site:bdjobs.com OR linkedin.com OR glassdoor.com".strip(),
        "search_depth": "basic",
        "max_results": 10,
    }
    async with httpx.AsyncClient(timeout=15) as client:
        resp = await client.post(url, json=payload)
        resp.raise_for_status()
        data = resp.json()

    jobs = []
    for item in data.get("results", []):
        jobs.append({
            "title":       query,
            "company":     "",
            "location":    location or "Bangladesh",
            "url":         item.get("url", ""),
            "description": item.get("content", "")[:1000],
            "source":      "tavily",
        })
    return jobs


# ---------------------------------------------------------------------------
# Main agent function
# ---------------------------------------------------------------------------

async def hunt_jobs(query: str, location: str, user_id: str) -> list[dict]:
    """
    Hunt jobs with priority JSearch → Remotive → Tavily.
    Results are cached in Redis. Fit scores are computed per job.
    """
    # 1. Check cache
    cached = await get_cached_jobs(query, location)
    if cached is not None:
        return cached

    # 2. Try JSearch first
    jobs: list[dict] = []
    try:
        jobs = await _search_jsearch(query, location)
    except Exception:
        pass

    # 3. Fallback to Remotive if JSearch returned nothing
    if not jobs:
        try:
            jobs = await _search_remotive(query)
        except Exception:
            pass

    # 4. Fallback to Tavily if still nothing
    if not jobs:
        try:
            jobs = await _search_tavily(query, location)
        except Exception:
            pass

    # 5. Compute fit scores
    for job in jobs:
        try:
            result = await compute_fit_score(
                job_description=job.get("description", job.get("title", "")),
                user_id=user_id,
            )
            job["fit_score"]      = result["score"]
            job["fit_explanation"] = result["explanation"]
        except Exception:
            job["fit_score"]       = 0
            job["fit_explanation"] = ""

    # 6. Sort by fit score descending
    jobs.sort(key=lambda j: j.get("fit_score", 0), reverse=True)

    # 7. Cache results
    await cache_jobs(jobs, query, location)

    return jobs
