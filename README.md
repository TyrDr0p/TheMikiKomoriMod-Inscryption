# The Miki Komori Mod - Inscryption Card Generator

This repository includes a Tkinter tool for creating `.jldr2` JSON files for Inscryption card mods. It can create standard card definitions and talking card definitions.

## Download The App

Prebuilt executables are published by GitHub Actions on the rolling prerelease named `Latest automated build`.

1. Open the repository's **Releases** page.
2. Download the package for your operating system:
   - `InscryptionCardGenerator-windows-x64.zip`
   - `InscryptionCardGenerator-linux-x64.tar.gz`
   - `InscryptionCardGenerator-macos-arm64.zip` or `InscryptionCardGenerator-macos-x64.zip`
3. Extract the package.
4. Run `InscryptionCardGenerator` or `InscryptionCardGenerator.exe`.

On macOS, you may need to allow the app in **System Settings > Privacy & Security** because the generated executable is not code-signed.

## Run From Source

Python 3.10 or newer is recommended.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python "1 Card Generator/Card_Generator.py"
```

On Windows, activate the virtual environment with `.venv\Scripts\activate` instead of `source .venv/bin/activate`.

Pillow is used only for portrait previews. The app can still generate `.jldr2` files without it, but selected portraits will not preview.

## Create A Card File

1. Open the **Card Editor** tab.
2. Enter a mod prefix and a unique card ID.
3. Fill in the display name, description, stats, costs, categories, traits, sigils, and optional portrait path.
4. Select **Generate .jldr2 File**.
5. Save the file into the folder expected by your Inscryption mod setup.

The generated file uses the card name format `Prefix_CardID` when a mod prefix is provided.

## Create A Talking Card File

1. Open the **Talking Card Editor** tab.
2. Enter the full target card ID.
3. Choose the required face, eye, mouth, and emission sprites.
4. Add at least one dialogue event with main dialogue lines.
5. Select **Generate .jldr2 File**.

The tool saves talking card data as a `.jldr2` file using the JSON Card Loader 2 format.

## Build Locally

Install the build dependencies, then run the helper script:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-build.txt
python scripts/build_executable.py
```

On Windows, activate the virtual environment with `.venv\Scripts\activate` instead of `source .venv/bin/activate`.

The script writes PyInstaller output to `dist/` and a compressed release package to `release/`.

The helper uses:

- `--onefile`
- `--windowed`
- `--noconfirm`
- `--clean`
- `--strip` on Linux and macOS
- UPX automatically on Windows and Linux when `upx` is available on `PATH`

## Automated Builds

GitHub Actions builds Windows, Linux, and macOS packages on every push to `main` and when the workflow is run manually. Successful builds are uploaded as workflow artifacts and attached to the rolling prerelease.

## Repository Folders

- `1 Card Generator/` - the Python card generator app.
- `Artwork/` - exported artwork files.
- `Artwork Projects/` - source artwork projects.
- `Cards/` - generated or curated card files.
- `Sigils/` - sigil-related files.
- `Notes/` - project notes.
