import pandas as pd
import numpy as np
from datetime import datetime
import json

# Read the CSV file
print("Loading hiring data...")
df = pd.read_csv('hiring_complete.csv')

# Add Status column based on the data
def determine_status(row):
    if pd.notna(row['Time to Hire (days)']):
        return 'Hired'
    elif pd.notna(row['Rejected at']) or pd.notna(row['Reject reason']):
        return 'Rejected'
    else:
        return 'Active'

df['Status'] = df.apply(determine_status, axis=1)

# Convert dates
df['Created at'] = pd.to_datetime(df['Created at'])
df['Rejected at'] = pd.to_datetime(df['Rejected at'])
df['Sourced at'] = pd.to_datetime(df['Sourced at'])

# Extract quarter
df['Quarter'] = df['Created at'].dt.to_period('Q').astype(str)
df['Month'] = df['Created at'].dt.to_period('M').astype(str)

print(f"\nTotal records: {len(df)}")
print(f"Date range: {df['Created at'].min()} to {df['Created at'].max()}")

# =============================================================================
# 1. HIRES ANALYSIS
# =============================================================================
print("\n" + "="*80)
print("1. HIRES ANALYSIS")
print("="*80)

hires_df = df[df['Status'] == 'Hired'].copy()
print(f"\nTotal Hires: {len(hires_df)}")

# Hires by Job
print("\nHires by Job Title:")
hires_by_job = hires_df['Job title'].value_counts()
for job, count in hires_by_job.items():
    print(f"  • {job}: {count}")

# Hires by Quarter
print("\nHires by Quarter:")
hires_by_quarter = hires_df['Quarter'].value_counts().sort_index()
for quarter, count in hires_by_quarter.items():
    print(f"  • {quarter}: {count}")

# Hires by Month
print("\nHires by Month:")
hires_by_month = hires_df['Month'].value_counts().sort_index()
for month, count in hires_by_month.items():
    print(f"  • {month}: {count}")

# =============================================================================
# 2. REJECTION ANALYSIS
# =============================================================================
print("\n" + "="*80)
print("2. REJECTION ANALYSIS")
print("="*80)

rejected_df = df[df['Status'] == 'Rejected'].copy()
print(f"\nTotal Rejections: {len(rejected_df)}")

# Top rejection reasons
print("\nTop 20 Rejection Reasons:")
rejection_reasons = rejected_df['Reject reason'].fillna('Not specified').value_counts()
for i, (reason, count) in enumerate(rejection_reasons.head(20).items(), 1):
    pct = (count / len(rejected_df)) * 100
    print(f"  {i}. {reason}: {count} ({pct:.1f}%)")

# Rejections by stage
print("\nRejections by Stage:")
rejection_by_stage = rejected_df['Stage name'].value_counts()
for stage, count in rejection_by_stage.items():
    pct = (count / len(rejected_df)) * 100
    print(f"  • {stage}: {count} ({pct:.1f}%)")

# =============================================================================
# 3. POSITIONS CLOSED & CONVERSION RATES
# =============================================================================
print("\n" + "="*80)
print("3. POSITIONS CLOSED & CONVERSION RATES")
print("="*80)

total_applications = len(df)
total_hired = len(hires_df)
total_rejected = len(rejected_df)
total_active = len(df[df['Status'] == 'Active'])

overall_conversion = (total_hired / total_applications) * 100

print(f"\nOverall Funnel Metrics:")
print(f"  • Total Applications: {total_applications}")
print(f"  • Hired: {total_hired} ({(total_hired/total_applications)*100:.1f}%)")
print(f"  • Rejected: {total_rejected} ({(total_rejected/total_applications)*100:.1f}%)")
print(f"  • Active (In Process): {total_active} ({(total_active/total_applications)*100:.1f}%)")
print(f"  • Overall Conversion Rate: {overall_conversion:.2f}%")

# Conversion by job
print(f"\nConversion Rate by Job Title:")
conversion_data = []
for job in df['Job title'].unique():
    job_df = df[df['Job title'] == job]
    job_hires = len(job_df[job_df['Status'] == 'Hired'])
    job_rejected = len(job_df[job_df['Status'] == 'Rejected'])
    job_active = len(job_df[job_df['Status'] == 'Active'])
    job_total = len(job_df)
    conv_rate = (job_hires / job_total) * 100 if job_total > 0 else 0

    conversion_data.append({
        'Job': job,
        'Total': job_total,
        'Hired': job_hires,
        'Rejected': job_rejected,
        'Active': job_active,
        'Conversion %': conv_rate
    })

    print(f"  • {job}:")
    print(f"      Total: {job_total} | Hired: {job_hires} | Rejected: {job_rejected} | Active: {job_active} | Conv: {conv_rate:.1f}%")

# =============================================================================
# 4. STAGE DISTRIBUTION
# =============================================================================
print("\n" + "="*80)
print("4. STAGE DISTRIBUTION")
print("="*80)

stage_counts = df['Stage name'].value_counts()
print(f"\nCandidates by Stage:")
for stage, count in stage_counts.items():
    pct = (count / len(df)) * 100
    print(f"  • {stage}: {count} ({pct:.1f}%)")

# =============================================================================
# 5. TIME TO HIRE ANALYSIS
# =============================================================================
print("\n" + "="*80)
print("5. TIME TO HIRE ANALYSIS")
print("="*80)

