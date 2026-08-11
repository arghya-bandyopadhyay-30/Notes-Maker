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