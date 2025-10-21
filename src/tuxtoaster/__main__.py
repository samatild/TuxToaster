import sys
from importlib.metadata import PackageNotFoundError, version as pkg_version
from .main import main as app_main


def _print_help() -> None:
    print(
        "Tux Toaster - All-in-one Linux stress and benchmarking toolkit\n\n"
        "Usage: tuxtoaster [--help] [--version]\n\n"
        "This is an interactive console application. Running without arguments\n"
        "opens a dynamic menu you can navigate with the keyboard.\n\n"
        "Repository: https://github.com/samatild/tuxtoaster"
    )


def _get_version() -> str:
    try:
        return pkg_version("tuxtoaster")
    except PackageNotFoundError:
        try:
            from . import __version__  # type: ignore
            return __version__  # type: ignore
        except Exception:
            return "unknown"


def _cli_entry() -> None:
    args = sys.argv[1:]

    if not args:
        app_main()
        return

    if args[0] in ("-h", "--help"):
        _print_help()
        return

    if args[0] in ("-V", "--version"):
        print(_get_version())
        return

    _print_help()
    sys.exit(2)


if __name__ == "__main__":
    _cli_entry()


def main() -> None:
    # Entry point used by console_scripts
    _cli_entry()

