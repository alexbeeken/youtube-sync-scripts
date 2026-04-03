import subprocess
from utils import log_debug

def populate_playlist_ids(playlist_url, playlist_file_path):
    log_debug(f"Wiping and remaking playlist IDs from: {playlist_url}")
    
    # Wipe the file
    open(playlist_file_path, 'w').close()

    # yt-dlp command to quickly fetch just the IDs without downloading video
    cmd = ["/root/.local/bin/yt-dlp", "--flat-playlist", "-4", "--print", "id", playlist_url]
    log_debug(f"Running command: {' '.join(cmd)}")
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        log_debug(f"Error fetching playlist: {result.stderr}")
        return

    # Filter out any blank lines
    ids = [vid_id.strip() for vid_id in result.stdout.strip().split('\n') if vid_id.strip()]

    # Write fresh IDs
    with open(playlist_file_path, 'w') as f:
        for vid_id in ids:
            f.write(f"{vid_id}\n")
            
    log_debug(f"Successfully saved {len(ids)} IDs to {playlist_file_path}")
