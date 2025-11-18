#!/usr/bin/env python3
"""
Comprehensive Hiring Analytics
Analyzes the full 930-row hiring dataset
"""

import pandas as pd
import numpy as np
from datetime import datetime
import json
from collections import defaultdict

# Try to read the file - it might be named differently
import os

possible_files = [
    'hiring_full_930.csv',
    'hiring_6m_merged.csv',
    'hiring_6m_merged (1).csv',
    '../hiring_6m_merged.csv',
    '../hiring_6m_merged (1).csv'
]

df = None
for file_path in possible_files:
    if os.path.exists(file_path):
        try:
            df = pd.read_csv(file_path, encoding='utf-8')
            print(f"✓ Loaded data from: {file_path}")
            print(f"✓ Total rows: {len(df)}")
            break
        except Exception as e:
            print(f"✗ Could not read {file_path}: {e}")

if df is None or len(df) < 900:
    print("\n" + "="*80)
    print("WARNING: Full dataset (930 rows) not found in current location.")
    print(f"Currently loaded: {len(df) if df is not None else 0} rows")
    print("="*80)
    if df is None:
        exit(1)

# Convert date columns
df['Created at'] = pd.to_datetime(df['Created at'], errors='coerce')
df['Sourced at'] = pd.to_datetime(df['Sourced at'], errors='coerce')
df['Rejected at'] = pd.to_datetime(df['Rejected at'], errors='coerce')

# Add quarter
df['Quarter'] = df['Created at'].dt.to_period('Q').astype(str)

# Extract country (simple approach - take first part before comma)
df['Country'] = df['Location (país,localidad)'].fillna('Unknown')

print("\n" + "="*80)
print("COMPREHENSIVE HIRING ANALYTICS REPORT")
print(f"Analysis Period: {df['Created at'].min().date()} to {df['Created at'].max().date()}")
print("="*80)

# ============================================================================
# 1. HIRES ANALYSIS
# ============================================================================
print("\n" + "="*80)
print("1. HIRES ANALYSIS")
print("="*80)

hires_df = df[df['Status'] == 'Hired'].copy()
total_hires = len(hires_df)

print(f"\n📊 Total Hires: {total_hires}")

# By Job
print(f"\n📋 Hires by Job Title:")
hires_by_job = hires_df['Job title'].value_counts()
for job, count in hires_by_job.items():
    pct = (count / total_hires) * 100 if total_hires > 0 else 0
    print(f"   • {job}: {count} ({pct:.1f}%)")

# By Quarter
print(f"\n📅 Hires by Quarter:")
hires_by_quarter = hires_df['Quarter'].value_counts().sort_index()
for quarter, count in hires_by_quarter.items():
    print(f"   • {quarter}: {count}")

# By Location/Country
print(f"\n🌍 Hires by Location (Top 10):")
hires_by_location = hires_df['Country'].value_counts().head(10)
for location, count in hires_by_location.items():
    print(f"   • {location}: {count}")

# By Role
print(f"\n👔 Hires by Role:")
hires_by_role = hires_df['Role'].fillna('Not specified').value_counts()
for role, count in hires_by_role.items():
    print(f"   • {role}: {count}")

# ============================================================================
# 2. REJECTION ANALYSIS
# ============================================================================
print("\n" + "="*80)
print("2. REJECTION ANALYSIS")
print("="*80)

rejected_df = df[df['Status'] == 'Rejected'].copy()
total_rejected = len(rejected_df)

print(f"\n❌ Total Rejections: {total_rejected}")

print(f"\n🔍 Top 15 Rejection Reasons:")
rejection_reasons = rejected_df['Reject reason'].fillna('Not specified').value_counts()
for i, (reason, count) in enumerate(rejection_reasons.head(15).items(), 1):
    pct = (count / total_rejected) * 100
    print(f"   {i:2d}. {reason}: {count} ({pct:.1f}%)")

print(f"\n📍 Rejections by Stage:")
rejection_by_stage = rejected_df['Stage name'].value_counts()
for stage, count in rejection_by_stage.items():
    pct = (count / total_rejected) * 100
    print(f"   • {stage}: {count} ({pct:.1f}%)")

