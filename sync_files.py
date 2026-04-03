import os
import subprocess
from utils import log_debug

def sync_downloads(playlist_file_path, downloaded_file_path, output_folder):
    # Ensure the downloaded file exists
    if not os.path.exists(downloaded_file_path):
        open(downloaded_file_path, 'w').close()

    with open(playlist_file_path, 'r') as f:
        playlist_ids = set(line.strip() for line in f if line.strip())

    # --- SAFETY CHECK ---
    if len(playlist_ids) == 0:
        print("0 items found, assuming error occured. Stopping operation.")
        log_debug("Playlist file returned 0 IDs. Aborting sync to prevent accidental deletion.")
        return
    # --------------------

    with open(downloaded_file_path, 'r') as f:
        downloaded_ids = set(line.strip() for line in f if line.strip())

    to_delete = downloaded_ids - playlist_ids
    to_download = playlist_ids - downloaded_ids

    log_debug(f"Found {len(to_delete)} items to delete.")
    log_debug(f"Found {len(to_download)} items to download.")

    # 1. Delete removed items
    for vid_id in to_delete:
        log_debug(f"Attempting to delete files for ID: {vid_id}")
        file_found_and_deleted = False
        
        for filename in os.listdir(output_folder):
            # We locate the file by checking if the YouTube ID is in the filename
            if vid_id in filename:
                file_path = os.path.join(output_folder, filename)
                log_debug(f"Deleting: {file_path}")
                os.remove(file_path)
                file_found_and_deleted = True

        # Remove the ID from our tracking file
        # (We only remove it if we found it in the playlist_ids diff earlier)
        downloaded_ids.remove(vid_id)
        with open(downloaded_file_path, 'w') as f:
            for i in downloaded_ids:
                f.write(f"{i}\n")

    # 2. Download new items
    for vid_id in to_download:
        log_debug(f"Downloading new ID: {vid_id}")
        url = f"https://www.youtube.com/watch?v={vid_id}"

        # Output template including ID in brackets for the delete step to work
        output_template = os.path.join(output_folder, "%(title)s [%(id)s].%(ext)s")
        cmd = ["/root/.local/bin/yt-dlp", "-f", "bestaudio", "-x", "--audio-format", "mp3", "-4", "-o", output_template, url]

        result = subprocess.run(cmd)
        if result.returncode == 0:
            log_debug(f"Successfully downloaded {vid_id}")
            downloaded_ids.add(vid_id)
            # Add the newly downloaded ID to the tracking file
            with open(downloaded_file_path, 'a') as f:
                f.write(f"{vid_id}\n")
        else:
            log_debug(f"Failed to download ID: {vid_id}")
