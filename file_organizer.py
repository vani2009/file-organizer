"""
File Organizer - Automation Script
Performs file operations: renaming, sorting, cleaning tasks.
Uses OS module, exception handling, logging, and user input.
"""

import os
import shutil
import logging
import datetime
import sys

# ─── Logging Setup ────────────────────────────────────────────────────────────
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

log_filename = os.path.join(
    log_dir,
    f"file_organizer_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# ─── File Type Categories ──────────────────────────────────────────────────────
FILE_CATEGORIES = {
    "Images":     [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
    "Documents":  [".pdf", ".doc", ".docx", ".txt", ".odt", ".rtf", ".md"],
    "Videos":     [".mp4", ".avi", ".mov", ".mkv", ".wmv", ".flv"],
    "Audio":      [".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a"],
    "Archives":   [".zip", ".tar", ".gz", ".rar", ".7z"],
    "Code":       [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".ts"],
    "Data":       [".csv", ".json", ".xml", ".xlsx", ".sql"],
    "Others":     []
}


def get_category(extension: str) -> str:
    """Return the category folder name for a given file extension."""
    ext = extension.lower()
    for category, extensions in FILE_CATEGORIES.items():
        if ext in extensions:
            return category
    return "Others"


# ─── Operations ───────────────────────────────────────────────────────────────

def sort_files(target_dir: str) -> None:
    """Sort files in target_dir into category sub-folders."""
    logger.info(f"Starting SORT operation on: {target_dir}")
    moved = 0
    skipped = 0

    try:
        entries = os.listdir(target_dir)
    except FileNotFoundError:
        logger.error(f"Directory not found: {target_dir}")
        print(f"  ✗ Directory '{target_dir}' does not exist.")
        return
    except PermissionError:
        logger.error(f"Permission denied: {target_dir}")
        print(f"  ✗ Permission denied for '{target_dir}'.")
        return

    for filename in entries:
        filepath = os.path.join(target_dir, filename)

        if os.path.isdir(filepath):
            logger.info(f"  Skipping directory: {filename}")
            skipped += 1
            continue

        _, ext = os.path.splitext(filename)
        category = get_category(ext)
        dest_dir = os.path.join(target_dir, category)

        try:
            os.makedirs(dest_dir, exist_ok=True)
            dest_path = os.path.join(dest_dir, filename)

            # Avoid overwriting: append counter if file exists
            if os.path.exists(dest_path):
                base, extension = os.path.splitext(filename)
                counter = 1
                while os.path.exists(dest_path):
                    dest_path = os.path.join(dest_dir, f"{base}_{counter}{extension}")
                    counter += 1

            shutil.move(filepath, dest_path)
            logger.info(f"  Moved '{filename}' → {category}/")
            moved += 1

        except PermissionError:
            logger.warning(f"  Permission denied moving '{filename}'")
            skipped += 1
        except Exception as e:
            logger.error(f"  Error moving '{filename}': {e}")
            skipped += 1

    print(f"\n  ✓ Sort complete: {moved} file(s) moved, {skipped} skipped.")
    logger.info(f"Sort complete: {moved} moved, {skipped} skipped.")


def rename_files(target_dir: str) -> None:
    """Bulk rename files: lowercase names, replace spaces with underscores, add date prefix."""
    logger.info(f"Starting RENAME operation on: {target_dir}")
    renamed = 0
    skipped = 0
    date_prefix = datetime.datetime.now().strftime("%Y%m%d")

    try:
        entries = os.listdir(target_dir)
    except FileNotFoundError:
        logger.error(f"Directory not found: {target_dir}")
        print(f"  ✗ Directory '{target_dir}' does not exist.")
        return

    for filename in entries:
        filepath = os.path.join(target_dir, filename)
        if os.path.isdir(filepath):
            skipped += 1
            continue

        base, ext = os.path.splitext(filename)
        new_base = base.lower().replace(" ", "_")
        new_name = f"{date_prefix}_{new_base}{ext.lower()}"
        new_path = os.path.join(target_dir, new_name)

        if new_name == filename:
            logger.info(f"  No change needed: '{filename}'")
            skipped += 1
            continue

        try:
            if os.path.exists(new_path):
                logger.warning(f"  Target already exists, skipping: '{new_name}'")
                skipped += 1
                continue

            os.rename(filepath, new_path)
            logger.info(f"  Renamed '{filename}' → '{new_name}'")
            renamed += 1

        except PermissionError:
            logger.warning(f"  Permission denied renaming '{filename}'")
            skipped += 1
        except Exception as e:
            logger.error(f"  Error renaming '{filename}': {e}")
            skipped += 1

    print(f"\n  ✓ Rename complete: {renamed} file(s) renamed, {skipped} skipped.")
    logger.info(f"Rename complete: {renamed} renamed, {skipped} skipped.")


def clean_files(target_dir: str) -> None:
    """Delete empty files and common junk files (.DS_Store, Thumbs.db, *.tmp)."""
    logger.info(f"Starting CLEAN operation on: {target_dir}")
    deleted = 0
    skipped = 0

    JUNK_NAMES = {".ds_store", "thumbs.db", "desktop.ini"}
    JUNK_EXTS  = {".tmp", ".bak", ".log~", ".swp"}

    try:
        for root, dirs, files in os.walk(target_dir):
            for filename in files:
                filepath = os.path.join(root, filename)
                base, ext = os.path.splitext(filename)
                reason = None

                if filename.lower() in JUNK_NAMES:
                    reason = "junk filename"
                elif ext.lower() in JUNK_EXTS:
                    reason = f"junk extension ({ext})"
                else:
                    try:
                        if os.path.getsize(filepath) == 0:
                            reason = "empty file"
                    except OSError:
                        pass

                if reason:
                    try:
                        os.remove(filepath)
                        logger.info(f"  Deleted '{filepath}' ({reason})")
                        deleted += 1
                    except PermissionError:
                        logger.warning(f"  Permission denied deleting '{filepath}'")
                        skipped += 1
                    except Exception as e:
                        logger.error(f"  Error deleting '{filepath}': {e}")
                        skipped += 1
                else:
                    skipped += 1

    except FileNotFoundError:
        logger.error(f"Directory not found: {target_dir}")
        print(f"  ✗ Directory '{target_dir}' does not exist.")
        return

    print(f"\n  ✓ Clean complete: {deleted} file(s) deleted, {skipped} unchanged.")
    logger.info(f"Clean complete: {deleted} deleted, {skipped} unchanged.")


# ─── Menu / User Input ────────────────────────────────────────────────────────

def print_banner():
    print("=" * 55)
    print("        FILE ORGANIZER - Automation Script")
    print("=" * 55)


def print_menu():
    print("\n  Select an operation:")
    print("  [1] Sort files into category folders")
    print("  [2] Rename files (lowercase + date prefix)")
    print("  [3] Clean junk/empty files")
    print("  [4] Run all operations")
    print("  [5] Exit")
    print("-" * 55)


def get_directory() -> str:
    while True:
        path = input("  Enter target directory path: ").strip()
        if not path:
            print("  ✗ Path cannot be empty. Try again.")
            continue
        path = os.path.expanduser(path)  # support ~
        if not os.path.isdir(path):
            print(f"  ✗ '{path}' is not a valid directory. Try again.")
            continue
        return path


def confirm(prompt: str) -> bool:
    answer = input(f"  {prompt} [y/N]: ").strip().lower()
    return answer == "y"


def main():
    print_banner()
    logger.info("File Organizer started.")

    while True:
        print_menu()
        choice = input("  Your choice (1-5): ").strip()

        if choice == "5":
            print("\n  Goodbye! Log saved to:", log_filename)
            logger.info("File Organizer exited by user.")
            break

        if choice not in {"1", "2", "3", "4"}:
            print("  ✗ Invalid choice. Please enter 1-5.")
            continue

        target = get_directory()

        if choice == "1":
            if confirm(f"Sort all files in '{target}'?"):
                sort_files(target)

        elif choice == "2":
            if confirm(f"Rename all files in '{target}'?"):
                rename_files(target)

        elif choice == "3":
            if confirm(f"Delete junk/empty files in '{target}'?"):
                clean_files(target)

        elif choice == "4":
            if confirm(f"Run ALL operations on '{target}'?"):
                sort_files(target)
                rename_files(os.path.join(target, "Documents"))  # example sub-dir
                clean_files(target)

        print(f"\n  Log file: {log_filename}")


if __name__ == "__main__":
    main()
