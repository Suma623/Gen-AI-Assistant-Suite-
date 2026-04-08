from datetime import datetime

def get_current_timestamp() -> str:
    """Returns a cleanly formatted string of the current date and time."""
    now = datetime.now()
    return now.strftime("%b %d, %Y - %I:%M %p")
