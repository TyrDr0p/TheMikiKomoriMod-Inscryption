from __future__ import annotations

import argparse
import os
import platform
import shutil
import subprocess
import sys
import tarfile
import zipfile
from pathlib import Path


APP_NAME = "InscryptionCardGenerator"
ROOT_DIR = Path(__file__).resolve().parents[1]
ENTRY_POINT = ROOT_DIR / "1 Card Generator" / "Card_Generator.py"
BUILD_DIR = ROOT_DIR / "build" / "pyinstaller"
PYINSTALLER_CACHE_DIR = ROOT_DIR / "build" / "pyinstaller-cache"
DIST_DIR = ROOT_DIR / "dist"
RELEASE_DIR = ROOT_DIR / "release"


def current_os_tag() -> str:
    system = platform.system().lower()
    if system == "windows":
        return "windows"
    if system == "darwin":
        return "macos"
    if system == "linux":
        return "linux"
    return system or "unknown"


def current_arch_tag() -> str:
    machine = platform.machine().lower()
    if machine in {"amd64", "x86_64"}:
        return "x64"
    if machine in {"arm64", "aarch64"}:
        return "arm64"
    return machine.replace(" ", "-") or "unknown"


def pyinstaller_command() -> list[str]:
    os_tag = current_os_tag()
    command = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--onefile",
        "--windowed",
        "--noconfirm",
        "--clean",
        "--name",
        APP_NAME,
        "--distpath",
        str(DIST_DIR),
        "--workpath",
        str(BUILD_DIR),
        "--specpath",
        str(ROOT_DIR),
        str(ENTRY_POINT),
    ]

    if os_tag in {"linux", "macos"}:
        command.append("--strip")

    if os_tag == "macos":
        command.append("--noupx")

    return command


def built_app_path() -> Path:
    os_tag = current_os_tag()
    if os_tag == "windows":
        return DIST_DIR / f"{APP_NAME}.exe"

    mac_app = DIST_DIR / f"{APP_NAME}.app"
    if os_tag == "macos" and mac_app.exists():
        return mac_app

    return DIST_DIR / APP_NAME


def package_name() -> str:
    extension = "tar.gz" if current_os_tag() == "linux" else "zip"
    return f"{APP_NAME}-{current_os_tag()}-{current_arch_tag()}.{extension}"


def zip_path(source: Path, destination: Path) -> None:
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        if source.is_dir():
            for file_path in sorted(source.rglob("*")):
                archive.write(file_path, file_path.relative_to(source.parent))
        else:
            archive.write(source, source.name)


def tar_path(source: Path, destination: Path) -> None:
    with tarfile.open(destination, "w:gz") as archive:
        archive.add(source, arcname=source.name)


def package_build(source: Path) -> Path:
    RELEASE_DIR.mkdir(exist_ok=True)
    destination = RELEASE_DIR / package_name()
    if destination.exists():
        destination.unlink()

    if destination.suffix == ".zip":
        zip_path(source, destination)
    else:
        tar_path(source, destination)

    return destination


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the Inscryption card generator executable.")
    parser.add_argument("--skip-package", action="store_true", help="Build the executable without creating a release archive.")
    args = parser.parse_args()

    if not ENTRY_POINT.exists():
        print(f"Entry point not found: {ENTRY_POINT}", file=sys.stderr)
        return 1

    if shutil.which("upx") and current_os_tag() in {"windows", "linux"}:
        print("UPX detected; PyInstaller will use it automatically.")
    elif current_os_tag() in {"windows", "linux"}:
        print("UPX not found; building without UPX compression.")

    env = os.environ.copy()
    env.setdefault("PYINSTALLER_CONFIG_DIR", str(PYINSTALLER_CACHE_DIR))
    env.setdefault("XDG_CACHE_HOME", str(ROOT_DIR / "build" / "cache"))

    subprocess.run(pyinstaller_command(), cwd=ROOT_DIR, env=env, check=True)

    app_path = built_app_path()
    if not app_path.exists():
        print(f"Expected build output not found: {app_path}", file=sys.stderr)
        return 1

    if args.skip_package:
        print(f"Built executable: {app_path}")
        return 0

    package_path = package_build(app_path)
    print(f"Built executable: {app_path}")
    print(f"Created package: {package_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
