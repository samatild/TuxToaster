__all__ = []

# Fallback version when package metadata isn't available (e.g., in editable installs)
try:
    from importlib.metadata import version as pkg_version
    __version__ = pkg_version("tuxtoaster")
except Exception:
    __version__ = "0.0.0"

