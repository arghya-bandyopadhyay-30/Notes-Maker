import re
from typing import Final
from urllib.parse import parse_qs, urlparse

from .string_constants import (
    YOUTUBE_EMBED_HOSTS,
    YOUTUBE_PATH_PATTERN,
    YOUTUBE_SHORT_HOSTS,
    YOUTUBE_SUBDOMAIN_PREFIXES,
    YOUTUBE_VIDEO_ID_PATTERN,
    YOUTUBE_WATCH_HOSTS,
)

VIDEO_ID_PATTERN: Final[re.Pattern[str]] = re.compile(
    YOUTUBE_VIDEO_ID_PATTERN
)

PATH_PATTERN: Final[re.Pattern[str]] = re.compile(
    YOUTUBE_PATH_PATTERN
)


def normalise_host(host: str) -> str:
    host = host.lower().strip().rstrip(".")

    if ":" in host:
        host = host.split(":", 1)[0]

    for prefix in YOUTUBE_SUBDOMAIN_PREFIXES:
        if host.startswith(prefix):
            host = host[len(prefix)]
            return host

    return host


def extract_video_id(url: str) -> str:
    if not isinstance(url, str):
        raise ValueError("YouTube URL must be a string.")

    url = url.strip()

    if not url:
        raise ValueError("YouTube URL must not be empty.")

    if (
        len(url) >= 2
        and url[0] == url[-1]
        and url[0] in {'"', "'"}
    ):
        url = url[1:-1].strip()

    if not url:
        raise ValueError("YouTube URL must not be empty.")

    if VIDEO_ID_PATTERN.fullmatch(url):
        return url

    parsed = urlparse(url)

    if not parsed.netloc:
        raise ValueError(
            f"Invalid YouTube URL. Missing hostname: {url}"
        )

    host = normalise_host(parsed.netloc)

    if host == YOUTUBE_WATCH_HOSTS and parsed.path == "/watch":
        video_id = parse_qs(parsed.query).get("v", [None])[0]

        if video_id and VIDEO_ID_PATTERN.fullmatch(video_id):
            return video_id

    if host == YOUTUBE_SHORT_HOSTS:
        video_id = parsed.path.strip("/").split("/")[0]

        if video_id and VIDEO_ID_PATTERN.fullmatch(video_id):
            return video_id

    if host in YOUTUBE_EMBED_HOSTS:
        match = PATH_PATTERN.match(parsed.path)

        if match:
            return match.group(1)

    raise ValueError(
        f"Could not extract a valid YouTube video ID from: {url}"
    )