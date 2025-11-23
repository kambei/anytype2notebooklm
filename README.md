# Anytype to NotebookLM Converter

A simple Python script to consolidate Anytype notes (exported as Markdown) into a single Markdown file, optimized for importing into Google's NotebookLM.

## Features

- Recursively scans a directory for `.md` files.
- Merges all found files into one output file.
- Adds headers (`# Source: <filename>`) to distinguish between original notes.
- Adds separators (`---`) between notes.

## Usage

1.  **Export your Anytype notes** to a folder on your computer.
2.  **Run the script**:

    ```bash
    python anytype_to_notebooklm.py <path_to_anytype_export> <output_file.md>
    ```

    **Example:**

    ```bash
    python anytype_to_notebooklm.py "C:\Users\Me\Desktop\AnytypeExport" "C:\Users\Me\Desktop\NotebookLM_Source.md"
    ```

3.  **Upload** the resulting `NotebookLM_Source.md` to NotebookLM.

## License

MIT
