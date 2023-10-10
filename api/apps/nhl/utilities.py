import requests
from contextlib import suppress
from typing import Union

def download_url(url: str) -> Union[str, dict]:
    s = requests.Session()
    s.headers.update({
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/109.0",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Referer": "http://www.google.com/"
    })
    with suppress(requests.exceptions.ConnectionError):
        r = s.get(url)
    with suppress(requests.JSONDecodeError):
            return r.json()
    return r.text