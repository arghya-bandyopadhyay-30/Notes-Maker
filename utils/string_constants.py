YOUTUBE = "youtube"

URL = "url"

LANGUAGE = "language"

OUTPUT_DIRECTORY = "output_directory"

MODELS = "models"

TRANSCRIPT = "transcript"

VALIDATOR = "validator"

YOUTUBE_VIDEO_ID_PATTERN = r"^[A-Za-z0-9_-]{11}$"

YOUTUBE_PATH_PATTERN = r"^/(?:shorts|embed|v)/([A-Za-z0-9_-]{11})(?:/|$)"

YOUTUBE_WATCH_HOSTS = {"youtube.com"}

YOUTUBE_SHORT_HOSTS = {"youtu.be"}

YOUTUBE_EMBED_HOSTS = {"youtube.com", "youtube-nocookie.com"}

YOUTUBE_SUBDOMAIN_PREFIXES = ("www.", "m.", "music.")

EMPTY_STRING = ""

DOT = "."

COLON = ":"

SLASH = "/"

QUOTE_CHARS = {'"', "'"}

YOUTUBE_WATCH_PATH = "/watch"

YOUTUBE_VIDEO_ID_QUERY_KEY = "v"

YOUTUBE_URL_MUST_BE_A_STRING = "YouTube URL must be a string."

YOUTUBE_URL_MUST_NOT_BE_EMPTY = "YouTube URL must not be empty."

YOUTUBE_INVALID_URL_MISSING_HOSTNAME = "Invalid YouTube URL. Missing hostname: {0}"

YOUTUBE_COULD_NOT_EXTRACT_VIDEO_ID = "Could not extract a valid YouTube video ID from: {0}"