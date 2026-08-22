import re
from typing import Callable, Final
from urllib.parse import ParseResult, parse_qs, urlparse

from src.utils.formatting.strings import (
    COLON,
    DOT,
    EMPTY_STRING,
    QUOTE_CHARS,
    SLASH,
    YOUTUBE_COULD_NOT_EXTRACT_VIDEO_ID,
    YOUTUBE_EMBED_HOSTS,
    YOUTUBE_INVALID_URL_MISSING_HOSTNAME,
    YOUTUBE_PATH_PATTERN,
    YOUTUBE_SHORT_HOSTS,
    YOUTUBE_SUBDOMAIN_PREFIXES,
    YOUTUBE_URL_MUST_BE_A_STRING,
    YOUTUBE_URL_MUST_NOT_BE_EMPTY,
    YOUTUBE_VIDEO_ID_PATTERN,
    YOUTUBE_VIDEO_ID_QUERY_KEY,
    YOUTUBE_WATCH_HOSTS,
    YOUTUBE_WATCH_PATH,
)

VIDEO_ID_PATTERN: Final[re.Pattern[str]] = re.compile(
    YOUTUBE_VIDEO_ID_PATTERN
)

PATH_PATTERN: Final[re.Pattern[str]] = re.compile(
    YOUTUBE_PATH_PATTERN
)


def normalise_host(host: str) -> str:
    normalised = host.lower().strip().rstrip(DOT)

    if COLON in normalised:
        normalised = normalised.split(COLON, 1)[0]

    for prefix in YOUTUBE_SUBDOMAIN_PREFIXES:
        if normalised.startswith(prefix):
            return normalised[len(prefix):]

    return normalised


def unwrap_quotes(url: str) -> str:
    if (
        len(url) >= 2
        and url[0] == url[-1]
        and url[0] in QUOTE_CHARS
    ):
        return url[1:-1].strip()

    return url


def extract_from_watch_url(
    host: str,
    parsed: ParseResult,
) -> str:
    if host not in YOUTUBE_WATCH_HOSTS or parsed.path != YOUTUBE_WATCH_PATH:
        return EMPTY_STRING

    video_id = parse_qs(parsed.query).get(YOUTUBE_VIDEO_ID_QUERY_KEY, [None])[0]

    if video_id and VIDEO_ID_PATTERN.fullmatch(video_id):
        return video_id

    return EMPTY_STRING


def extract_from_short_url(
    host: str,
    parsed: ParseResult,
) -> str:
    if host not in YOUTUBE_SHORT_HOSTS:
        return EMPTY_STRING

    video_id = parsed.path.strip(SLASH).split(SLASH)[0]

    if video_id and VIDEO_ID_PATTERN.fullmatch(video_id):
        return video_id

    return EMPTY_STRING


def extract_from_embed_path(
    host: str,
    parsed: ParseResult,
) -> str:
    if host not in YOUTUBE_EMBED_HOSTS:
        return EMPTY_STRING

    match = PATH_PATTERN.match(parsed.path)

    if match:
        return match.group(1)

    return EMPTY_STRING


URL_EXTRACTORS: Final[
    tuple[Callable[[str, ParseResult], str], ...]
] = (
    extract_from_watch_url,
    extract_from_short_url,
    extract_from_embed_path,
)


def extract_video_id(url: str) -> str:
    if not isinstance(url, str):
        raise ValueError(YOUTUBE_URL_MUST_BE_A_STRING)

    candidate = unwrap_quotes(url.strip())

    if not candidate:
        raise ValueError(YOUTUBE_URL_MUST_NOT_BE_EMPTY)

    if VIDEO_ID_PATTERN.fullmatch(candidate):
        return candidate

    parsed = urlparse(candidate)

    if not parsed.netloc:
        raise ValueError(
            YOUTUBE_INVALID_URL_MISSING_HOSTNAME.format(candidate)
        )

    host = normalise_host(parsed.netloc)

    video_id = next(
        (
            result
            for extractor in URL_EXTRACTORS
            for result in (extractor(host, parsed),)
            if result
        ),
        EMPTY_STRING,
    )

    if video_id:
        return video_id

    raise ValueError(
        YOUTUBE_COULD_NOT_EXTRACT_VIDEO_ID.format(candidate)
    )