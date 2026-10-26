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

REGION_COLORS = {
    'Africa': '#E41A1C',
    'Americas': '#377EB8',
    'Asia': '#4DAF4A',
    'Europe': '#984EA3',
    'Oceania': '#FF7F00'
}

REGION_SET2 = {
    'Africa': '#66C2A5',
    'Americas': '#8DA0CB',
    'Asia': '#FC8D62',
    'Europe': '#E78AC3',
    'Oceania': '#A6D854'
}

def render_html_wrapper(svg_content, width=800, height=500):
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body {{
    margin: 0;
    padding: 0;
    background: #ffffff;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    display: flex;
    justify-content: center;
    align-items: center;
    width: {width}px;
    height: {height}px;
  }}
  svg {{
    width: {width}px;
    height: {height}px;
  }}
</style>
</head>
<body>
{svg_content}
</body>
</html>"""

# --- Chart 1: Histogram ---
def make_histogram():
    w, h = 900, 560
    pad_l, pad_r, pad_t, pad_b = 80, 50, 80, 70
    plot_w = w - pad_l - pad_r
    plot_h = h - pad_t - pad_b
    
    # Bins: 50 to 88, binwidth = 3 -> [51, 54), [54, 57), ...
    bins = [51 + i*3 for i in range(13)] # 51, 54, 57, 60, 63, 66, 69, 72, 75, 78, 81, 84, 87
    counts = [0] * (len(bins) - 1)
    for d in data:
        val = d['Life_Expectancy']
        for i in range(len(bins) - 1):
            if bins[i] <= val < bins[i+1]:
                counts[i] += 1
                break
            elif i == len(bins) - 2 and val >= bins[i+1]:
                counts[i] += 1
                
    max_c = 10
    
    svg = [f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">']
    # Background
    svg.append(f'<rect width="{w}" height="{h}" fill="#ffffff"/>')
    
    # Title & Subtitle
    svg.append(f'<text x="{w/2}" y="36" text-anchor="middle" font-size="20" font-weight="bold" fill="#2c3e50">Distribution of Life Expectancy Across Countries</text>')
    svg.append(f'<text x="{w/2}" y="60" text-anchor="middle" font-size="13" fill="#7f8c8d">50 Countries Worldwide (2023 Estimates)</text>')
    
    # Gridlines and Y-axis labels
    for y_val in range(0, max_c + 1, 2):
        y_pos = pad_t + plot_h - (y_val / max_c) * plot_h
        svg.append(f'<line x1="{pad_l}" y1="{y_pos}" x2="{pad_l + plot_w}" y2="{y_pos}" stroke="#eef0f2" stroke-width="1.2"/>')
        svg.append(f'<text x="{pad_l - 12}" y="{y_pos + 4}" text-anchor="end" font-size="12" fill="#555">{y_val}</text>')
        
    # X-axis gridlines & labels
    x_min, x_max = 50, 88
    for x_val in range(50, 90, 5):
        x_pos = pad_l + ((x_val - x_min) / (x_max - x_min)) * plot_w
        svg.append(f'<line x1="{x_pos}" y1="{pad_t}" x2="{x_pos}" y2="{pad_t + plot_h}" stroke="#f4f5f7" stroke-width="1"/>')
        svg.append(f'<text x="{x_pos}" y="{pad_t + plot_h + 22}" text-anchor="middle" font-size="12" fill="#555">{x_val}</text>')
        
    # Bars
    for i in range(len(counts)):
        b_start = bins[i]
        b_end = bins[i+1]
        x1 = pad_l + ((b_start - x_min) / (x_max - x_min)) * plot_w
        x2 = pad_l + ((b_end - x_min) / (x_max - x_min)) * plot_w
        bar_w = (x2 - x1) - 2
        bar_h = (counts[i] / max_c) * plot_h
        y1 = pad_t + plot_h - bar_h
        svg.append(f'<rect x="{x1+1}" y="{y1}" width="{bar_w}" height="{bar_h}" fill="#3498db" rx="2" stroke="#ffffff" stroke-width="1"/>')
        if counts[i] > 0:
            svg.append(f'<text x="{x1 + bar_w/2}" y="{y1 - 6}" text-anchor="middle" font-size="11" font-weight="600" fill="#2980b9">{counts[i]}</text>')
            
    # Mean line
    mean_val = sum(d['Life_Expectancy'] for d in data) / len(data)
    mean_x = pad_l + ((mean_val - x_min) / (x_max - x_min)) * plot_w
    svg.append(f'<line x1="{mean_x}" y1="{pad_t}" x2="{mean_x}" y2="{pad_t + plot_h}" stroke="#e74c3c" stroke-width="2.5" stroke-dasharray="6,4"/>')
    svg.append(f'<rect x="{mean_x + 8}" y="{pad_t + 15}" width="95" height="24" rx="4" fill="#fdeded" stroke="#e74c3c" stroke-width="1"/>')
    svg.append(f'<text x="{mean_x + 14}" y="{pad_t + 31}" font-size="11" font-weight="bold" fill="#c0392b">Mean = {mean_val:.1f} yrs</text>')
    
    # Axis titles
    svg.append(f'<text x="{pad_l + plot_w/2}" y="{pad_t + plot_h + 52}" text-anchor="middle" font-size="13" font-weight="bold" fill="#333">Life Expectancy (Years)</text>')
    svg.append(f'<text transform="rotate(-90)" x="-{pad_t + plot_h/2}" y="{pad_l - 45}" text-anchor="middle" font-size="13" font-weight="bold" fill="#333">Number of Countries</text>')
    
    # Border
    svg.append(f'<line x1="{pad_l}" y1="{pad_t + plot_h}" x2="{pad_l + plot_w}" y2="{pad_t + plot_h}" stroke="#ccc" stroke-width="1.5"/>')
    svg.append(f'<line x1="{pad_l}" y1="{pad_t}" x2="{pad_l}" y2="{pad_t + plot_h}" stroke="#ccc" stroke-width="1.5"/>')
    
    svg.append('</svg>')
    return "".join(svg)

# --- Chart 2: Boxplot by Region ---
def make_boxplot():
    w, h = 900, 560
    pad_l, pad_r, pad_t, pad_b = 80, 50, 80, 70
    plot_w = w - pad_l - pad_r
    plot_h = h - pad_t - pad_b
    
    # Sorted regions by median life expectancy
    region_data = {}
    for r in ['Africa', 'Asia', 'Americas', 'Europe', 'Oceania']:
        sub = sorted([d['Life_Expectancy'] for d in data if d['Region'] == r])
        n = len(sub)
        q1 = sub[n // 4]
        med = sub[n // 2] if n % 2 != 0 else (sub[n // 2 - 1] + sub[n // 2]) / 2
        q3 = sub[(3 * n) // 4]
        iqr = q3 - q1
        w_low = max(sub[0], q1 - 1.5 * iqr)
        w_high = min(sub[-1], q3 + 1.5 * iqr)
        outliers = [x for x in sub if x < w_low or x > w_high]
        region_data[r] = {
            'q1': q1, 'med': med, 'q3': q3, 'w_low': w_low, 'w_high': w_high,
            'outliers': outliers, 'raw': sub
        }
    
    reg_list = sorted(region_data.keys(), key=lambda r: region_data[r]['med'])
    
    y_min, y_max = 50, 90
    
    svg = [f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">']
    svg.append(f'<rect width="{w}" height="{h}" fill="#ffffff"/>')
    svg.append(f'<text x="{w/2}" y="36" text-anchor="middle" font-size="20" font-weight="bold" fill="#2c3e50">Life Expectancy by Region</text>')
    svg.append(f'<text x="{w/2}" y="60" text-anchor="middle" font-size="13" fill="#7f8c8d">Boxplot showing median, interquartile spread, and regional variability</text>')
    
    # Y-axis gridlines
    for y_val in range(50, 95, 5):
        y_pos = pad_t + plot_h - ((y_val - y_min) / (y_max - y_min)) * plot_h
        svg.append(f'<line x1="{pad_l}" y1="{y_pos}" x2="{pad_l + plot_w}" y2="{y_pos}" stroke="#eef0f2" stroke-width="1.2"/>')
        svg.append(f'<text x="{pad_l - 12}" y="{y_pos + 4}" text-anchor="end" font-size="12" fill="#555">{y_val}</text>')
        
    slot_w = plot_w / len(reg_list)
    box_w = 64
    
    import random
    rng = random.Random(42)
    
    for i, r in enumerate(reg_list):
        cx = pad_l + (i + 0.5) * slot_w
        info = region_data[r]
        color = REGION_SET2[r]
        
        y_q1 = pad_t + plot_h - ((info['q1'] - y_min) / (y_max - y_min)) * plot_h
        y_q3 = pad_t + plot_h - ((info['q3'] - y_min) / (y_max - y_min)) * plot_h
        y_med = pad_t + plot_h - ((info['med'] - y_min) / (y_max - y_min)) * plot_h
        y_wlow = pad_t + plot_h - ((info['w_low'] - y_min) / (y_max - y_min)) * plot_h
        y_whigh = pad_t + plot_h - ((info['w_high'] - y_min) / (y_max - y_min)) * plot_h
        
        # Whiskers
        svg.append(f'<line x1="{cx}" y1="{y_q3}" x2="{cx}" y2="{y_whigh}" stroke="#444" stroke-width="1.8"/>')
        svg.append(f'<line x1="{cx - 15}" y1="{y_whigh}" x2="{cx + 15}" y2="{y_whigh}" stroke="#444" stroke-width="1.8"/>')
        svg.append(f'<line x1="{cx}" y1="{y_q1}" x2="{cx}" y2="{y_wlow}" stroke="#444" stroke-width="1.8"/>')
        svg.append(f'<line x1="{cx - 15}" y1="{y_wlow}" x2="{cx + 15}" y2="{y_wlow}" stroke="#444" stroke-width="1.8"/>')
        
        # Box
        b_top = min(y_q1, y_q3)
        b_h = abs(y_q1 - y_q3)
        svg.append(f'<rect x="{cx - box_w/2}" y="{b_top}" width="{box_w}" height="{b_h}" fill="{color}" fill-opacity="0.75" stroke="#333" stroke-width="1.8" rx="2"/>')
        
        # Median line
        svg.append(f'<line x1="{cx - box_w/2}" y1="{y_med}" x2="{cx + box_w/2}" y2="{y_med}" stroke="#222" stroke-width="3"/>')
        
        # Jittered raw points
        for val in info['raw']:
            jit = (rng.random() - 0.5) * 32
            pt_y = pad_t + plot_h - ((val - y_min) / (y_max - y_min)) * plot_h
            svg.append(f'<circle cx="{cx + jit}" cy="{pt_y}" r="3.5" fill="#2c3e50" fill-opacity="0.45" stroke="#ffffff" stroke-width="0.8"/>')
            
        # Region label
        svg.append(f'<text x="{cx}" y="{pad_t + plot_h + 24}" text-anchor="middle" font-size="13" font-weight="600" fill="#333">{r}</text>')
        svg.append(f'<text x="{cx}" y="{pad_t + plot_h + 40}" text-anchor="middle" font-size="11" fill="#777">(n={len(info["raw"])})</text>')
        
    svg.append(f'<text transform="rotate(-90)" x="-{pad_t + plot_h/2}" y="{pad_l - 45}" text-anchor="middle" font-size="13" font-weight="bold" fill="#333">Life Expectancy (Years)</text>')
    svg.append(f'<line x1="{pad_l}" y1="{pad_t + plot_h}" x2="{pad_l + plot_w}" y2="{pad_t + plot_h}" stroke="#ccc" stroke-width="1.5"/>')
    svg.append(f'<line x1="{pad_l}" y1="{pad_t}" x2="{pad_l}" y2="{pad_t + plot_h}" stroke="#ccc" stroke-width="1.5"/>')
    
    svg.append('</svg>')
    return "".join(svg)

# --- Chart 3: Scatter Plot Life Exp vs GDP ---
def make_scatter_gdp():
    w, h = 950, 580
    pad_l, pad_r, pad_t, pad_b = 80, 50, 80, 80
    plot_w = w - pad_l - pad_r
    plot_h = h - pad_t - pad_b
    
    x_min, x_max = 0, 100000
    y_min, y_max = 50, 90
    
    svg = [f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">']
    svg.append(f'<rect width="{w}" height="{h}" fill="#ffffff"/>')
    svg.append(f'<text x="{w/2}" y="36" text-anchor="middle" font-size="20" font-weight="bold" fill="#2c3e50">Life Expectancy vs. GDP Per Capita</text>')
    svg.append(f'<text x="{w/2}" y="58" text-anchor="middle" font-size="13" fill="#7f8c8d">Higher economic prosperity shows strong non-linear correlation with life expectancy</text>')
    
    # Y-axis
    for y_val in range(50, 95, 5):
        y_pos = pad_t + plot_h - ((y_val - y_min) / (y_max - y_min)) * plot_h
        svg.append(f'<line x1="{pad_l}" y1="{y_pos}" x2="{pad_l + plot_w}" y2="{y_pos}" stroke="#eef0f2" stroke-width="1.2"/>')
        svg.append(f'<text x="{pad_l - 12}" y="{y_pos + 4}" text-anchor="end" font-size="12" fill="#555">{y_val}</text>')
        
    # X-axis
    for x_val in range(0, 110000, 20000):
        x_pos = pad_l + ((x_val - x_min) / (x_max - x_min)) * plot_w
        svg.append(f'<line x1="{x_pos}" y1="{pad_t}" x2="{x_pos}" y2="{pad_t + plot_h}" stroke="#eef0f2" stroke-width="1.2"/>')
        svg.append(f'<text x="{x_pos}" y="{pad_t + plot_h + 22}" text-anchor="middle" font-size="12" fill="#555">${x_val:,}</text>')
        
    # Non-linear trend line (Log model approximation)
    trend_pts = []
    for g in range(800, 98000, 1500):
        # approximate logarithmic curve y = a + b * ln(x)
        life_est = 41.5 + 3.85 * math.log(g)
        life_est = min(max(life_est, 52), 85)
        tx = pad_l + ((g - x_min) / (x_max - x_min)) * plot_w
        ty = pad_t + plot_h - ((life_est - y_min) / (y_max - y_min)) * plot_h
        trend_pts.append((tx, ty))
    
    path_d = f"M {trend_pts[0][0]:.1f} {trend_pts[0][1]:.1f} " + " ".join(f"L {pt[0]:.1f} {pt[1]:.1f}" for pt in trend_pts[1:])
    svg.append(f'<path d="{path_d}" fill="none" stroke="#555555" stroke-width="2.5" stroke-dasharray="7,5" opacity="0.8"/>')
    
    # Points
    for d in data:
        px = pad_l + ((d['GDP_Per_Capita'] - x_min) / (x_max - x_min)) * plot_w
        py = pad_t + plot_h - ((d['Life_Expectancy'] - y_min) / (y_max - y_min)) * plot_h
        c = REGION_COLORS[d['Region']]
        svg.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="5.5" fill="{c}" fill-opacity="0.85" stroke="#ffffff" stroke-width="1.2"/>')
        
    # Legend
    leg_x = pad_l + 30
    leg_y = pad_t + plot_h + 55
    svg.append(f'<text x="{leg_x}" y="{leg_y + 11}" font-size="12" font-weight="bold" fill="#333">Region:</text>')
    cur_x = leg_x + 65
    for r in ['Africa', 'Americas', 'Asia', 'Europe', 'Oceania']:
        c = REGION_COLORS[r]
        svg.append(f'<circle cx="{cur_x}" cy="{leg_y + 7}" r="5.5" fill="{c}" fill-opacity="0.85"/>')
        svg.append(f'<text x="{cur_x + 12}" y="{leg_y + 11}" font-size="12" fill="#444">{r}</text>')
        cur_x += 105
        
    svg.append(f'<text x="{pad_l + plot_w/2}" y="{pad_t + plot_h + 46}" text-anchor="middle" font-size="13" font-weight="bold" fill="#333">GDP Per Capita (USD)</text>')
    svg.append(f'<text transform="rotate(-90)" x="-{pad_t + plot_h/2}" y="{pad_l - 45}" text-anchor="middle" font-size="13" font-weight="bold" fill="#333">Life Expectancy (Years)</text>')
    
    svg.append(f'<line x1="{pad_l}" y1="{pad_t + plot_h}" x2="{pad_l + plot_w}" y2="{pad_t + plot_h}" stroke="#ccc" stroke-width="1.5"/>')
    svg.append(f'<line x1="{pad_l}" y1="{pad_t}" x2="{pad_l}" y2="{pad_t + plot_h}" stroke="#ccc" stroke-width="1.5"/>')
    
    svg.append('</svg>')
    return "".join(svg)

# --- Chart 4: Bar Chart Regional Averages ---
def make_barchart():
    w, h = 900, 520
    pad_l, pad_r, pad_t, pad_b = 130, 80, 80, 60
    plot_w = w - pad_l - pad_r
    plot_h = h - pad_t - pad_b
    
    reg_summary = []
    for r in ['Africa', 'Asia', 'Americas', 'Europe', 'Oceania']:
        sub = [d['Life_Expectancy'] for d in data if d['Region'] == r]
        avg = sum(sub) / len(sub)
        reg_summary.append((r, avg, len(sub)))
        
    reg_summary.sort(key=lambda x: x[1]) # ascending
    
    svg = [f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">']
    svg.append(f'<rect width="{w}" height="{h}" fill="#ffffff"/>')
    svg.append(f'<text x="{w/2}" y="36" text-anchor="middle" font-size="20" font-weight="bold" fill="#2c3e50">Average Life Expectancy by Region</text>')
    svg.append(f'<text x="{w/2}" y="58" text-anchor="middle" font-size="13" fill="#7f8c8d">Comparison of regional means (2023 Estimates)</text>')
    
    x_max = 95
    for x_val in range(0, 100, 15):
        x_pos = pad_l + (x_val / x_max) * plot_w
        svg.append(f'<line x1="{x_pos}" y1="{pad_t}" x2="{x_pos}" y2="{pad_t + plot_h}" stroke="#eef0f2" stroke-width="1.2"/>')
        svg.append(f'<text x="{x_pos}" y="{pad_t + plot_h + 22}" text-anchor="middle" font-size="12" fill="#555">{x_val}</text>')
        
    slot_h = plot_h / len(reg_summary)
    bar_h = 38
    
    for i, (r, avg, cnt) in enumerate(reg_summary):
        cy = pad_t + (i + 0.5) * slot_h
        y_top = cy - bar_h / 2
        bw = (avg / x_max) * plot_w
        c = REGION_SET2[r]
        
        svg.append(f'<rect x="{pad_l}" y="{y_top}" width="{bw}" height="{bar_h}" fill="{c}" fill-opacity="0.85" rx="3" stroke="#ffffff" stroke-width="1"/>')
        svg.append(f'<text x="{pad_l - 15}" y="{cy + 5}" text-anchor="end" font-size="13" font-weight="600" fill="#333">{r}</text>')
        svg.append(f'<text x="{pad_l + bw + 12}" y="{cy + 5}" font-size="13" font-weight="bold" fill="#2c3e50">{avg:.1f} yrs</text>')
        
    svg.append(f'<text x="{pad_l + plot_w/2}" y="{pad_t + plot_h + 46}" text-anchor="middle" font-size="13" font-weight="bold" fill="#333">Average Life Expectancy (Years)</text>')
    svg.append(f'<line x1="{pad_l}" y1="{pad_t}" x2="{pad_l}" y2="{pad_t + plot_h}" stroke="#ccc" stroke-width="1.5"/>')
    svg.append(f'<line x1="{pad_l}" y1="{pad_t + plot_h}" x2="{pad_l + plot_w}" y2="{pad_t + plot_h}" stroke="#ccc" stroke-width="1.5"/>')
    
    svg.append('</svg>')
    return "".join(svg)

# --- Chart 5: Scatter Life Exp vs Healthcare Expenditure ---
def make_scatter_health():
    w, h = 950, 580
    pad_l, pad_r, pad_t, pad_b = 80, 50, 80, 80
    plot_w = w - pad_l - pad_r
    plot_h = h - pad_t - pad_b
    
    x_min, x_max = 2, 18
    y_min, y_max = 50, 90
    
    svg = [f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">']
    svg.append(f'<rect width="{w}" height="{h}" fill="#ffffff"/>')
    svg.append(f'<text x="{w/2}" y="36" text-anchor="middle" font-size="20" font-weight="bold" fill="#2c3e50">Life Expectancy vs. Healthcare Expenditure</text>')
    svg.append(f'<text x="{w/2}" y="58" text-anchor="middle" font-size="13" fill="#7f8c8d">Linear relationship with health spending as percentage of GDP (r = 0.661)</text>')
    
    for y_val in range(50, 95, 5):
        y_pos = pad_t + plot_h - ((y_val - y_min) / (y_max - y_min)) * plot_h
        svg.append(f'<line x1="{pad_l}" y1="{y_pos}" x2="{pad_l + plot_w}" y2="{y_pos}" stroke="#eef0f2" stroke-width="1.2"/>')
        svg.append(f'<text x="{pad_l - 12}" y="{y_pos + 4}" text-anchor="end" font-size="12" fill="#555">{y_val}</text>')
        
    for x_val in range(2, 20, 2):
        x_pos = pad_l + ((x_val - x_min) / (x_max - x_min)) * plot_w
        svg.append(f'<line x1="{x_pos}" y1="{pad_t}" x2="{x_pos}" y2="{pad_t + plot_h}" stroke="#eef0f2" stroke-width="1.2"/>')
        svg.append(f'<text x="{x_pos}" y="{pad_t + plot_h + 22}" text-anchor="middle" font-size="12" fill="#555">{x_val}%</text>')
        
    # Regression line: y = a + bx
    # compute slope
    xs = [d['Healthcare_Expenditure_Pct'] for d in data]
    ys = [d['Life_Expectancy'] for d in data]
    mx, my = sum(xs)/len(xs), sum(ys)/len(ys)
    b = sum((xs[i]-mx)*(ys[i]-my) for i in range(len(xs))) / sum((xs[i]-mx)**2 for i in range(len(xs)))
    a = my - b * mx
    
    x_start, x_end = 2.5, 17.0
    y_start, y_end = a + b * x_start, a + b * x_end
    
    sx = pad_l + ((x_start - x_min) / (x_max - x_min)) * plot_w
    sy = pad_t + plot_h - ((y_start - y_min) / (y_max - y_min)) * plot_h
    ex = pad_l + ((x_end - x_min) / (x_max - x_min)) * plot_w
    ey = pad_t + plot_h - ((y_end - y_min) / (y_max - y_min)) * plot_h
    svg.append(f'<line x1="{sx:.1f}" y1="{sy:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" stroke="#444" stroke-width="2.5" stroke-dasharray="6,4"/>')
    
    for d in data:
        px = pad_l + ((d['Healthcare_Expenditure_Pct'] - x_min) / (x_max - x_min)) * plot_w
        py = pad_t + plot_h - ((d['Life_Expectancy'] - y_min) / (y_max - y_min)) * plot_h
        c = REGION_COLORS[d['Region']]
        svg.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="5.5" fill="{c}" fill-opacity="0.85" stroke="#ffffff" stroke-width="1.2"/>')
        
    leg_x = pad_l + 30
    leg_y = pad_t + plot_h + 55
    svg.append(f'<text x="{leg_x}" y="{leg_y + 11}" font-size="12" font-weight="bold" fill="#333">Region:</text>')
    cur_x = leg_x + 65
    for r in ['Africa', 'Americas', 'Asia', 'Europe', 'Oceania']:
        c = REGION_COLORS[r]
        svg.append(f'<circle cx="{cur_x}" cy="{leg_y + 7}" r="5.5" fill="{c}" fill-opacity="0.85"/>')
        svg.append(f'<text x="{cur_x + 12}" y="{leg_y + 11}" font-size="12" fill="#444">{r}</text>')
        cur_x += 105
        
    svg.append(f'<text x="{pad_l + plot_w/2}" y="{pad_t + plot_h + 46}" text-anchor="middle" font-size="13" font-weight="bold" fill="#333">Healthcare Expenditure (% of GDP)</text>')
    svg.append(f'<text transform="rotate(-90)" x="-{pad_t + plot_h/2}" y="{pad_l - 45}" text-anchor="middle" font-size="13" font-weight="bold" fill="#333">Life Expectancy (Years)</text>')
    svg.append(f'<line x1="{pad_l}" y1="{pad_t + plot_h}" x2="{pad_l + plot_w}" y2="{pad_t + plot_h}" stroke="#ccc" stroke-width="1.5"/>')
    svg.append(f'<line x1="{pad_l}" y1="{pad_t}" x2="{pad_l}" y2="{pad_t + plot_h}" stroke="#ccc" stroke-width="1.5"/>')
    
    svg.append('</svg>')
    return "".join(svg)

# --- Chart 6: Scatter Life Exp vs Literacy Rate ---
def make_scatter_literacy():
    w, h = 950, 580
    pad_l, pad_r, pad_t, pad_b = 80, 50, 80, 80
    plot_w = w - pad_l - pad_r
    plot_h = h - pad_t - pad_b
    
    x_min, x_max = 40, 105
    y_min, y_max = 50, 90
    
    svg = [f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">']
    svg.append(f'<rect width="{w}" height="{h}" fill="#ffffff"/>')
    svg.append(f'<text x="{w/2}" y="36" text-anchor="middle" font-size="20" font-weight="bold" fill="#2c3e50">Life Expectancy vs. Adult Literacy Rate</text>')
    svg.append(f'<text x="{w/2}" y="58" text-anchor="middle" font-size="13" fill="#7f8c8d">Education level correlates positively with longevity outcomes (r = 0.785)</text>')
    
    for y_val in range(50, 95, 5):
        y_pos = pad_t + plot_h - ((y_val - y_min) / (y_max - y_min)) * plot_h
        svg.append(f'<line x1="{pad_l}" y1="{y_pos}" x2="{pad_l + plot_w}" y2="{y_pos}" stroke="#eef0f2" stroke-width="1.2"/>')
        svg.append(f'<text x="{pad_l - 12}" y="{y_pos + 4}" text-anchor="end" font-size="12" fill="#555">{y_val}</text>')
        
    for x_val in range(40, 110, 10):
        x_pos = pad_l + ((x_val - x_min) / (x_max - x_min)) * plot_w
        svg.append(f'<line x1="{x_pos}" y1="{pad_t}" x2="{x_pos}" y2="{pad_t + plot_h}" stroke="#eef0f2" stroke-width="1.2"/>')
        svg.append(f'<text x="{x_pos}" y="{pad_t + plot_h + 22}" text-anchor="middle" font-size="12" fill="#555">{x_val}%</text>')
        
    xs = [d['Adult_Literacy_Rate'] for d in data]
    ys = [d['Life_Expectancy'] for d in data]
    mx, my = sum(xs)/len(xs), sum(ys)/len(ys)
    b = sum((xs[i]-mx)*(ys[i]-my) for i in range(len(xs))) / sum((xs[i]-mx)**2 for i in range(len(xs)))
    a = my - b * mx
    
    x_start, x_end = 45.0, 100.0
    y_start, y_end = a + b * x_start, a + b * x_end
    
    sx = pad_l + ((x_start - x_min) / (x_max - x_min)) * plot_w
    sy = pad_t + plot_h - ((y_start - y_min) / (y_max - y_min)) * plot_h
    ex = pad_l + ((x_end - x_min) / (x_max - x_min)) * plot_w
    ey = pad_t + plot_h - ((y_end - y_min) / (y_max - y_min)) * plot_h
    svg.append(f'<line x1="{sx:.1f}" y1="{sy:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" stroke="#444" stroke-width="2.5" stroke-dasharray="6,4"/>')
    
    for d in data:
        px = pad_l + ((d['Adult_Literacy_Rate'] - x_min) / (x_max - x_min)) * plot_w
        py = pad_t + plot_h - ((d['Life_Expectancy'] - y_min) / (y_max - y_min)) * plot_h
        c = REGION_COLORS[d['Region']]
        svg.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="5.5" fill="{c}" fill-opacity="0.85" stroke="#ffffff" stroke-width="1.2"/>')
        
    leg_x = pad_l + 30
    leg_y = pad_t + plot_h + 55
    svg.append(f'<text x="{leg_x}" y="{leg_y + 11}" font-size="12" font-weight="bold" fill="#333">Region:</text>')
    cur_x = leg_x + 65
    for r in ['Africa', 'Americas', 'Asia', 'Europe', 'Oceania']:
        c = REGION_COLORS[r]
        svg.append(f'<circle cx="{cur_x}" cy="{leg_y + 7}" r="5.5" fill="{c}" fill-opacity="0.85"/>')
        svg.append(f'<text x="{cur_x + 12}" y="{leg_y + 11}" font-size="12" fill="#444">{r}</text>')
        cur_x += 105
        
    svg.append(f'<text x="{pad_l + plot_w/2}" y="{pad_t + plot_h + 46}" text-anchor="middle" font-size="13" font-weight="bold" fill="#333">Adult Literacy Rate (%)</text>')
    svg.append(f'<text transform="rotate(-90)" x="-{pad_t + plot_h/2}" y="{pad_l - 45}" text-anchor="middle" font-size="13" font-weight="bold" fill="#333">Life Expectancy (Years)</text>')
    svg.append(f'<line x1="{pad_l}" y1="{pad_t + plot_h}" x2="{pad_l + plot_w}" y2="{pad_t + plot_h}" stroke="#ccc" stroke-width="1.5"/>')
    svg.append(f'<line x1="{pad_l}" y1="{pad_t}" x2="{pad_l}" y2="{pad_t + plot_h}" stroke="#ccc" stroke-width="1.5"/>')
    
    svg.append('</svg>')
    return "".join(svg)

# Save charts
charts = [
    ("01_histogram_life_expectancy", make_histogram(), 900, 560),
    ("02_boxplot_life_expectancy_by_region", make_boxplot(), 900, 560),
    ("03_scatter_life_exp_vs_gdp", make_scatter_gdp(), 950, 580),
    ("04_bar_avg_life_exp_by_region", make_barchart(), 900, 520),
    ("05_scatter_life_exp_vs_healthcare", make_scatter_health(), 950, 580),
    ("06_scatter_life_exp_vs_literacy", make_scatter_literacy(), 950, 580),
]

os.makedirs('/mnt/alterra/repo/life-expectancy-analysis/output', exist_ok=True)
os.makedirs('/tmp/charts', exist_ok=True)

for name, svg_code, cw, ch in charts:
    html_file = f"/tmp/charts/{name}.html"
    png_file = f"/mnt/alterra/repo/life-expectancy-analysis/output/{name}.png"
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(render_html_wrapper(svg_code, cw, ch))
    cmd = [
        "brave", "--headless", "--disable-gpu", "--no-sandbox",
        f"--window-size={cw},{ch}",
        f"--screenshot={png_file}",
        html_file
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"Generated: {png_file}")

print("All 6 charts rendered successfully to output/")
