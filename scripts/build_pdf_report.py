import base64
import os
import subprocess

def img_to_base64(path):
    with open(path, 'rb') as f:
        return f"data:image/png;base64,{base64.b64encode(f.read()).decode('utf-8')}"

img_hist = img_to_base64('/mnt/alterra/repo/life-expectancy-analysis/output/01_histogram_life_expectancy.png')
img_box = img_to_base64('/mnt/alterra/repo/life-expectancy-analysis/output/02_boxplot_life_expectancy_by_region.png')
img_gdp = img_to_base64('/mnt/alterra/repo/life-expectancy-analysis/output/03_scatter_life_exp_vs_gdp.png')
img_bar = img_to_base64('/mnt/alterra/repo/life-expectancy-analysis/output/04_bar_avg_life_exp_by_region.png')
img_health = img_to_base64('/mnt/alterra/repo/life-expectancy-analysis/output/05_scatter_life_exp_vs_healthcare.png')
img_lit = img_to_base64('/mnt/alterra/repo/life-expectancy-analysis/output/06_scatter_life_exp_vs_literacy.png')

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Global Life Expectancy and Socioeconomic Factors - Descriptive Analysis Report</title>
<style>
  @page {{
    size: A4 portrait;
    margin: 14mm 16mm 14mm 16mm;
  }}
  * {{
    box-sizing: border-box;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    color: #2c3e50;
    line-height: 1.45;
    font-size: 9.8pt;
    margin: 0;
    padding: 0;
    background: #ffffff;
  }}
  .page {{
    page-break-after: always;
    position: relative;
    min-height: 269mm;
  }}
  .page:last-child {{
    page-break-after: avoid;
  }}

  /* Typography */
  h1.doc-title {{
    font-size: 19pt;
    font-weight: 800;
    color: #1a365d;
    margin: 0 0 4px 0;
    letter-spacing: -0.5px;
    line-height: 1.2;
  }}
  .doc-subtitle {{
    font-size: 11pt;
    font-weight: 500;
    color: #4a5568;
    margin-bottom: 12px;
  }}
  .meta-box {{
    background: #f7fafc;
    border: 1px solid #e2e8f0;
    border-left: 4px solid #3182ce;
    border-radius: 4px;
    padding: 8px 12px;
    display: flex;
    justify-content: space-between;
    font-size: 8.5pt;
    color: #4a5568;
    margin-bottom: 14px;
  }}
  .meta-box div strong {{
    color: #2d3748;
  }}
  
  h2.sec-title {{
    font-size: 12pt;
    font-weight: 700;
    color: #2b6cb0;
    border-bottom: 1.5px solid #edf2f7;
    padding-bottom: 3px;
    margin: 12px 0 6px 0;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }}
  h3.subsec-title {{
    font-size: 10.2pt;
    font-weight: 700;
    color: #2d3748;
    margin: 8px 0 4px 0;
  }}
  p {{
    margin: 0 0 7px 0;
    text-align: justify;
  }}
  
  /* Tables */
  table.data-table {{
    width: 100%;
    border-collapse: collapse;
    margin: 8px 0 12px 0;
    font-size: 8.5pt;
  }}
  table.data-table th {{
    background: #ebf8ff;
    color: #2b6cb0;
    font-weight: 700;
    text-align: left;
    padding: 6px 8px;
    border-top: 1.5px solid #bee3f8;
    border-bottom: 1.5px solid #bee3f8;
  }}
  table.data-table td {{
    padding: 5px 8px;
    border-bottom: 1px solid #edf2f7;
  }}
  table.data-table tr:nth-child(even) td {{
    background: #f7fafc;
  }}
  .text-right {{
    text-align: right;
  }}
  .text-center {{
    text-align: center;
  }}

  /* Grid layout for figures */
  .fig-row {{
    display: flex;
    gap: 12px;
    margin-bottom: 10px;
    align-items: flex-start;
  }}
  .fig-col {{
    flex: 1;
  }}
  .fig-card {{
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 4px;
    padding: 6px;
    margin-bottom: 4px;
  }}
  .fig-card img {{
    width: 100%;
    height: auto;
    display: block;
    border-radius: 2px;
  }}
  .fig-caption {{
    font-size: 8pt;
    color: #4a5568;
    font-style: italic;
    margin-top: 4px;
    line-height: 1.3;
  }}
  
  .badge {{
    display: inline-block;
    padding: 1px 6px;
    font-size: 7.5pt;
    font-weight: 600;
    border-radius: 3px;
    background: #e2e8f0;
    color: #2d3748;
  }}
  .badge-africa {{ background: #fed7d7; color: #9b2c2c; }}
  .badge-asia {{ background: #feebc8; color: #9c4221; }}
  .badge-americas {{ background: #c3dafe; color: #2c5282; }}
  .badge-europe {{ background: #e9d8fd; color: #553c9a; }}
  .badge-oceania {{ background: #c6f6d5; color: #22543d; }}

  .highlight-box {{
    background: #f0fff4;
    border-left: 3.5px solid #38a169;
    border-radius: 3px;
    padding: 7px 10px;
    margin: 8px 0;
    font-size: 8.8pt;
    color: #22543d;
  }}
  .warning-box {{
    background: #fffaf0;
    border-left: 3.5px solid #dd6b20;
    border-radius: 3px;
    padding: 7px 10px;
    margin: 8px 0;
    font-size: 8.8pt;
    color: #7b341e;
  }}

  .footer-note {{
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    display: flex;
    justify-content: space-between;
    border-top: 1px solid #e2e8f0;
    padding-top: 4px;
    font-size: 7.5pt;
    color: #a0aec0;
  }}
</style>
</head>
<body>

<!-- ==================== PAGE 1 ==================== -->
<div class="page">
  <h1 class="doc-title">Global Life Expectancy & Socioeconomic Factors</h1>
  <div class="doc-subtitle">A Descriptive Cross-National Data Analysis (2023 Estimates)</div>
  
  <div class="meta-box">
    <div><strong>Topic:</strong> Public Health & Global Economics</div>
    <div><strong>Author:</strong> Research & Data Analysis Group</div>
    <div><strong>Sample Size:</strong> 50 Countries (5 Continents)</div>
    <div><strong>Date:</strong> October 2026</div>
  </div>

  <h2 class="sec-title">1. Introduction & Research Objectives</h2>
  <p>
    Life expectancy at birth is one of the most fundamental indicators of national well-being, reflecting population health status, sanitary infrastructure, nutritional availability, and general social progress. While life expectancy has improved substantially over the past half-century, profound disparities remain between different geographic regions and economic classes.
  </p>
  <p>
    The primary objective of this project is to conduct an empirical, descriptive analysis examining cross-country relationships between life expectancy and key socioeconomic drivers: national economic output (GDP per capita), public healthcare financing (% of GDP allocated to health), and human capital development (adult literacy rate). This study analyzes a standardized dataset of 50 nations to identify baseline distribution shapes, detect outlier clusters, and assess bivariate associations.
  </p>

  <h2 class="sec-title">2. Data Provenance & Structure</h2>
  <p>
    Data were compiled and curated from official, publicly accessible multilateral research repositories:
  </p>
  <ul style="margin: 0 0 8px 20px; padding: 0; font-size: 9pt;">
    <li><strong>World Bank Open Data</strong> (<code>data.worldbank.org</code>): GDP Per Capita (current USD), Total Population (millions), and Adult Literacy Rate (% of population aged 15 and above).</li>
    <li><strong>World Health Organization (WHO) Global Health Observatory</strong> (<code>who.int/data/gho</code>): Life Expectancy at birth (years) and Healthcare Expenditure (% of national GDP).</li>
  </ul>
  <p>
    The structured dataset contains 50 complete observations across 7 standardized columns, containing zero missing values (NA count = 0), verified for immediate execution in RStudio via the companion <code>analysis.R</code> script and the delivered Excel workbook <code>life_expectancy_data.xlsx</code>.
  </p>

  <h2 class="sec-title">3. Comprehensive Descriptive Statistics</h2>
  <p>
    Parametric and non-parametric summary measures were computed across all numeric indicators.
  </p>

  <table class="data-table">
    <thead>
      <tr>
        <th>Variable</th>
        <th>Unit</th>
        <th class="text-right">Mean</th>
        <th class="text-right">Std. Dev</th>
        <th class="text-right">Median</th>
        <th class="text-right">Min</th>
        <th class="text-right">Max</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Life Expectancy</strong></td>
        <td>Years</td>
        <td class="text-right">74.88</td>
        <td class="text-right">7.58</td>
        <td class="text-right">76.60</td>
        <td class="text-right">54.30</td>
        <td class="text-right">84.80</td>
      </tr>
      <tr>
        <td><strong>GDP Per Capita</strong></td>
        <td>USD ($)</td>
        <td class="text-right">24,354</td>
        <td class="text-right">26,058</td>
        <td class="text-right">12,426</td>
        <td class="text-right">492</td>
        <td class="text-right">93,457</td>
      </tr>
      <tr>
        <td><strong>Healthcare Expenditure</strong></td>
        <td>% of GDP</td>
        <td class="text-right">7.10</td>
        <td class="text-right">3.20</td>
        <td class="text-right">6.50</td>
        <td class="text-right">2.50</td>
        <td class="text-right">16.60</td>
      </tr>
      <tr>
        <td><strong>Adult Literacy Rate</strong></td>
        <td>%</td>
        <td class="text-right">86.64</td>
        <td class="text-right">16.32</td>
        <td class="text-right">95.90</td>
        <td class="text-right">47.10</td>
        <td class="text-right">99.80</td>
      </tr>
      <tr>
        <td><strong>Population</strong></td>
        <td>Millions</td>
        <td class="text-right">126.96</td>
        <td class="text-right">312.44</td>
        <td class="text-right">43.80</td>
        <td class="text-right">5.20</td>
        <td class="text-right">1,428.60</td>
      </tr>
    </tbody>
  </table>

  <h3 class="subsec-title">Regional Disaggregation Overview</h3>
  <table class="data-table">
    <thead>
      <tr>
        <th>Region</th>
        <th class="text-center">Count</th>
        <th class="text-right">Avg Life Exp</th>
        <th class="text-right">Avg GDP/Capita</th>
        <th class="text-right">Avg Health Exp (%)</th>
        <th class="text-right">Avg Literacy (%)</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><span class="badge badge-oceania">Oceania</span></td>
        <td class="text-center">2</td>
        <td class="text-right">82.7 yrs</td>
        <td class="text-right">$56,370</td>
        <td class="text-right">9.6%</td>
        <td class="text-right">99.0%</td>
      </tr>
      <tr>
        <td><span class="badge badge-europe">Europe</span></td>
        <td class="text-center">12</td>
        <td class="text-right">80.6 yrs</td>
        <td class="text-right">$47,381</td>
        <td class="text-right">9.2%</td>
        <td class="text-right">99.0%</td>
      </tr>
      <tr>
        <td><span class="badge badge-americas">Americas</span></td>
        <td class="text-center">10</td>
        <td class="text-right">77.5 yrs</td>
        <td class="text-right">$20,691</td>
        <td class="text-right">9.3%</td>
        <td class="text-right">95.6%</td>
      </tr>
      <tr>
        <td><span class="badge badge-asia">Asia</span></td>
        <td class="text-center">14</td>
        <td class="text-right">75.9 yrs</td>
        <td class="text-right">$12,298</td>
        <td class="text-right">5.1%</td>
        <td class="text-right">88.8%</td>
      </tr>
      <tr>
        <td><span class="badge badge-africa">Africa</span></td>
        <td class="text-center">12</td>
        <td class="text-right">64.4 yrs</td>
        <td class="text-right">$2,266</td>
        <td class="text-right">4.5%</td>
        <td class="text-right">68.0%</td>
      </tr>
    </tbody>
  </table>

  <div class="footer-note">
    <span>Global Life Expectancy & Socioeconomic Analysis | Technical Report</span>
    <span>Page 1 of 3</span>
  </div>
</div>

<!-- ==================== PAGE 2 ==================== -->
<div class="page">
  <h2 class="sec-title">4. Distributional Characteristics & Regional Disparities</h2>
  
  <p>
    An examination of numeric distribution properties reveals substantial skewness in global health outcomes. Figures 1 through 3 illustrate the global frequency distribution, dispersion patterns across geographic blocs, and rank comparisons of continental averages.
  </p>

  <div class="fig-row">
    <div class="fig-col">
      <div class="fig-card">
        <img src="{img_hist}" alt="Histogram of Life Expectancy">
      </div>
      <div class="fig-caption"><strong>Figure 1:</strong> Histogram of life expectancy (binwidth = 3 years). The dashed vertical line denotes the grand mean of 74.9 years. Notice the left skew with a prolonged tail.</div>
    </div>
    <div class="fig-col">
      <div class="fig-card">
        <img src="{img_box}" alt="Boxplot by Region">
      </div>
      <div class="fig-caption"><strong>Figure 2:</strong> Boxplot displaying median, interquartile range (IQR), and spread across regions. Jittered points display raw observations within each continental grouping.</div>
    </div>
  </div>

  <h3 class="subsec-title">Distributional Properties & Outlier Diagnostics</h3>
  <p>
    As visualized in <strong>Figure 1</strong>, global life expectancy exhibits pronounced left-skewness. A high concentration of countries clusters in the 75–84 year range (mode at 81–84 years). The lower tail extends down to 54.3 years (Nigeria) and 59.3 years (Mozambique), creating a 30.5-year gap between the highest and lowest countries in the sample. The sample median (76.6 years) sits notably above the sample mean (74.88 years), a classic property of negatively skewed public health data where a minority of distressed nations pull down the arithmetic average.
  </p>
  <p>
    The regional boxplot in <strong>Figure 2</strong> reveals sharp geographical stratifications:
  </p>
  <ul style="margin: 0 0 8px 20px; padding: 0; font-size: 8.9pt;">
    <li><strong>Europe & Oceania:</strong> Demonstrate high medians (&gt;82 years) and remarkably tight interquartile spreads, indicative of universally mature healthcare systems and consistent socioeconomic safety nets.</li>
    <li><strong>Americas:</strong> Median life expectancy reaches 77.0 years. The United States exhibits high life expectancy (79.1 years) but is paired with unprecedented healthcare spending (16.6% of GDP), behaving as an expenditure outlier.</li>
    <li><strong>Asia:</strong> Exhibits the broadest intra-regional variance, ranging from highly developed societies (Japan at 84.8 years, South Korea at 83.7 years) down to emerging economies (Pakistan at 66.1 years).</li>
    <li><strong>Africa:</strong> Records both the lowest regional median (63.4 years) and the highest internal dispersion (standard deviation = 5.56 years), with northern states (Morocco at 74.0 yrs) performing substantially above sub-Saharan nations.</li>
  </ul>

  <div class="fig-row" style="margin-top: 6px;">
    <div class="fig-col" style="flex: 0 0 52%;">
      <div class="fig-card">
        <img src="{img_bar}" alt="Regional Averages Bar Chart">
      </div>
      <div class="fig-caption"><strong>Figure 3:</strong> Horizontal bar chart of regional mean life expectancies. A distinct 18.3-year gap separates Oceania from Africa.</div>
    </div>
    <div class="fig-col" style="flex: 0 0 48%; padding-left: 6px;">
      <h3 class="subsec-title" style="margin-top: 0;">Regional Gap Summary</h3>
      <p style="font-size: 8.8pt;">
        <strong>Figure 3</strong> summarizes the stark continental divide: European (80.6 yrs) and Oceanian (82.7 yrs) citizens live on average 16 to 18 years longer than citizens in African nations (64.4 yrs). 
      </p>
      <div class="highlight-box">
        <strong>Key Observation:</strong> The regional difference is strongly paired with economic resources: the average European GDP/capita ($47,381) in the sample is more than 20 times greater than that of the sampled African nations ($2,266).
      </div>
    </div>
  </div>

  <div class="footer-note">
    <span>Global Life Expectancy & Socioeconomic Analysis | Technical Report</span>
    <span>Page 2 of 3</span>
  </div>
</div>

<!-- ==================== PAGE 3 ==================== -->
<div class="page">
  <h2 class="sec-title">5. Socioeconomic Associations & Correlation Analysis</h2>
  <p>
    Bivariate relationships were evaluated between life expectancy and economic prosperity, healthcare expenditure, and adult literacy. All three factors show positive, statistically robust associations.
  </p>

  <div class="fig-row">
    <div class="fig-col">
      <div class="fig-card">
        <img src="{img_gdp}" alt="Life Exp vs GDP Per Capita">
      </div>
      <div class="fig-caption"><strong>Figure 4:</strong> Scatter plot of Life Expectancy vs. GDP Per Capita with logarithmic trend curve (r = 0.694). Diminishing returns appear above $30,000.</div>
    </div>
    <div class="fig-col">
      <div class="fig-card">
        <img src="{img_health}" alt="Life Exp vs Healthcare Expenditure">
      </div>
      <div class="fig-caption"><strong>Figure 5:</strong> Life Expectancy vs. Healthcare Expenditure as % of GDP with linear fit (r = 0.661). Higher spending aligns with longer life.</div>
    </div>
  </div>

  <div class="fig-row">
    <div class="fig-col" style="flex: 0 0 50%;">
      <div class="fig-card">
        <img src="{img_lit}" alt="Life Exp vs Literacy Rate">
      </div>
      <div class="fig-caption"><strong>Figure 6:</strong> Life Expectancy vs. Adult Literacy Rate with linear fit (r = 0.785). Strongest single linear bivariate predictor in the dataset.</div>
    </div>
    <div class="fig-col" style="flex: 0 0 50%; padding-left: 6px;">
      <h3 class="subsec-title" style="margin-top: 0;">Comparative Correlation Matrix</h3>
      <table class="data-table" style="font-size: 8.2pt; margin-top: 2px;">
        <thead>
          <tr>
            <th>Indicator Pair</th>
            <th class="text-center">Pearson r</th>
            <th>Relationship Strength</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Life Exp vs. Adult Literacy</td>
            <td class="text-center"><strong>+0.785</strong></td>
            <td>Strong positive</td>
          </tr>
          <tr>
            <td>Life Exp vs. GDP Per Capita</td>
            <td class="text-center"><strong>+0.694</strong></td>
            <td>Moderate-to-strong non-linear</td>
          </tr>
          <tr>
            <td>Life Exp vs. Healthcare Exp %</td>
            <td class="text-center"><strong>+0.661</strong></td>
            <td>Moderate positive</td>
          </tr>
        </tbody>
      </table>
      <p style="font-size: 8.5pt;">
        <strong>The Preston Curve Effect:</strong> In <strong>Figure 4</strong>, the relationship with GDP per capita is distinctly concave. At early development stages (GDP &lt; $10,000), marginal economic increases correspond to steep gains in lifespan. Beyond $35,000, longevity plateaus between 81 and 85 years.
      </p>
    </div>
  </div>

  <h2 class="sec-title">6. Discussion & Methodological Scope</h2>
  <p>
    The findings corroborate established developmental economics: basic income, sanitary infrastructure, and general literacy constitute essential foundations for maternal health and infectious disease containment. Literacy (r = 0.785) shows the highest direct linear correlation with longevity, reflecting how maternal education and health literacy directly influence community survival.
  </p>

  <div class="warning-box">
    <strong>Methodological Scope & Causal Disclaimer:</strong> This study is strictly descriptive and cross-sectional. The observed positive correlations (r = 0.66 to 0.79) do not establish causal relationships. Confounding factors—such as institutional quality, environmental conditions, and peacetime stability—simultaneously influence both economic metrics and health outcomes.
  </div>

  <h2 class="sec-title">7. Conclusions</h2>
  <ul style="margin: 0 0 6px 18px; padding: 0; font-size: 8.8pt;">
    <li><strong>Socioeconomic Underpinnings:</strong> Life expectancy is tightly bound to national economic capacity and human development, with literacy rate being the strongest linear covariate.</li>
    <li><strong>Non-Linear Economic Returns:</strong> Wealth yields massive life gains in developing nations, but exhibits diminishing marginal returns in high-income states.</li>
    <li><strong>Closing the Global Gap:</strong> Addressing the 18.3-year lifespan disparity between Africa and advanced economies requires integrated investments in both public healthcare capacity and foundational education.</li>
  </ul>

  <div class="footer-note">
    <span>Global Life Expectancy & Socioeconomic Analysis | Technical Report</span>
    <span>Page 3 of 3</span>
  </div>
</div>

</body>
</html>
"""

report_html_path = '/mnt/alterra/repo/life-expectancy-analysis/report.html'
report_pdf_path = '/mnt/alterra/repo/life-expectancy-analysis/report.pdf'

with open(report_html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Wrote report HTML to: {report_html_path}")

cmd = [
    "brave", "--headless", "--disable-gpu", "--no-sandbox",
    "--print-to-pdf-no-header",
    f"--print-to-pdf={report_pdf_path}",
    report_html_path
]

res = subprocess.run(cmd, capture_output=True, text=True)
print("Brave PDF Output:", res.stdout, res.stderr)
print(f"Generated PDF at: {report_pdf_path}")