# Rejection reasons breakdown by stage
print(f"\n🔄 Top Rejection Reasons by Stage:")
for stage in ['Screening', 'Code Technical Interview', 'People Interview', 'Psicotécnicos', 'PsicotÃ©cnicos']:
    stage_rejections = rejected_df[rejected_df['Stage name'] == stage]
    if len(stage_rejections) > 0:
        print(f"\n   {stage} ({len(stage_rejections)} rejections):")
        top_reasons = stage_rejections['Reject reason'].value_counts().head(3)
        for reason, count in top_reasons.items():
            print(f"      - {reason}: {count}")

# ============================================================================
# 3. CONVERSION METRICS
# ============================================================================
print("\n" + "="*80)
print("3. CONVERSION METRICS & FUNNEL ANALYSIS")
print("="*80)

total_applications = len(df)
total_hired = len(hires_df)
total_rejected = len(rejected_df)
total_active = len(df[df['Status'] == 'Active'])

print(f"\n📈 Overall Funnel:")
print(f"   Total Applications: {total_applications}")
print(f"   └─ Hired: {total_hired} ({(total_hired/total_applications)*100:.1f}%)")
print(f"   └─ Rejected: {total_rejected} ({(total_rejected/total_applications)*100:.1f}%)")
print(f"   └─ Active (In Process): {total_active} ({(total_active/total_applications)*100:.1f}%)")

overall_conversion = (total_hired / total_applications) * 100
print(f"\n🎯 Overall Conversion Rate: {overall_conversion:.2f}%")

# Conversion by Job
print(f"\n💼 Conversion Rate by Job (Top 10):")
job_conversions = []
for job in df['Job title'].unique():
    job_df = df[df['Job title'] == job]
    job_hires = len(job_df[job_df['Status'] == 'Hired'])
    job_total = len(job_df)
    conv_rate = (job_hires / job_total) * 100 if job_total > 0 else 0
    job_conversions.append((job, job_hires, job_total, conv_rate))

job_conversions.sort(key=lambda x: x[3], reverse=True)
for job, hires, total, conv_rate in job_conversions[:10]:
    if total >= 5:  # Only show positions with at least 5 applications
        print(f"   • {job}")
        print(f"     {hires}/{total} = {conv_rate:.1f}%")

# Conversion by Location
print(f"\n🌎 Conversion Rate by Location (Top 10):")
location_conversions = []
for location in df['Country'].value_counts().head(15).index:
    loc_df = df[df['Country'] == location]
    loc_hires = len(loc_df[loc_df['Status'] == 'Hired'])
    loc_total = len(loc_df)
    conv_rate = (loc_hires / loc_total) * 100 if loc_total > 0 else 0
    if loc_total >= 5:
        location_conversions.append((location, loc_hires, loc_total, conv_rate))

location_conversions.sort(key=lambda x: x[3], reverse=True)
for location, hires, total, conv_rate in location_conversions[:10]:
    print(f"   • {location}: {hires}/{total} = {conv_rate:.1f}%")

# ============================================================================
# 4. TIME TO HIRE ANALYSIS
# ============================================================================
print("\n" + "="*80)
print("4. TIME TO HIRE ANALYSIS")
print("="*80)

if total_hires > 0:
    avg_time = hires_df['Time to Hire (days)'].mean()
    median_time = hires_df['Time to Hire (days)'].median()
    min_time = hires_df['Time to Hire (days)'].min()
    max_time = hires_df['Time to Hire (days)'].max()

    print(f"\n⏱️  Overall Time to Hire:")
    print(f"   Average: {avg_time:.1f} days")
    print(f"   Median: {median_time:.1f} days")
    print(f"   Range: {min_time:.0f} - {max_time:.0f} days")

    print(f"\n📊 Average Time to Hire by Job:")
    for job in hires_df['Job title'].unique():
        job_hires = hires_df[hires_df['Job title'] == job]
        if len(job_hires) > 0:
            avg_time = job_hires['Time to Hire (days)'].mean()
            count = len(job_hires)
            print(f"   • {job}: {avg_time:.1f} days ({count} hires)")
else:
    print("\n⚠️  No hires yet to calculate time to hire metrics")

# ============================================================================
# 5. STAGE ANALYSIS
# ============================================================================
print("\n" + "="*80)
print("5. STAGE DISTRIBUTION & PROGRESSION")
print("="*80)

