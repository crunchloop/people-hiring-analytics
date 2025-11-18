import pandas as pd
import numpy as np
from datetime import datetime
import json
from io import StringIO

# The CSV data (you'll need to paste the full content here)
# For demonstration, I'm including a sample. You would replace this with the full data.
csv_data = """Job title,Job name,Department name,Role,"Location (país,localidad)",Candidate name,Edad,Referring site,Created at,Sourced at,Stage name,Status,Rejected at,Reject reason,Time to Hire (days)
Jr AI Fullstack Dev,,,,,Guillermo Torres,,,2025-05-30,2025-05-30,Code challenge,Rejected,2025-07-14,No respetó tiempo límite,
Jr AI Fullstack Dev,,,,,Joaquín Urruty,,,2025-10-24,2025-10-24,Inbox,Active,,,"""

# Save CSV
with open('hiring_6m_merged.csv', 'w', encoding='utf-8') as f:
    # Read from document - for now using sample
    # In production, you'd paste the full content
    f.write(csv_data)

print("Please provide the full CSV content to process all 930 rows.")
print("For now, creating analysis framework...")
