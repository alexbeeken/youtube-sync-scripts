import sys
import os
from utils import log_debug
import fetch_ids
import sync_files
import rename_files

if __name__ == "__main__":
    # Validate arguments
    if len(sys.argv) != 3:
        print("Usage: python3 main.py <playlist_link> <output_folder_absolute_path>")
        sys.exit(1)

    playlist_link = sys.argv[1]
    output_folder = sys.argv[2]

    if not os.path.isabs(output_folder):
        print("Error: The output folder must be an absolute path (e.g., /home/dietpi/music).")
        sys.exit(1)

    # Ensure output directory exists
    os.makedirs(output_folder, exist_ok=True)

    # Define our tracking files inside the output folder
    playlist_file = os.path.join(output_folder, "playlist_ids.txt")
    downloaded_file = os.path.join(output_folder, "downloaded_ids.txt")
    rename_csv = os.path.join(output_folder, "renames.csv")

    # Create dummy CSV if it doesn't exist so the user knows where to put it
    if not os.path.exists(rename_csv):
        with open(rename_csv, 'w') as f:
            f.write("Old Name,New Name\n")

    log_debug(f"Starting YouTube sync job...")
    log_debug(f"Playlist: {playlist_link}")
    log_debug(f"Target: {output_folder}")

    # Run the 3 steps
    fetch_ids.populate_playlist_ids(playlist_link, playlist_file)
    sync_files.sync_downloads(playlist_file, downloaded_file, output_folder)
    rename_files.process_renames(output_folder, rename_csv)

    log_debug("Sync complete.")
