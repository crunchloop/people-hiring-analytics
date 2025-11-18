import pandas as pd
import numpy as np
from datetime import datetime
import json

# Load the data
df = pd.read_csv('hiring_6m_merged.csv')

# Clean and prepare data
df['Created at'] = pd.to_datetime(df['Created at'])
df['Sourced at'] = pd.to_datetime(df['Sourced at'])
df['Rejected at'] = pd.to_datetime(df['Rejected at'])

# Extract quarter from Created at
df['Quarter'] = df['Created at'].dt.to_period('Q').astype(str)

# Extract country from Location
df['Country'] = df['Location (país,localidad)'].fillna('Unknown')

# 1. NUMBER OF HIRES
hires_df = df[df['Status'] == 'Hired'].copy()

hires_by_job = hires_df['Job title'].value_counts().to_dict()
hires_by_quarter = hires_df['Quarter'].value_counts().sort_index().to_dict()
hires_by_country = hires_df['Country'].value_counts().to_dict()
hires_by_role = hires_df['Role'].fillna('Not specified').value_counts().to_dict()

print("=" * 80)
print("HIRES ANALYSIS")
print("=" * 80)
print(f"\nTotal Hires: {len(hires_df)}")
print(f"\nHires by Job:")
for job, count in sorted(hires_by_job.items(), key=lambda x: x[1], reverse=True):
    print(f"  {job}: {count}")

print(f"\nHires by Quarter:")
for quarter, count in sorted(hires_by_quarter.items()):
    print(f"  {quarter}: {count}")

print(f"\nHires by Country:")
for country, count in sorted(hires_by_country.items(), key=lambda x: x[1], reverse=True)[:10]:
    print(f"  {country}: {count}")

# 2. REJECTION REASONS
rejected_df = df[df['Status'] == 'Rejected'].copy()

print("\n" + "=" * 80)
print("REJECTION ANALYSIS")
print("=" * 80)
print(f"\nTotal Rejections: {len(rejected_df)}")

rejection_reasons = rejected_df['Reject reason'].fillna('Not specified').value_counts()
print(f"\nTop 15 Rejection Reasons:")
for reason, count in rejection_reasons.head(15).items():
    pct = (count / len(rejected_df)) * 100
    print(f"  {reason}: {count} ({pct:.1f}%)")

# Rejection by stage
rejection_by_stage = rejected_df['Stage name'].value_counts()
print(f"\nRejections by Stage:")
for stage, count in rejection_by_stage.items():
    pct = (count / len(rejected_df)) * 100
    print(f"  {stage}: {count} ({pct:.1f}%)")

# 3. POSITIONS CLOSED (Hires per job)
print("\n" + "=" * 80)
print("POSITIONS CLOSED")
print("=" * 80)
positions_closed = hires_df['Job title'].value_counts()
print(f"\nTotal Positions Filled: {len(hires_df)}")
print(f"Positions Closed by Job:")
for job, count in positions_closed.items():
    print(f"  {job}: {count}")

# 4. CONVERSION RATES
print("\n" + "=" * 80)
print("CONVERSION RATES")
print("=" * 80)

total_applications = len(df)
total_hired = len(hires_df)
total_rejected = len(rejected_df)
total_active = len(df[df['Status'] == 'Active'])

overall_conversion = (total_hired / total_applications) * 100
print(f"\nOverall Funnel Metrics:")
print(f"  Total Applications: {total_applications}")
print(f"  Hired: {total_hired} ({(total_hired/total_applications)*100:.1f}%)")
print(f"  Rejected: {total_rejected} ({(total_rejected/total_applications)*100:.1f}%)")
print(f"  Active (In Process): {total_active} ({(total_active/total_applications)*100:.1f}%)")
print(f"  Overall Conversion Rate: {overall_conversion:.2f}%")

# Conversion by job
print(f"\nConversion Rate by Job:")
for job in df['Job title'].unique():
    job_df = df[df['Job title'] == job]
    job_hires = len(job_df[job_df['Status'] == 'Hired'])
    job_total = len(job_df)
    conv_rate = (job_hires / job_total) * 100 if job_total > 0 else 0
    print(f"  {job}: {job_hires}/{job_total} = {conv_rate:.1f}%")

