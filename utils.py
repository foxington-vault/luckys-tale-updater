import requests


def user_agent(ref: str) -> dict[str, str]:
    return {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5)"
            "AppleWebKit/537.36 (KHTML, like Gecko)"
            "Chrome/45.0.2454.101 Safari/537.36"
        ),
        "referrer": ref
    }


rs = requests.Session()


def fetch_url(url: str):
    return rs.get(url, headers=user_agent)
