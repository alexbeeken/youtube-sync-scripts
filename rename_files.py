import os
import csv
from mutagen.id3 import ID3, TPE1, TALB
from utils import log_debug

def process_renames(output_folder, rename_csv_path):
    if not os.path.exists(rename_csv_path):
        log_debug(f"Rename CSV not found at {rename_csv_path}. Skipping rename phase.")
        return

    # Load rename rules, artist, and album into a dictionary
    # Format: { "Old Name": {"new_name": "...", "artist": "...", "album": "..."} }
    rename_data = {}
    with open(rename_csv_path, mode='r', encoding='utf-8') as f:
        # Use DictReader to handle the new columns by name
        reader = csv.DictReader(f)
        for row in reader:
            old_name = row['Old Name'].strip()
            rename_data[old_name] = {
                'new_name': row['New Name'].strip(),
                'artist': row.get('Artist', '').strip(),
                'album': row.get('Album', '').strip()
            }

    log_debug(f"Loaded {len(rename_data)} rules from CSV.")

    for filename in os.listdir(output_folder):
        file_path = os.path.join(output_folder, filename)
        if not os.path.isfile(file_path):
            continue

        name_without_ext, ext = os.path.splitext(filename)
        
        # Determine if this file exists in our CSV (checking full name or name w/o ext)
        entry = None
        if filename in rename_data:
            entry = rename_data[filename]
        elif name_without_ext in rename_data:
            entry = rename_data[name_without_ext]

        if entry:
            new_filename = entry['new_name']
            # Ensure extension is preserved if the CSV value doesn't include it
            if not new_filename.lower().endswith(ext.lower()):
                new_filename += ext
                
            new_path = os.path.join(output_folder, new_filename)
            
            # 1. Rename the file
            log_debug(f"Match found! Renaming '{filename}' to '{new_filename}'")
            os.rename(file_path, new_path)

            # 2. Update Metadata (if .mp3)
            if new_filename.lower().endswith('.mp3'):
                update_metadata(new_path, entry['artist'], entry['album'])

def update_metadata(file_path, artist, album):
    """Updates the ID3 tags for Artist and Album."""
    if not artist and not album:
        return

    try:
        # Load or create ID3 tags
        try:
            tags = ID3(file_path)
        except Exception:
            tags = ID3()

        # TPE1 is Lead Performer/Artist, TALB is Album/Movie/Show title
        if artist:
            tags.add(TPE1(encoding=3, text=artist))
        if album:
            tags.add(TALB(encoding=3, text=album))

        tags.save(file_path, v2_version=3) # v2.3 is most compatible
        log_debug(f"Successfully tagged metadata for: {os.path.basename(file_path)}")
    except Exception as e:
        log_debug(f"Failed to update metadata for {file_path}: {e}")