# Conversion by country
print(f"\nConversion Rate by Country (Top 10):")
country_stats = []
for country in df['Country'].value_counts().head(10).index:
    country_df = df[df['Country'] == country]
    country_hires = len(country_df[country_df['Status'] == 'Hired'])
    country_total = len(country_df)
    conv_rate = (country_hires / country_total) * 100 if country_total > 0 else 0
    country_stats.append((country, country_hires, country_total, conv_rate))
    print(f"  {country}: {country_hires}/{country_total} = {conv_rate:.1f}%")

# 5. STAGE ANALYSIS
print("\n" + "=" * 80)
print("STAGE ANALYSIS")
print("=" * 80)

# Define stage order (roughly)
stage_order = ['Inbox', 'Screening', 'Code challenge', 'Code Technical Interview',
               'Conversational Technical Interview', 'People Interview',
               'English Interview', 'Psicotécnicos', 'PsicotÃ©cnicos',
               'Job References', 'Offer', 'Hired']

stage_counts = df['Stage name'].value_counts()
print(f"\nCandidates by Stage:")
for stage, count in stage_counts.items():
    pct = (count / len(df)) * 100
    print(f"  {stage}: {count} ({pct:.1f}%)")

# 6. TIME TO HIRE ANALYSIS
print("\n" + "=" * 80)
print("TIME TO HIRE ANALYSIS")
print("=" * 80)

avg_time_to_hire = hires_df['Time to Hire (days)'].mean()
median_time_to_hire = hires_df['Time to Hire (days)'].median()
min_time = hires_df['Time to Hire (days)'].min()
max_time = hires_df['Time to Hire (days)'].max()

print(f"\nTime to Hire Statistics:")
print(f"  Average: {avg_time_to_hire:.1f} days")
print(f"  Median: {median_time_to_hire:.1f} days")
print(f"  Min: {min_time:.0f} days")
print(f"  Max: {max_time:.0f} days")

print(f"\nAverage Time to Hire by Job:")
for job in hires_df['Job title'].unique():
    job_hires = hires_df[hires_df['Job title'] == job]
    avg_time = job_hires['Time to Hire (days)'].mean()
    print(f"  {job}: {avg_time:.1f} days")

# 7. SOURCE ANALYSIS
print("\n" + "=" * 80)
print("SOURCE ANALYSIS (Referring Site)")
print("=" * 80)

source_counts = df['Referring site'].fillna('Unknown').value_counts()
print(f"\nApplications by Source:")
for source, count in source_counts.items():
    pct = (count / len(df)) * 100
    hired_from_source = len(df[(df['Referring site'] == source) & (df['Status'] == 'Hired')])
    conv_rate = (hired_from_source / count) * 100 if count > 0 else 0
    print(f"  {source}: {count} applications ({pct:.1f}%), {hired_from_source} hires ({conv_rate:.1f}% conversion)")

# Save metrics to JSON for dashboard
metrics = {
    'summary': {
        'total_applications': int(total_applications),
        'total_hired': int(total_hired),
        'total_rejected': int(total_rejected),
        'total_active': int(total_active),
        'overall_conversion_rate': float(overall_conversion)
    },
    'hires': {
        'by_job': hires_by_job,
        'by_quarter': hires_by_quarter,
        'by_country': hires_by_country,
        'by_role': hires_by_role
    },
    'rejections': {
        'total': int(len(rejected_df)),
        'by_reason': rejection_reasons.head(15).to_dict(),
        'by_stage': rejection_by_stage.to_dict()
    },
    'conversion_by_job': {job: float((len(df[(df['Job title'] == job) & (df['Status'] == 'Hired')]) / len(df[df['Job title'] == job])) * 100)
                          for job in df['Job title'].unique()},
    'time_to_hire': {
        'average': float(avg_time_to_hire),
        'median': float(median_time_to_hire),
        'min': float(min_time),
        'max': float(max_time),
        'by_job': {job: float(hires_df[hires_df['Job title'] == job]['Time to Hire (days)'].mean())
                   for job in hires_df['Job title'].unique()}
    },
    'stage_distribution': stage_counts.to_dict(),
    'source_analysis': {source: {
        'applications': int(count),
        'hires': int(len(df[(df['Referring site'] == source) & (df['Status'] == 'Hired')])),
        'conversion_rate': float((len(df[(df['Referring site'] == source) & (df['Status'] == 'Hired')]) / count) * 100) if count > 0 else 0
    } for source, count in source_counts.items()}
}

with open('hiring_metrics.json', 'w') as f:
    json.dump(metrics, f, indent=2)

print("\n" + "=" * 80)
print("Metrics saved to hiring_metrics.json")
print("=" * 80)
