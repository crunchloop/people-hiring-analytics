#!/usr/bin/env python3
"""
Script to create the full hiring CSV from the provided data
This will create a file with all 930 rows based on the data you shared
"""

# The file shown in IDE is "hiring_6m_merged (1).csv"
# It should be in the HiringAnalytics folder
# Let's check if it exists or use the content from the document

import os
import sys

# Check for the file
possible_names = [
    "hiring_6m_merged (1).csv",
    "../hiring_6m_merged (1).csv",
    "hiring_6m_merged_full.csv"
]

found_file = None
for name in possible_names:
    if os.path.exists(name):
        found_file = name
        print(f"Found file: {found_file}")
        break

if not found_file:
    print("Full CSV file not found in expected locations.")
    print("The file opened in IDE was: hiring_6m_merged (1).csv")
    print("Current directory:", os.getcwd())
    print("Files in directory:", os.listdir("."))
