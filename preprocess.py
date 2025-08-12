import pandas as pd
import re
from datetime import datetime

def clean_chat(file):
    """
    Parse WhatsApp exported .txt content (file-like) into a DataFrame.
    Accepts uploaded file or raw string.
    Returns DataFrame with columns: timestamp, sender, message
    """
    if hasattr(file, "read"):
        raw = file.read()
        try:
            raw = raw.decode("utf-8")
        except Exception:
            raw = str(raw)
    else:
        raw = str(file)

    lines = raw.splitlines()
    # pattern with optional AM/PM
    pattern = r'^(\d{1,2}/\d{1,2}/\d{2,4}),\s+(\d{1,2}:\d{2})(?:\s?[APMapm]{2})?\s+-\s+([^:]+):\s+(.*)$'

    rows = []
    current = None
    for line in lines:
        line = line.strip()
        m = re.match(pattern, line)
        if m:
            if current:
                rows.append(current)
            date, time, sender, message = m.groups()
            # Try common datetime formats
            dt = None
            for fmt in ["%d/%m/%Y %H:%M", "%d/%m/%y %H:%M", "%d/%m/%Y %I:%M %p", "%d/%m/%y %I:%M %p"]:
                try:
                    dt = datetime.strptime(f"{date} {time}", fmt)
                    break
                except Exception:
                    continue
            if dt is None:
                dt = pd.NaT
            current = {"timestamp": dt, "sender": sender.strip(), "message": message.strip()}
        else:
            if current:
                current["message"] += " " + line

    if current:
        rows.append(current)

    df = pd.DataFrame(rows)
    if 'timestamp' in df.columns:
        df = df.dropna(subset=['timestamp']).sort_values('timestamp').reset_index(drop=True)
    else:
        df['timestamp'] = pd.NaT
    return df
