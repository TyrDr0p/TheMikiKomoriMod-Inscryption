# The Miki Komori Mod - Inscryption Card Generator

This repository includes a Tkinter tool for creating JSONCardLoader `.jldr2` files for Inscryption card mods. It can create Cards, Sigils, Tribes, and Talking Cards, with local JSON Schema validation before save.

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

Pillow is used only for image previews where available. JSON generation and schema validation use `jsonschema`.

## Create JSONCardLoader Files

Open the tab for the output type you want:

- **Cards** saves card definitions as `.jldr2`.
- **Sigils** saves sigil definitions as `_sigil.jldr2`.
- **Tribes** saves tribe definitions as `_tribe.jldr2`.
- **Talking Cards** saves talking card definitions as `_talk.jldr2`.

Each tab includes a form, **Reset Form**, **Preview / Validate**, **Save**, and a read-only JSON preview. The app validates against checked-in JSONCardLoader schema fixtures before saving and shows any schema errors in the preview/status area.

For Cards, enter the unprefixed card ID and optional mod prefix. The generated JSON keeps `name` and `modPrefix` separate, matching JSONCardLoader's card schema.

Enum-backed fields such as meta categories, abilities, special abilities, tribes, traits, appearance behaviours, gem costs, temples, emotions, and talking-card event names are selectable with checkboxes or dropdowns. The option lists are aligned with the SaxbyModEnums wiki where those enums apply, and described enum values show those descriptions as hover tooltips.

For Sigils, the **Ability Behaviour Builder** can generate common Configils trigger/action structures without hand-writing JSON. Use the advanced JSON editor only when you need fields outside the guided templates.

For Talking Cards, nested schema-backed JSON editors are included for advanced structures such as emotions and dialogue events. Use the dropdown template controls to add common emotion and dialogue entries, and use **Validate Nested JSON** inside those editors when changing nested data directly.

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

Run the local checks with:

```bash
python -m py_compile "1 Card Generator/Card_Generator.py"
python -m unittest discover -s tests
```

## Automated Builds

GitHub Actions builds Windows, Linux, and macOS packages on every push to `main` and when the workflow is run manually. Successful builds are uploaded as workflow artifacts and attached to the rolling prerelease.

## Repository Folders

- `1 Card Generator/` - the Python card generator app.
- `schemas/jsoncardloader/` - local JSONCardLoader schema fixtures used for validation.
- `Artwork/` - exported artwork files.
- `Artwork Projects/` - source artwork projects.
- `Cards/` - generated or curated card files.
- `Sigils/` - sigil-related files.
- `Notes/` - project notes.
