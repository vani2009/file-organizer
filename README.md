# 🗂️ File Organizer — Automation Script

> Internship Task Submission | Python OS Automation  
> **Author:** Vani Agarwal &nbsp;|&nbsp; [GitHub](https://github.com/vani2009)

---

## 📌 Overview

**File Organizer** is a Python automation script that performs three file management operations on any directory you choose:

| Operation | What it does |
|-----------|-------------|
| **Sort**  | Moves files into category sub-folders (`Images/`, `Documents/`, `Videos/`, `Code/`, `Data/`, etc.) based on file extension |
| **Rename** | Converts filenames to lowercase, replaces spaces with underscores, and adds a `YYYYMMDD_` date prefix |
| **Clean** | Deletes junk files (`.DS_Store`, `Thumbs.db`, `*.tmp`, `*.bak`) and empty (0-byte) files |

All operations are menu-driven, fully logged, and include exception handling.

---

## ✅ Requirements Met

- [x] `os` module for all file operations (`os.listdir`, `os.rename`, `os.walk`, `os.makedirs`)
- [x] `shutil` for safe file moves
- [x] Exception handling (`try/except`) in every operation
- [x] Logging to console **and** timestamped file (`logs/file_organizer_YYYYMMDD_HHMMSS.log`)
- [x] Interactive user input (menu-driven, no CLI arguments needed)

---

## 🚀 Getting Started

### Prerequisites

- Python 3.x (no external packages — standard library only)

### Installation

```bash
git clone https://github.com/vani2009/file-organizer.git
cd file-organizer
```

### Run

```bash
python file_organizer.py
```

---

## 🖥️ Usage

When you run the script, an interactive menu appears:

```
=======================================================
        FILE ORGANIZER - Automation Script
=======================================================

  Select an operation:
  [1] Sort files into category folders
  [2] Rename files (lowercase + date prefix)
  [3] Clean junk/empty files
  [4] Run all operations
  [5] Exit
-------------------------------------------------------
  Your choice (1-5):
```

1. Enter a number (1–4) to select an operation
2. Enter the full path to your target directory
3. Confirm when prompted
4. Check the `logs/` folder for a detailed log of everything that happened

---

## 📁 File Categories (Sort)

| Folder | Extensions |
|--------|-----------|
| `Images/` | `.jpg` `.jpeg` `.png` `.gif` `.bmp` `.svg` `.webp` |
| `Documents/` | `.pdf` `.doc` `.docx` `.txt` `.odt` `.rtf` `.md` |
| `Videos/` | `.mp4` `.avi` `.mov` `.mkv` `.wmv` `.flv` |
| `Audio/` | `.mp3` `.wav` `.aac` `.flac` `.ogg` `.m4a` |
| `Archives/` | `.zip` `.tar` `.gz` `.rar` `.7z` |
| `Code/` | `.py` `.js` `.html` `.css` `.java` `.cpp` `.c` `.ts` |
| `Data/` | `.csv` `.json` `.xml` `.xlsx` `.sql` |
| `Others/` | Everything else |

---

## 📋 Sample Output

**Before:**
```
Desktop/
├── My Resume.PDF
├── photo1.JPG
├── data report.CSV
├── project.py
├── .DS_Store
├── temp_file.tmp
├── budget.xlsx
├── notes.TXT
└── video clip.MP4
```

**After Sort:**
```
Desktop/
├── Code/project.py
├── Data/budget.xlsx
├── Data/data report.CSV
├── Documents/My Resume.PDF
├── Documents/notes.TXT
├── Images/photo1.JPG
├── Others/.DS_Store
├── Others/temp_file.tmp
└── Videos/video clip.MP4
```

**After Rename (Documents folder):**
```
Documents/
├── 20260511_my_resume.pdf
└── 20260511_notes.txt
```

**After Clean:**
```
✓ Clean complete: 1021 file(s) deleted, 103748 unchanged.
```

---

## 📝 Log Format

Every run creates a new log file in `logs/`:

```
logs/file_organizer_20260511_140752.log
```

Sample log entries:
```
2026-05-11 14:10:05,123 [INFO] File Organizer started.
2026-05-11 14:10:08,441 [INFO] Starting SORT operation on: C:\Users\Vani Agarwal\Desktop
2026-05-11 14:10:08,512 [INFO]   Moved 'photo1.JPG' → Images/
2026-05-11 14:10:08,513 [INFO]   Moved 'My Resume.PDF' → Documents/
2026-05-11 14:10:09,001 [INFO] Sort complete: 9 moved, 0 skipped.
2026-05-11 14:11:10,924 [INFO] Clean complete: 1021 deleted, 103748 unchanged.
2026-05-11 14:11:26,619 [INFO] File Organizer exited by user.
```

---

## 🗃️ Project Structure

```
file-organizer/
├── file_organizer.py   # Main script
├── README.md           # This file
└── logs/               # Auto-created on first run
    └── file_organizer_YYYYMMDD_HHMMSS.log
```

---

## ⚠️ Notes

- The **Clean** operation is permanent — deleted files do not go to the Recycle Bin. Use with care.
- If a file with the same name already exists in the destination (during Sort), a counter suffix is appended automatically to avoid overwriting.
- The script skips sub-directories during Sort and Rename (only top-level files are processed); Clean uses `os.walk` to recurse into all sub-folders.

---

## 📄 License

This project was created as part of an internship task submission for [InternSpark](https://internspark.in).
