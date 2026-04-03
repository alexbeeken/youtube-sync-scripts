import os

def log_debug(message):
    """Prints debug statements if DEBUG_YT_SYNC is set to true."""
    if os.environ.get('DEBUG_YT_SYNC', '').lower() == 'true':
        print(f"[DEBUG] {message}")
