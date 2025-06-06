# CodeToClip

CodeToClip is a Python script that merges the content of multiple files and/or directories into a single text block and copies it to your clipboard. This is useful for quickly grabbing code snippets, configurations, or any text-based content from various files to paste into LLMs, documents, or other applications.

## Features

-   **Recursive File Discovery:** Scans through specified directories to find all files.
-   **Clipboard Integration:** Copies the combined text content directly to the clipboard using `pyperclip`.
-   **Relative Path Headers:** Each file's content is preceded by a comment line indicating its relative path (e.g., `//folder/file.py`).
-   **Configurable Filtering:**
    -   Ignores common non-project directories like `.git`, `node_modules`, `__pycache__`, `venv`, `build`, `dist`, etc.
    -   Ignores common system files like `.DS_Store` and `Thumbs.db`.
    -   Skips files that appear to be binary or cause decoding errors.
    -   Allows customization of ignored directory/file names and file extensions directly within the script.
-   **File Size Limit:** Skips individual files larger than a configurable size (default 1MB) to prevent excessive clipboard content.
-   **User Feedback:** Prints information about processed files, skipped files, total content size, and clipboard status.
-   **Cross-Platform (with dependencies):** Works on Windows, macOS, and Linux, provided Python and clipboard utilities are set up.

## Usage

There are two main ways to use CodeToClip:

1.  **Drag and Drop (Windows/macOS):**
    *   Save the `codetoclip.py` script to a known location.
    *   Select one or more files and/or folders in your file explorer.
    *   Drag them directly onto the `codetoclip.py` script icon.
    *   A terminal window will open, show the progress, and the combined content will be copied to your clipboard.

2.  **Command Line:**
    *   Open your terminal or command prompt.
    *   Navigate to the directory where you saved `codetoclip.py` or ensure it's in your system's PATH.
    *   Run the script with the paths to your desired files and/or folders as arguments:
        ```bash
        python codetoclip.py /path/to/your/file.txt /path/to/your/folder/
        ```
    *   The script will process the files, and the combined content will be copied to your clipboard.

## Dependencies

-   **Python 3:** The script is written for Python 3.
-   **`pyperclip` library:** Used for clipboard operations.

You can install `pyperclip` using pip:
```bash
pip install pyperclip
```

### Clipboard System Dependencies

`pyperclip` relies on system utilities for clipboard access. You might need to install them if you encounter issues:

-   **Linux:**
    ```bash
    sudo apt-get install xclip
    # or
    sudo apt-get install xsel
    ```
-   **Windows & macOS:** These usually work out of the box.

If copying to the clipboard fails, the script will print the first 1000 characters of the combined content to the terminal as a fallback.

## Configuration

You can customize the behavior of the script by editing these lists/variables at the beginning of the `main()` function in `codetoclip.py`:

-   `text_extensions`: A set of file extensions to prioritize (currently, the script attempts to read all files and handles errors, but this list exists if you want to reinstate stricter extension filtering).
-   `ignore_filenames`: A set of exact filenames to ignore (case-insensitive).
-   `ignore_dirnames`: A set of directory names to ignore (case-insensitive). Any directory in the path matching these will cause contained files to be skipped.
-   `max_file_size_mb`: An integer defining the maximum size in megabytes for an individual file to be included.

## License

This project is licensed under the terms of the LICENSE file.
