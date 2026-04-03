# YouTube Playlist Sync Tool

A Python application that synchronizes YouTube playlist content to a local folder, with automatic file renaming capabilities.

## Overview

This tool performs a three-step synchronization process:
1. **Fetch** video IDs from a YouTube playlist
2. **Sync** downloaded files with the playlist
3. **Rename** files according to a custom mapping

## Requirements

- Python 3.x
- [python-mutagen](https://github.com/quodlibet/mutagen)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- Modules: `utils`, `fetch_ids`, `sync_files`, `rename_files`

## Installation

1. Clone or download the project files
2. Ensure all module files are in the same directory:
   ```
   ├── main.py
   ├── utils.py
   ├── fetch_ids.py
   ├── sync_files.py
   ├── rename_files.py
   └── requirements.txt (optional)
   ```

## Usage

### Command Line

```bash
python3 main.py <playlist_link> <output_folder_absolute_path>
```

### Arguments

| Argument | Description | Required |
|----------|-------------|----------|
| `<playlist_link>` | YouTube playlist URL | Yes |
| `<output_folder_absolute_path>` | Absolute path to store synced files | Yes |

### Examples

```bash
# Basic usage
python3 main.py "https://youtube.com/playlist?list=PLxxx" "/home/user/music"

# With debug logging enabled
python3 main.py "https://youtube.com/playlist?list=PLxxx" "/mnt/storage/downloads"
```

## Output Files

The tool creates the following tracking files in your output folder:

| File | Purpose |
|------|---------|
| `playlist_ids.txt` | Stores video IDs from the playlist |
| `downloaded_ids.txt` | Tracks already downloaded videos |
| `renames.csv` | Mapping file for renaming files |

## Rename Configuration

The `renames.csv` file uses the following format:

```csv
Old Name,New Name
video1.mp4,Song Title.mp4
video2.mp4,Artist - Track.mp4
```

**Note:** A default empty CSV is created if none exists. Edit this file before running the sync to apply custom naming.

## Error Handling

The application validates:
- ✅ Exactly 2 command-line arguments
- ✅ Output folder is an absolute path (not relative)
- ✅ Creates output directory if it doesn't exist

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Usage: python3 main.py..." error | Ensure exactly 2 arguments are provided |
| "Output folder must be absolute path" | Use full path (e.g., `/home/user/music` not `music`) |
| Missing module errors | Verify all `.py` files are in the same directory |

## Notes

- Debug logging is enabled via the `log_debug` function from `utils`
- The tool is idempotent—running it multiple times won't duplicate downloads
- Ensure you have write permissions for the output folder

---

*For issues or questions, check the `utils.py` configuration or contact the project maintainer.*
