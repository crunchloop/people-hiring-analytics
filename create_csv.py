import csv

# This will read from the document content and create the CSV
csv_content = """Job title,Job name,Department name,Role,"Location (país,localidad)",Candidate name,Edad,Referring site,Created at,Sourced at,Stage name,Status,Rejected at,Reject reason,Time to Hire (days)
Jr AI Fullstack Dev,,,,,Guillermo Torres,,,2025-05-30,2025-05-30,Code challenge,Rejected,2025-07-14,No respetó tiempo límite,
Jr AI Fullstack Dev,,,,,Joaquín Urruty,,,2025-10-24,2025-10-24,Inbox,Active,,,
Jr AI Fullstack Dev,,,,,Lorenzo Garese,,,2025-07-21,2025-07-21,Code challenge,Rejected,2025-09-15,No respetó tiempo límite,
Jr AI Fullstack Dev,,,,,Maite Tuya,,,2025-10-24,2025-10-24,Inbox,Active,,,
Jr AI Fullstack Dev,,,,,Marcelo Martínez Lluch,,,2025-08-27,2025-08-27,Screening,Rejected,2025-09-15,Opening Paused,"""

# Since the full CSV is too large to paste, let me read it from your document
# For now, let me create a minimal working version to test the script

with open('hiring_6m_merged.csv', 'w', encoding='utf-8') as f:
    f.write(csv_content)

print("CSV file created successfully (partial data for testing)")
