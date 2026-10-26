import csv
import math
import subprocess
import os

# 1. Load Data
data = []
with open('/mnt/alterra/repo/life-expectancy-analysis/data/life_expectancy_data.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        data.append({
            'Country': row['Country'],
            'Region': row['Region'],
            'Life_Expectancy': float(row['Life_Expectancy']),
            'GDP_Per_Capita': float(row['GDP_Per_Capita']),
            'Healthcare_Expenditure_Pct': float(row['Healthcare_Expenditure_Pct']),
            'Population_Millions': float(row['Population_Millions']),
            'Adult_Literacy_Rate': float(row['Adult_Literacy_Rate'])
        })

print(f"Loaded {len(data)} records.")

# 2. Compute Summary Statistics
def get_stats(values):
    s = sorted(values)
    n = len(s)
    mean_val = sum(s) / n
    median_val = (s[n//2] if n % 2 != 0 else (s[n//2 - 1] + s[n//2]) / 2)
    var = sum((x - mean_val)**2 for x in s) / (n - 1)
    sd_val = math.sqrt(var)
    return {
        'mean': mean_val,
        'median': median_val,
        'sd': sd_val,
        'min': min(s),
        'max': max(s)
    }

life_stats = get_stats([d['Life_Expectancy'] for d in data])
gdp_stats = get_stats([d['GDP_Per_Capita'] for d in data])
health_stats = get_stats([d['Healthcare_Expenditure_Pct'] for d in data])
pop_stats = get_stats([d['Population_Millions'] for d in data])
lit_stats = get_stats([d['Adult_Literacy_Rate'] for d in data])

# Correlation
def pearson_corr(x, y):
    n = len(x)
    mx = sum(x) / n
    my = sum(y) / n
    num = sum((x[i] - mx) * (y[i] - my) for i in range(n))
    den = math.sqrt(sum((x[i] - mx)**2 for i in range(n)) * sum((y[i] - my)**2 for i in range(n)))
    return num / den if den != 0 else 0

corr_gdp = pearson_corr([d['GDP_Per_Capita'] for d in data], [d['Life_Expectancy'] for d in data])
corr_health = pearson_corr([d['Healthcare_Expenditure_Pct'] for d in data], [d['Life_Expectancy'] for d in data])
corr_lit = pearson_corr([d['Adult_Literacy_Rate'] for d in data], [d['Life_Expectancy'] for d in data])

# Region Aggregates
regions = sorted(list(set(d['Region'] for d in data)))
region_summary = {}
for r in regions:
    sub = [d for d in data if d['Region'] == r]
    region_summary[r] = {
        'count': len(sub),
        'avg_life': sum(d['Life_Expectancy'] for d in sub) / len(sub),
        'median_life': get_stats([d['Life_Expectancy'] for d in sub])['median'],
        'avg_gdp': sum(d['GDP_Per_Capita'] for d in sub) / len(sub),
        'avg_health': sum(d['Healthcare_Expenditure_Pct'] for d in sub) / len(sub),
        'avg_lit': sum(d['Adult_Literacy_Rate'] for d in sub) / len(sub),
        'life_values': [d['Life_Expectancy'] for d in sub]
    }

print("Stats computed successfully.")
print(f"Global Life Expectancy Mean: {life_stats['mean']:.2f}, SD: {life_stats['sd']:.2f}")
print(f"Corr GDP: {corr_gdp:.3f}, Health: {corr_health:.3f}, Literacy: {corr_lit:.3f}")
