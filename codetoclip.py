import sys
import os
import pyperclip

def get_files_recursively(paths_to_scan):
    """
    Generates (file_path, relative_path_for_display) for all files
    in the given paths, recursing into directories.
    """
    for item_path in paths_to_scan:
        item_path = os.path.abspath(item_path) # Ensure absolute path

        if os.path.isfile(item_path):
            # For a single file dropped, its relative path is just its name
            relative_name = os.path.basename(item_path)
            yield item_path, relative_name.replace(os.sep, '/')
        elif os.path.isdir(item_path):
            # For a directory, walk through it
            # The base for relative paths is the directory itself
            base_dir_for_relpath = item_path
            for root, _, files in os.walk(item_path):
                for filename in files:
                    full_path = os.path.join(root, filename)
                    # Calculate path relative to the *dropped* directory
                    relative_path = os.path.relpath(full_path, base_dir_for_relpath)
                    yield full_path, relative_path.replace(os.sep, '/')
        else:
            print(f"Warning: '{item_path}' is not a file or directory. Skipping.")

def main():
    if len(sys.argv) < 2:
        print("Usage: Drag and drop files/folders onto this script.")
        print("Or run: python codetoclip.py <file1> <folder1> ...")
        input("Press Enter to exit...") # Keep window open if run directly
        return

    dropped_items = sys.argv[1:]
    all_formatted_content = []
    total_files_processed = 0
    total_size_bytes = 0

    print(f"Processing {len(dropped_items)} dropped item(s)...")

    # Define common text file extensions (add more if needed)
    # This is a simple heuristic to avoid trying to read large binary files.
    # You can remove this filter if you want to try reading everything.
    text_extensions = {
        '.txt', '.py', '.js', '.jsx', '.ts', '.tsx', '.html', '.htm', '.css', '.scss', '.sass',
        '.json', '.xml', '.yaml', '.yml', '.md', '.rst', '.java', '.c', '.cpp', '.h', '.hpp',
        '.cs', '.go', '.php', '.rb', '.swift', '.kt', '.kts', '.sh', '.bash', '.zsh', '.ps1',
        '.sql', '.ini', '.cfg', '.conf', '.toml', '.dockerfile', 'docker-compose.yml',
        '.gitignore', '.gitattributes', '.editorconfig', '.env', # Common dotfiles
        # Add extensions for your common project files
    }
    # Files to always ignore by name (case-insensitive)
    ignore_filenames = {
        '.ds_store', 'thumbs.db',
    }
    # Directories to always ignore by name (case-insensitive)
    ignore_dirnames = {
        '.git', 'node_modules', '__pycache__', '.vscode', '.idea',
        'venv', 'env', '.env', # Python virtual environments
        'build', 'dist', 'target', # Common build output folders
    }

    for file_path, display_path in get_files_recursively(dropped_items):
        # Skip based on directory name in the path
        path_parts = file_path.lower().split(os.sep)
        if any(part in ignore_dirnames for part in path_parts):
            # print(f"Skipping due to ignored directory in path: {display_path}")
            continue

        # Skip based on filename
        if os.path.basename(file_path).lower() in ignore_filenames:
            # print(f"Skipping ignored filename: {display_path}")
            continue

        # Optional: Skip based on extension if it's likely not text
        # _, ext = os.path.splitext(file_path.lower())
        # if ext not in text_extensions and ext: # Check if ext is not empty (for files like 'LICENSE')
        #     print(f"Skipping non-text file (by extension): {display_path} (ext: {ext})")
        #     continue
        # For LLM context, it might be better to try reading and catch errors
        # So, let's try to read and handle errors instead of strict extension filtering

        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            file_size = os.path.getsize(file_path)
            # Limit file size to avoid huge clipboard content (e.g., 1MB)
            max_file_size_mb = 1
            if file_size > max_file_size_mb * 1024 * 1024:
                print(f"Skipping large file: {display_path} ({file_size / (1024*1024):.2f} MB > {max_file_size_mb} MB)")
                continue


            formatted_file_content = f"//{display_path}\n{content.strip()}\n"
            all_formatted_content.append(formatted_file_content)
            total_files_processed += 1
            total_size_bytes += len(content.encode('utf-8')) # Approximate size of content being copied
            print(f"Added: {display_path}")

        except FileNotFoundError:
            print(f"Error: File not found '{file_path}'. Skipping.")
        except UnicodeDecodeError:
            print(f"Warning: Could not decode '{display_path}' as UTF-8. Skipping (likely binary).")
        except Exception as e:
            print(f"Error reading file '{file_path}': {e}. Skipping.")

    if not all_formatted_content:
        print("No text files found or processed.")
        input("Press Enter to exit...")
        return

    final_output = "\n".join(all_formatted_content)

    try:
        pyperclip.copy(final_output)
        print(f"\n--- Successfully processed {total_files_processed} file(s) ---")
        print(f"Total content size: {total_size_bytes / 1024:.2f} KB")
        print("Content has been copied to your clipboard!")
    except pyperclip.PyperclipException as e:
        print(f"\n--- Processed {total_files_processed} file(s) but failed to copy to clipboard ---")
        print(f"Error: {e}")
        print("You may need to install a copy/paste mechanism for your system.")
        print("For Linux, try: sudo apt-get install xclip or sudo apt-get install xsel")
        print("\nFull content output (first 1000 chars):\n")
        print(final_output[:1000] + "..." if len(final_output) > 1000 else final_output)

    input("Press Enter to exit...") # Keep window open to see messages

if __name__ == "__main__":
    main()
