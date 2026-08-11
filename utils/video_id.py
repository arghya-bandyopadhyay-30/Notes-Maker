import re
from typing import Callable, Final
from urllib.parse import ParseResult, parse_qs, urlparse

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
    normalised = host.lower().strip().rstrip(".")

    if ":" in normalised:
        normalised = normalised.split(":", 1)[0]

    for prefix in YOUTUBE_SUBDOMAIN_PREFIXES:
        if normalised.startswith(prefix):
            return normalised[len(prefix):]

    return normalised


def unwrap_quotes(url: str) -> str:
    if (
        len(url) >= 2
        and url[0] == url[-1]
        and url[0] in {'"', "'"}
    ):
        return url[1:-1].strip()

    return url


def extract_from_watch_url(
    host: str,
    parsed: ParseResult,
) -> str:
    if host not in YOUTUBE_WATCH_HOSTS or parsed.path != "/watch":
        return ""

    video_id = parse_qs(parsed.query).get("v", [None])[0]

    if video_id and VIDEO_ID_PATTERN.fullmatch(video_id):
        return video_id

    return ""


def extract_from_short_url(
    host: str,
    parsed: ParseResult,
) -> str:
    if host not in YOUTUBE_SHORT_HOSTS:
        return ""

    video_id = parsed.path.strip("/").split("/")[0]

    if video_id and VIDEO_ID_PATTERN.fullmatch(video_id):
        return video_id

    return ""


def extract_from_embed_path(
    host: str,
    parsed: ParseResult,
) -> str:
    if host not in YOUTUBE_EMBED_HOSTS:
        return ""

    match = PATH_PATTERN.match(parsed.path)

    if match:
        return match.group(1)

    return ""


URL_EXTRACTORS: Final[
    tuple[Callable[[str, ParseResult], str], ...]
] = (
    extract_from_watch_url,
    extract_from_short_url,
    extract_from_embed_path,
)


def extract_video_id(url: str) -> str:
    if not isinstance(url, str):
        raise ValueError("YouTube URL must be a string.")

    candidate = unwrap_quotes(url.strip())

    if not candidate:
        raise ValueError("YouTube URL must not be empty.")

    if VIDEO_ID_PATTERN.fullmatch(candidate):
        return candidate

    parsed = urlparse(candidate)

    if not parsed.netloc:
        raise ValueError(
            f"Invalid YouTube URL. Missing hostname: {candidate}"
        )

    host = normalise_host(parsed.netloc)

    video_id = next(
        (
            result
            for extractor in URL_EXTRACTORS
            for result in (extractor(host, parsed),)
            if result
        ),
        "",
    )

    if video_id:
        return video_id

    raise ValueError(
        f"Could not extract a valid YouTube video ID from: {candidate}"
    )