if len(hires_df) > 0:
    avg_time = hires_df['Time to Hire (days)'].mean()
    median_time = hires_df['Time to Hire (days)'].median()
    min_time = hires_df['Time to Hire (days)'].min()
    max_time = hires_df['Time to Hire (days)'].max()

    print(f"\nTime to Hire Statistics:")
    print(f"  • Average: {avg_time:.1f} days")
    print(f"  • Median: {median_time:.1f} days")
    print(f"  • Min: {min_time:.0f} days")
    print(f"  • Max: {max_time:.0f} days")

    print(f"\nAverage Time to Hire by Job:")
    for job in hires_df['Job title'].unique():
        job_hires = hires_df[hires_df['Job title'] == job]
        avg = job_hires['Time to Hire (days)'].mean()
        print(f"  • {job}: {avg:.1f} days")
else:
    print("\nNo hires with time to hire data available.")

# =============================================================================
# 6. QUARTERLY TRENDS
# =============================================================================
print("\n" + "="*80)
print("6. QUARTERLY TRENDS")
print("="*80)

print("\nApplications by Quarter:")
apps_by_quarter = df['Quarter'].value_counts().sort_index()
for quarter, count in apps_by_quarter.items():
    hired_q = len(df[(df['Quarter'] == quarter) & (df['Status'] == 'Hired')])
    rejected_q = len(df[(df['Quarter'] == quarter) & (df['Status'] == 'Rejected')])
    active_q = len(df[(df['Quarter'] == quarter) & (df['Status'] == 'Active')])
    conv_q = (hired_q / count) * 100 if count > 0 else 0
    print(f"  • {quarter}: {count} apps | {hired_q} hired | {rejected_q} rejected | {active_q} active | {conv_q:.1f}% conv")

# =============================================================================
# 7. TOP REJECTION REASONS BY STAGE
# =============================================================================
print("\n" + "="*80)
print("7. TOP REJECTION REASONS BY STAGE")
print("="*80)

top_stages = rejected_df['Stage name'].value_counts().head(10).index
for stage in top_stages:
    stage_rejected = rejected_df[rejected_df['Stage name'] == stage]
    print(f"\n{stage} ({len(stage_rejected)} rejections):")
    reasons = stage_rejected['Reject reason'].value_counts().head(3)
    for reason, count in reasons.items():
        pct = (count / len(stage_rejected)) * 100
        print(f"  • {reason}: {count} ({pct:.1f}%)")

# =============================================================================
# 8. SUMMARY STATISTICS BY JOB
# =============================================================================
print("\n" + "="*80)
print("8. DETAILED SUMMARY BY JOB TITLE")
print("="*80)

for job in sorted(df['Job title'].unique()):
    job_df = df[df['Job title'] == job]
    job_hired = len(job_df[job_df['Status'] == 'Hired'])
    job_rejected = len(job_df[job_df['Status'] == 'Rejected'])
    job_active = len(job_df[job_df['Status'] == 'Active'])

    print(f"\n{job}:")
    print(f"  Total Applications: {len(job_df)}")
    print(f"  Hired: {job_hired} ({(job_hired/len(job_df))*100:.1f}%)")
    print(f"  Rejected: {job_rejected} ({(job_rejected/len(job_df))*100:.1f}%)")
    print(f"  Active: {job_active} ({(job_active/len(job_df))*100:.1f}%)")

    if job_rejected > 0:
        print(f"  Top 3 Rejection Reasons:")
        job_rejected_df = job_df[job_df['Status'] == 'Rejected']
        top_reasons = job_rejected_df['Reject reason'].value_counts().head(3)
        for reason, count in top_reasons.items():
            print(f"    - {reason}: {count}")

# =============================================================================
# SAVE TO JSON
# =============================================================================
print("\n" + "="*80)
print("SAVING METRICS TO JSON...")
print("="*80)

metrics = {
    'summary': {
        'total_applications': int(total_applications),
        'total_hired': int(total_hired),
        'total_rejected': int(total_rejected),
        'total_active': int(total_active),
        'overall_conversion_rate': float(overall_conversion),
        'date_range': {
            'start': str(df['Created at'].min()),
            'end': str(df['Created at'].max())
        }
    },
    'hires': {
        'by_job': hires_by_job.to_dict(),
        'by_quarter': hires_by_quarter.to_dict(),
        'by_month': hires_by_month.to_dict()
    },
    'rejections': {
        'total': int(len(rejected_df)),
        'by_reason': rejection_reasons.head(20).to_dict(),
        'by_stage': rejection_by_stage.to_dict()
    },
    'conversion_by_job': {item['Job']: {
        'total': int(item['Total']),
        'hired': int(item['Hired']),
        'rejected': int(item['Rejected']),
        'active': int(item['Active']),
        'conversion_rate': float(item['Conversion %'])
    } for item in conversion_data},
    'time_to_hire': {
        'average': float(avg_time) if len(hires_df) > 0 else None,
        'median': float(median_time) if len(hires_df) > 0 else None,
        'min': float(min_time) if len(hires_df) > 0 else None,
        'max': float(max_time) if len(hires_df) > 0 else None,
        'by_job': {job: float(hires_df[hires_df['Job title'] == job]['Time to Hire (days)'].mean())
                   for job in hires_df['Job title'].unique()} if len(hires_df) > 0 else {}
    },
    'stage_distribution': stage_counts.to_dict(),
    'quarterly_trends': {quarter: {
        'applications': int(count),
        'hired': int(len(df[(df['Quarter'] == quarter) & (df['Status'] == 'Hired')])),
        'rejected': int(len(df[(df['Quarter'] == quarter) & (df['Status'] == 'Rejected')])),
        'active': int(len(df[(df['Quarter'] == quarter) & (df['Status'] == 'Active')]))
    } for quarter, count in apps_by_quarter.items()}
}

with open('hiring_metrics.json', 'w', encoding='utf-8') as f:
    json.dump(metrics, f, indent=2, ensure_ascii=False)

print("✓ Metrics saved to hiring_metrics.json")
print("\nAnalysis complete!")