print(f"\n📋 Candidates by Stage:")
stage_counts = df['Stage name'].value_counts()
for stage, count in stage_counts.items():
    pct = (count / len(df)) * 100

    # Breakdown by status
    stage_hired = len(df[(df['Stage name'] == stage) & (df['Status'] == 'Hired')])
    stage_rejected = len(df[(df['Stage name'] == stage) & (df['Status'] == 'Rejected')])
    stage_active = len(df[(df['Stage name'] == stage) & (df['Status'] == 'Active')])

    print(f"\n   • {stage}: {count} ({pct:.1f}%)")
    print(f"      Hired: {stage_hired} | Rejected: {stage_rejected} | Active: {stage_active}")

# ============================================================================
# 6. SOURCE ANALYSIS
# ============================================================================
print("\n" + "="*80)
print("6. SOURCE ANALYSIS (Referring Sites)")
print("="*80)

source_counts = df['Referring site'].fillna('Unknown').value_counts()
print(f"\n📊 Applications by Source:")
for source, count in source_counts.items():
    pct = (count / len(df)) * 100
    hired_from_source = len(df[(df['Referring site'] == source) & (df['Status'] == 'Hired')])
    conv_rate = (hired_from_source / count) * 100 if count > 0 else 0
    print(f"   • {source}:")
    print(f"      {count} applications ({pct:.1f}%) → {hired_from_source} hires ({conv_rate:.1f}% conversion)")

# ============================================================================
# 7. POSITIONS CLOSED
# ============================================================================
print("\n" + "="*80)
print("7. POSITIONS CLOSED")
print("="*80)

print(f"\n✅ Total Positions Filled: {total_hires}")
if total_hires > 0:
    print(f"\n📊 Breakdown by Job:")
    positions_closed = hires_df['Job title'].value_counts()
    for job, count in positions_closed.items():
        print(f"   • {job}: {count} position(s) filled")

# ============================================================================
# SAVE COMPREHENSIVE METRICS TO JSON
# ============================================================================

metrics = {
    'summary': {
        'total_applications': int(total_applications),
        'total_hired': int(total_hired),
        'total_rejected': int(total_rejected),
        'total_active': int(total_active),
        'overall_conversion_rate': float(overall_conversion),
        'analysis_period': {
            'start': str(df['Created at'].min().date()),
            'end': str(df['Created at'].max().date())
        }
    },
    'hires': {
        'total': int(total_hires),
        'by_job': hires_by_job.to_dict(),
        'by_quarter': hires_by_quarter.to_dict(),
        'by_location': hires_by_location.to_dict(),
        'by_role': hires_by_role.to_dict()
    },
    'rejections': {
        'total': int(total_rejected),
        'top_reasons': rejection_reasons.head(15).to_dict(),
        'by_stage': rejection_by_stage.to_dict()
    },
    'conversion_by_job': {job: {
        'total_applications': int(total),
        'hires': int(hires),
        'conversion_rate': float(conv_rate)
    } for job, hires, total, conv_rate in job_conversions},
    'conversion_by_location': {loc: {
        'total_applications': int(total),
        'hires': int(hires),
        'conversion_rate': float(conv_rate)
    } for loc, hires, total, conv_rate in location_conversions},
    'time_to_hire': {
        'average_days': float(avg_time) if total_hires > 0 else None,
        'median_days': float(median_time) if total_hires > 0 else None,
        'min_days': float(min_time) if total_hires > 0 else None,
        'max_days': float(max_time) if total_hires > 0 else None,
        'by_job': {job: float(hires_df[hires_df['Job title'] == job]['Time to Hire (days)'].mean())
                   for job in hires_df['Job title'].unique()} if total_hires > 0 else {}
    },
    'stage_distribution': stage_counts.to_dict(),
    'source_analysis': {source: {
        'applications': int(count),
        'hires': int(len(df[(df['Referring site'] == source) & (df['Status'] == 'Hired')])),
        'conversion_rate': float((len(df[(df['Referring site'] == source) & (df['Status'] == 'Hired')]) / count) * 100) if count > 0 else 0
    } for source, count in source_counts.items()}
}

with open('full_hiring_analytics.json', 'w', encoding='utf-8') as f:
    json.dump(metrics, f, indent=2, ensure_ascii=False)

print("\n" + "="*80)
print("✅ Complete analytics saved to: full_hiring_analytics.json")
print("="*80)
