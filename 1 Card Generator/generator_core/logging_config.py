from __future__ import annotations

import argparse
import logging
import logging.handlers
import platform
import sys
import tempfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from .schemas import project_root


LOG_NAME = "InscryptionCardGenerator"


@dataclass(frozen=True)
class CliArgs:
    debug: bool = False


def parse_cli_args(argv=None) -> CliArgs:
    parser = argparse.ArgumentParser(description="Run the Inscryption JSONCardLoader generator.")
    parser.add_argument("--debug", action="store_true", help="Enable verbose console and file debug logging.")
    args = parser.parse_args(argv)
    return CliArgs(debug=args.debug)


def runtime_base_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return project_root()


def default_log_dir() -> Path:
    return runtime_base_dir() / "logs"


def debug_log_path(log_dir: Path | None = None, timestamp: datetime | None = None) -> Path:
    timestamp = timestamp or datetime.now()
    return (log_dir or default_log_dir()) / f"{LOG_NAME}-debug-{timestamp:%Y%m%d-%H%M%S}.log"


def writable_debug_log_path(log_dir: Path | None = None) -> Path:
    preferred = debug_log_path(log_dir)
    for path in (preferred, debug_log_path(Path.cwd() / "logs"), debug_log_path(Path(tempfile.gettempdir()))):
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("a", encoding="utf-8"):
                pass
            return path
        except OSError:
            continue
    raise OSError("Unable to create a debug log file in the app, current, or temp directory.")


def configure_debug_logging(enabled: bool, log_dir: Path | None = None, console: bool = True) -> Path | None:
    root_logger = logging.getLogger()
    for handler in list(root_logger.handlers):
        root_logger.removeHandler(handler)
        handler.close()

    if not enabled:
        root_logger.addHandler(logging.NullHandler())
        return None

    log_path = writable_debug_log_path(log_dir)
    root_logger.setLevel(logging.DEBUG)

    verbose_formatter = logging.Formatter(
        "%(asctime)s.%(msecs)03d %(levelname)-8s "
        "pid=%(process)d thread=%(threadName)s "
        "%(name)s:%(lineno)d %(funcName)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    console_formatter = logging.Formatter("%(levelname)s: %(message)s")

    file_handler = logging.handlers.RotatingFileHandler(
        log_path,
        maxBytes=10 * 1024 * 1024,
        backupCount=3,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(verbose_formatter)

    root_logger.addHandler(file_handler)
    console_stream = (sys.stdout or sys.stderr) if console else None
    if console_stream:
        console_handler = logging.StreamHandler(console_stream)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(console_formatter)
        root_logger.addHandler(console_handler)
    logging.captureWarnings(True)

    logger = logging.getLogger(__name__)
    logger.info("Debug logging enabled. Log file: %s", log_path)
    logger.debug("Runtime base directory: %s", runtime_base_dir())
    logger.debug("Project/resource root: %s", project_root())
    logger.debug("Python executable: %s", sys.executable)
    logger.debug("Python version: %s", sys.version.replace("\n", " "))
    logger.debug("Platform: %s", platform.platform())
    logger.debug("Command line: %s", sys.argv)
    logger.debug("Current working directory: %s", Path.cwd())
    logger.debug("Frozen executable: %s", getattr(sys, "frozen", False))
    return log_path
