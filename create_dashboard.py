import json
import pandas as pd

# Read the metrics
with open('hiring_metrics.json', 'r', encoding='utf-8') as f:
    metrics = json.load(f)

# Read the raw data
df = pd.read_csv('hiring_complete.csv')

# Create HTML dashboard
html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hiring Analytics Dashboard - Last 6 Months</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: #f5f7fa;
            color: #2d3748;
            padding: 20px;
            line-height: 1.6;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}

        h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            color: #1a202c;
        }}

        .date-range {{
            color: #718096;
            font-size: 0.95em;
            margin-bottom: 30px;
        }}

        .summary-cards {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}

        .card {{
            background: white;
            border-radius: 12px;
            padding: 25px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}

        .card-title {{
            font-size: 0.85em;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: #718096;
            margin-bottom: 10px;
            font-weight: 600;
        }}

        .card-value {{
            font-size: 2.5em;
            font-weight: 700;
            color: #2d3748;
        }}

        .card-subtitle {{
            font-size: 0.9em;
            color: #a0aec0;
            margin-top: 5px;
        }}

        .metric-positive {{
            color: #38a169;
        }}

        .metric-negative {{
            color: #e53e3e;
        }}

        .metric-neutral {{
            color: #3182ce;
        }}

        .section {{
            background: white;
            border-radius: 12px;
            padding: 30px;
            margin-bottom: 25px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}

        .section-title {{
            font-size: 1.5em;
            margin-bottom: 20px;
            color: #1a202c;
            border-bottom: 2px solid #e2e8f0;
            padding-bottom: 10px;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }}

        th, td {{
            text-align: left;
            padding: 12px;
            border-bottom: 1px solid #e2e8f0;
        }}

        th {{
            background: #f7fafc;
            font-weight: 600;
            color: #4a5568;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        tr:hover {{
            background: #f7fafc;
        }}

        .progress-bar {{
            background: #e2e8f0;
            height: 8px;
            border-radius: 4px;
            overflow: hidden;
            margin-top: 8px;
        }}

        .progress-fill {{
            background: linear-gradient(90deg, #4299e1, #3182ce);
            height: 100%;
            transition: width 0.3s ease;
        }}

        .badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.85em;
            font-weight: 600;
        }}

        .badge-success {{
            background: #c6f6d5;
            color: #22543d;
        }}

        .badge-danger {{
            background: #fed7d7;
            color: #742a2a;
        }}

        .badge-warning {{
            background: #feebc8;
            color: #7c2d12;
        }}

        .badge-info {{
            background: #bee3f8;
            color: #2c5282;
        }}

        .grid-2 {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 25px;
        }}

        @media (max-width: 768px) {{
            .grid-2 {{
                grid-template-columns: 1fr;
            }}
        }}

        .list-item {{
            padding: 10px 0;
            border-bottom: 1px solid #e2e8f0;
        }}

        .list-item:last-child {{
            border-bottom: none;
        }}

        .flex-between {{
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .number-badge {{
            background: #edf2f7;
            color: #4a5568;
            padding: 2px 8px;
            border-radius: 4px;
            font-weight: 600;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Hiring Analytics Dashboard</h1>
        <div class="date-range">Period: {metrics['summary']['date_range']['start'][:10]} to {metrics['summary']['date_range']['end'][:10]}</div>

        <!-- Summary Cards -->
        <div class="summary-cards">
            <div class="card">
                <div class="card-title">Total Applications</div>
                <div class="card-value">{metrics['summary']['total_applications']}</div>
                <div class="card-subtitle">Last 6 months</div>
            </div>

            <div class="card">
                <div class="card-title">Hired</div>
                <div class="card-value metric-positive">{metrics['summary']['total_hired']}</div>
                <div class="card-subtitle">{metrics['summary']['total_hired']/metrics['summary']['total_applications']*100:.1f}% conversion rate</div>
            </div>

            <div class="card">
                <div class="card-title">Rejected</div>
                <div class="card-value metric-negative">{metrics['summary']['total_rejected']}</div>
                <div class="card-subtitle">{metrics['summary']['total_rejected']/metrics['summary']['total_applications']*100:.1f}% rejection rate</div>
            </div>

            <div class="card">
                <div class="card-title">Active (In Process)</div>
                <div class="card-value metric-neutral">{metrics['summary']['total_active']}</div>
                <div class="card-subtitle">{metrics['summary']['total_active']/metrics['summary']['total_applications']*100:.1f}% in pipeline</div>
            </div>
        </div>

        <!-- Conversion by Job -->
        <div class="section">
            <h2 class="section-title">Conversion Rate by Job Title</h2>
            <table>
                <thead>
                    <tr>
                        <th>Job Title</th>
                        <th>Total</th>
                        <th>Hired</th>
                        <th>Rejected</th>
                        <th>Active</th>
                        <th>Conversion %</th>
                    </tr>
                </thead>
                <tbody>
"""

# Add job conversion data
for job, data in metrics['conversion_by_job'].items():
    conv_badge = 'badge-success' if data['conversion_rate'] > 2 else 'badge-danger' if data['conversion_rate'] < 1 else 'badge-warning'
    html += f"""
                    <tr>
                        <td><strong>{job}</strong></td>
                        <td>{data['total']}</td>
                        <td>{data['hired']}</td>
                        <td>{data['rejected']}</td>
                        <td>{data['active']}</td>
                        <td><span class="badge {conv_badge}">{data['conversion_rate']:.1f}%</span></td>
                    </tr>
"""

html += """
                </tbody>
            </table>
        </div>

        <!-- Grid Layout -->
        <div class="grid-2">
            <!-- Quarterly Trends -->
            <div class="section">
                <h2 class="section-title">Quarterly Trends</h2>
"""

for quarter, data in sorted(metrics['quarterly_trends'].items()):
    conv = (data['hired'] / data['applications'] * 100) if data['applications'] > 0 else 0
    html += f"""
                <div class="list-item">
                    <div class="flex-between">
                        <strong>{quarter}</strong>
                        <span class="number-badge">{data['applications']} apps</span>
                    </div>
                    <div style="font-size: 0.9em; color: #718096; margin-top: 5px;">
                        Hired: {data['hired']} | Rejected: {data['rejected']} | Active: {data['active']} | Conv: {conv:.1f}%
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: {conv}%"></div>
                    </div>
                </div>
"""

html += """
            </div>

            <!-- Time to Hire -->
            <div class="section">
                <h2 class="section-title">Time to Hire</h2>
"""

if metrics['time_to_hire']['average']:
    html += f"""
                <div class="list-item">
                    <div class="flex-between">
                        <span>Average</span>
                        <strong>{metrics['time_to_hire']['average']:.1f} days</strong>
                    </div>
                </div>
                <div class="list-item">
                    <div class="flex-between">
                        <span>Median</span>
                        <strong>{metrics['time_to_hire']['median']:.1f} days</strong>
                    </div>
                </div>
                <div class="list-item">
                    <div class="flex-between">
                        <span>Min</span>
                        <strong>{metrics['time_to_hire']['min']:.0f} days</strong>
                    </div>
                </div>
                <div class="list-item">
                    <div class="flex-between">
                        <span>Max</span>
                        <strong>{metrics['time_to_hire']['max']:.0f} days</strong>
                    </div>
                </div>
"""
else:
    html += "<p>No time to hire data available</p>"

html += """
            </div>
        </div>

        <!-- Top Rejection Reasons -->
        <div class="section">
            <h2 class="section-title">Top Rejection Reasons</h2>
            <table>
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Reason</th>
                        <th>Count</th>
                        <th>Percentage</th>
                    </tr>
                </thead>
                <tbody>
"""

total_rejected = metrics['summary']['total_rejected']
for i, (reason, count) in enumerate(list(metrics['rejections']['by_reason'].items())[:15], 1):
    pct = (count / total_rejected * 100) if total_rejected > 0 else 0
    html += f"""
                    <tr>
                        <td>{i}</td>
                        <td>{reason}</td>
                        <td>{count}</td>
                        <td>{pct:.1f}%</td>
                    </tr>
"""

html += """
                </tbody>
            </table>
        </div>

        <!-- Stage Distribution -->
        <div class="section">
            <h2 class="section-title">Candidate Distribution by Stage</h2>
            <table>
                <thead>
                    <tr>
                        <th>Stage</th>
                        <th>Count</th>
                        <th>Percentage</th>
                        <th>Distribution</th>
                    </tr>
                </thead>
                <tbody>
"""

total_apps = metrics['summary']['total_applications']
for stage, count in metrics['stage_distribution'].items():
    pct = (count / total_apps * 100) if total_apps > 0 else 0
    html += f"""
                    <tr>
                        <td><strong>{stage}</strong></td>
                        <td>{count}</td>
                        <td>{pct:.1f}%</td>
                        <td>
                            <div class="progress-bar">
                                <div class="progress-fill" style="width: {pct}%"></div>
                            </div>
                        </td>
                    </tr>
"""

html += """
                </tbody>
            </table>
        </div>

        <!-- Rejections by Stage -->
        <div class="section">
            <h2 class="section-title">Rejections by Stage</h2>
            <table>
                <thead>
                    <tr>
                        <th>Stage</th>
                        <th>Rejections</th>
                        <th>% of Total Rejections</th>
                    </tr>
                </thead>
                <tbody>
"""

for stage, count in metrics['rejections']['by_stage'].items():
    pct = (count / total_rejected * 100) if total_rejected > 0 else 0
    html += f"""
                    <tr>
                        <td>{stage}</td>
                        <td>{count}</td>
                        <td>{pct:.1f}%</td>
                    </tr>
"""

html += """
                </tbody>
            </table>
        </div>

    </div>

    <script>
        // Add animation on load
        window.addEventListener('load', () => {
            const progressBars = document.querySelectorAll('.progress-fill');
            progressBars.forEach(bar => {
                const width = bar.style.width;
                bar.style.width = '0%';
                setTimeout(() => {
                    bar.style.width = width;
                }, 100);
            });
        });
    </script>
</body>
</html>
"""

# Write the HTML file
with open('hiring_analytics_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("✓ Dashboard created successfully: hiring_analytics_dashboard.html")
print("\nYou can open this file in your browser to view the interactive dashboard!")
