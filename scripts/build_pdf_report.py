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
<title>Global Life Expectancy & Socioeconomic Factors - Research Report</title>
<style>
  @page {{
    size: A4 portrait;
    margin: 16mm 18mm 16mm 18mm;
  }}
  * {{
    box-sizing: border-box;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    color: #242424;
    line-height: 1.5;
    font-size: 9.6pt;
    margin: 0;
    padding: 0;
    background: #ffffff;
  }}
  .page {{
    page-break-after: always;
    position: relative;
    min-height: 265mm;
  }}
  .page:last-child {{
    page-break-after: avoid;
  }}

  /* Medium-style Editorial Typography */
  h1.doc-title {{
    font-family: Georgia, Cambria, "Times New Roman", Times, serif;
    font-size: 22pt;
    font-weight: 700;
    color: #111111;
    margin: 0 0 6px 0;
    letter-spacing: -0.6px;
    line-height: 1.22;
  }}
  .doc-subtitle {{
    font-size: 11pt;
    color: #6b6b6b;
    margin-bottom: 12px;
    font-weight: 400;
    line-height: 1.4;
  }}
  .meta-line {{
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 8.5pt;
    color: #757575;
    border-bottom: 1px solid #e5e5e5;
    padding-bottom: 10px;
    margin-bottom: 16px;
  }}
  .meta-dot {{
    color: #b0b0b0;
  }}
  
  h2.sec-title {{
    font-family: Georgia, Cambria, "Times New Roman", Times, serif;
    font-size: 12.5pt;
    font-weight: 700;
    color: #111111;
    margin: 14px 0 6px 0;
    letter-spacing: -0.2px;
  }}
  h3.subsec-title {{
    font-size: 9.8pt;
    font-weight: 600;
    color: #242424;
    margin: 10px 0 4px 0;
  }}
  p {{
    margin: 0 0 8px 0;
    text-align: justify;
    color: #292929;
  }}
  
  /* Classic Academic Booktabs Table (Neutral, No AI Pastel Colors) */
  table.booktabs {{
    width: 100%;
    border-collapse: collapse;
    margin: 8px 0 12px 0;
    font-size: 8.5pt;
    border-top: 1.5px solid #111111;
    border-bottom: 1.5px solid #111111;
  }}
  table.booktabs th {{
    font-weight: 600;
    color: #111111;
    text-align: left;
    padding: 6px 8px;
    border-bottom: 1px solid #111111;
    background: transparent;
  }}
  table.booktabs td {{
    padding: 5px 8px;
    border-bottom: 1px solid #eeeeee;
    color: #242424;
  }}
  table.booktabs tr:last-child td {{
    border-bottom: none;
  }}
  .text-right {{
    text-align: right;
  }}
  .text-center {{
    text-align: center;
  }}

  /* Minimalist Figures */
  .fig-row {{
    display: flex;
    gap: 14px;
    margin-bottom: 10px;
    align-items: flex-start;
  }}
  .fig-col {{
    flex: 1;
  }}
  .fig-card {{
    background: #ffffff;
    border: 1px solid #e8e8e8;
    border-radius: 2px;
    padding: 5px;
    margin-bottom: 3px;
  }}
  .fig-card img {{
    width: 100%;
    height: auto;
    display: block;
  }}
  .fig-caption {{
    font-size: 8pt;
    color: #666666;
    margin-top: 4px;
    line-height: 1.35;
  }}
  .fig-caption strong {{
    color: #222222;
  }}

  /* Editorial Blockquote (Neutral, Clean) */
  blockquote.editorial-note {{
    margin: 8px 0;
    padding: 6px 12px;
    border-left: 2.5px solid #242424;
    background: #fafafa;
    color: #383838;
    font-size: 8.8pt;
    line-height: 1.45;
  }}
  blockquote.editorial-note strong {{
    color: #111111;
  }}

  .footer-note {{
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    display: flex;
    justify-content: space-between;
    border-top: 1px solid #eeeeee;
    padding-top: 4px;
    font-size: 7.5pt;
    color: #8c8c8c;
  }}
</style>
</head>
<body>

<!-- ==================== PAGE 1 ==================== -->
<div class="page">
  <h1 class="doc-title">Global Life Expectancy & Socioeconomic Factors</h1>
  <div class="doc-subtitle">A Cross-National Descriptive Analysis Across 50 Countries</div>
  
  <div class="meta-line">
    <span><strong>Author:</strong> Research & Data Analysis Group</span>
    <span class="meta-dot">·</span>
    <span><strong>Data Sources:</strong> World Bank & WHO (2023 Estimates)</span>
    <span class="meta-dot">·</span>
    <span><strong>Date:</strong> October 2026</span>
    <span class="meta-dot">·</span>
    <span><strong>Sample:</strong> 50 Nations (5 Continents)</span>
  </div>

  <h2 class="sec-title">1. Introduction & Research Objectives</h2>
  <p>
    Life expectancy at birth serves as a foundational benchmark for measuring national living standards, sanitary conditions, and public healthcare capacity. Over the past half-century, global longevity has improved considerably; however, substantial disparities persist between developing and advanced economies.
  </p>
  <p>
    This report provides a descriptive analysis examining how national life expectancy relates to three key socioeconomic variables: national economic output (GDP per capita in USD), public health spending (% of GDP allocated to healthcare), and foundational human capital (adult literacy rate). The objective is to identify distribution patterns, assess continental disparities, and evaluate bivariate associations without assuming direct causality.
  </p>

  <h2 class="sec-title">2. Data Provenance & Structure</h2>
  <p>
    The dataset was compiled from official, publicly accessible multilateral databases:
  </p>
  <ul style="margin: 0 0 8px 18px; padding: 0; font-size: 9pt; color: #333;">
    <li><strong>World Bank Open Data</strong> (<code>data.worldbank.org</code>): GDP Per Capita (current USD), Total Population (millions), and Adult Literacy Rate (% of population aged 15 and above).</li>
    <li><strong>World Health Organization (WHO) Global Health Observatory</strong> (<code>who.int/data/gho</code>): Life Expectancy at birth (years) and Healthcare Expenditure (% of national GDP).</li>
  </ul>
  <p>
    The sample consists of 50 countries across five continental regions (Africa, Americas, Asia, Europe, and Oceania). The data were screened for consistency, containing zero missing entries, and formatted for straightforward replication in RStudio via the delivered R script and Excel workbook.
  </p>

  <h2 class="sec-title">3. Descriptive Summary Statistics</h2>
  <p>
    Summary measures across all numeric variables in the sample are presented in Table 1, followed by regional aggregate comparisons in Table 2.
  </p>

  <table class="booktabs">
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

  <h3 class="subsec-title">Table 2: Regional Disaggregation</h3>
  <table class="booktabs">
    <thead>
      <tr>
        <th>Region</th>
        <th class="text-center">Count</th>
        <th class="text-right">Mean Life Exp</th>
        <th class="text-right">Mean GDP/Capita</th>
        <th class="text-right">Mean Health Exp (%)</th>
        <th class="text-right">Mean Literacy (%)</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Oceania</td>
        <td class="text-center">2</td>
        <td class="text-right">82.7 yrs</td>
        <td class="text-right">$56,370</td>
        <td class="text-right">9.6%</td>
        <td class="text-right">99.0%</td>
      </tr>
      <tr>
        <td>Europe</td>
        <td class="text-center">12</td>
        <td class="text-right">80.6 yrs</td>
        <td class="text-right">$47,381</td>
        <td class="text-right">9.2%</td>
        <td class="text-right">99.0%</td>
      </tr>
      <tr>
        <td>Americas</td>
        <td class="text-center">10</td>
        <td class="text-right">77.5 yrs</td>
        <td class="text-right">$20,691</td>
        <td class="text-right">9.3%</td>
        <td class="text-right">95.6%</td>
      </tr>
      <tr>
        <td>Asia</td>
        <td class="text-center">14</td>
        <td class="text-right">75.9 yrs</td>
        <td class="text-right">$12,298</td>
        <td class="text-right">5.1%</td>
        <td class="text-right">88.8%</td>
      </tr>
      <tr>
        <td>Africa</td>
        <td class="text-center">12</td>
        <td class="text-right">64.4 yrs</td>
        <td class="text-right">$2,266</td>
        <td class="text-right">4.5%</td>
        <td class="text-right">68.0%</td>
      </tr>
    </tbody>
  </table>

  <div class="footer-note">
    <span>Global Life Expectancy & Socioeconomic Factors | Research Report</span>
    <span>Page 1 of 3</span>
  </div>
</div>

<!-- ==================== PAGE 2 ==================== -->
<div class="page">
  <h2 class="sec-title">4. Distributional Characteristics & Regional Disparities</h2>
  
  <p>
    An evaluation of numeric distributions reveals negative skewness in global health outcomes, accompanied by defined continental groupings. Figures 1 through 3 display the global frequency distribution, regional dispersion, and comparative averages.
  </p>

  <div class="fig-row">
    <div class="fig-col">
      <div class="fig-card">
        <img src="{img_hist}" alt="Histogram of Life Expectancy">
      </div>
      <div class="fig-caption"><strong>Figure 1.</strong> Frequency distribution of life expectancy across 50 countries (binwidth = 3 years). The dashed vertical line marks the sample mean of 74.9 years.</div>
    </div>
    <div class="fig-col">
      <div class="fig-card">
        <img src="{img_box}" alt="Boxplot by Region">
      </div>
      <div class="fig-caption"><strong>Figure 2.</strong> Boxplot showing median, interquartile range (IQR), and spread across regions. Individual points depict country observations.</div>
    </div>
  </div>

  <h3 class="subsec-title">Distribution Properties & Outlier Diagnostics</h3>
  <p>
    As illustrated in <strong>Figure 1</strong>, the distribution of global life expectancy is left-skewed. The majority of countries cluster in the 75–84 year bracket, with the modal frequency occurring between 81 and 84 years. At the lower tail, several nations record life expectancies below 62 years (Nigeria at 54.3 years and Mozambique at 59.3 years), establishing a 30.5-year span across the sample. Because of this lower tail, the median (76.6 years) sits 1.7 years above the arithmetic mean (74.88 years).
  </p>
  <p>
    The regional boxplot in <strong>Figure 2</strong> highlights clear geographic clustering:
  </p>
  <ul style="margin: 0 0 8px 18px; padding: 0; font-size: 8.9pt; color: #333;">
    <li><strong>Europe & Oceania:</strong> Characterized by high medians (&gt;82 years) and narrow interquartile ranges, reflecting mature public health systems and consistent universal service delivery.</li>
    <li><strong>Americas:</strong> Median life expectancy reaches 77.0 years. While the United States records high longevity (79.1 years), its health spending (16.6% of GDP) stands as a distinct expenditure outlier.</li>
    <li><strong>Asia:</strong> Demonstrates substantial internal diversity, spanning high-income societies (Japan at 84.8 years, South Korea at 83.7 years) down to emerging economies (Pakistan at 66.1 years).</li>
    <li><strong>Africa:</strong> Records the lowest median (63.4 years) and widest dispersion (SD = 5.56 years), with northern states (Morocco at 74.0 years) substantially outpacing sub-Saharan nations.</li>
  </ul>

  <div class="fig-row" style="margin-top: 6px;">
    <div class="fig-col" style="flex: 0 0 52%;">
      <div class="fig-card">
        <img src="{img_bar}" alt="Regional Averages Bar Chart">
      </div>
      <div class="fig-caption"><strong>Figure 3.</strong> Horizontal bar chart of regional mean life expectancies. A gap of 18.3 years separates Oceania from Africa.</div>
    </div>
    <div class="fig-col" style="flex: 0 0 48%; padding-left: 6px;">
      <h3 class="subsec-title" style="margin-top: 0;">Summary of Regional Disparities</h3>
      <p style="font-size: 8.8pt;">
        <strong>Figure 3</strong> summarizes the continental division: citizens in European and Oceanian countries live on average 16 to 18 years longer than those in African nations.
      </p>
      <blockquote class="editorial-note">
        <strong>Observation:</strong> This lifespan disparity directly parallels economic differences: the mean European GDP per capita ($47,381) in the sample is roughly twenty times higher than that of the sampled African nations ($2,266).
      </blockquote>
    </div>
  </div>

  <div class="footer-note">
    <span>Global Life Expectancy & Socioeconomic Factors | Research Report</span>
    <span>Page 2 of 3</span>
  </div>
</div>

<!-- ==================== PAGE 3 ==================== -->
<div class="page">
  <h2 class="sec-title">5. Socioeconomic Associations & Correlation Analysis</h2>
  <p>
    Bivariate relationships were evaluated between life expectancy and economic prosperity, healthcare expenditure, and adult literacy rate. All three factors show positive, statistically notable correlations.
  </p>

  <div class="fig-row">
    <div class="fig-col">
      <div class="fig-card">
        <img src="{img_gdp}" alt="Life Exp vs GDP Per Capita">
      </div>
      <div class="fig-caption"><strong>Figure 4.</strong> Life Expectancy vs. GDP Per Capita with logarithmic trend line (r = +0.694). Gains diminish notably above $30,000.</div>
    </div>
    <div class="fig-col">
      <div class="fig-card">
        <img src="{img_health}" alt="Life Exp vs Healthcare Expenditure">
      </div>
      <div class="fig-caption"><strong>Figure 5.</strong> Life Expectancy vs. Healthcare Expenditure as % of GDP with linear fit (r = +0.661). Higher spending aligns with longer life.</div>
    </div>
  </div>

  <div class="fig-row">
    <div class="fig-col" style="flex: 0 0 50%;">
      <div class="fig-card">
        <img src="{img_lit}" alt="Life Exp vs Literacy Rate">
      </div>
      <div class="fig-caption"><strong>Figure 6.</strong> Life Expectancy vs. Adult Literacy Rate with linear fit (r = +0.785). Strongest single linear bivariate relationship.</div>
    </div>
    <div class="fig-col" style="flex: 0 0 50%; padding-left: 6px;">
      <h3 class="subsec-title" style="margin-top: 0;">Correlation Summary</h3>
      <table class="booktabs" style="font-size: 8.2pt; margin-top: 2px;">
        <thead>
          <tr>
            <th>Indicator Pair</th>
            <th class="text-center">Pearson r</th>
            <th>Relationship Type</th>
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
        <strong>The Preston Curve Effect:</strong> In <strong>Figure 4</strong>, the association with GDP per capita is non-linear and concave. At lower income levels (GDP &lt; $10,000), marginal increases in economic output correlate with steep life expectancy gains. Beyond $35,000, returns diminish, and life expectancy plateaus between 81 and 85 years.
      </p>
    </div>
  </div>

  <h2 class="sec-title">6. Discussion & Methodological Scope</h2>
  <p>
    These observations align with established literature in developmental economics: foundational income, sanitation infrastructure, and basic education are critical prerequisites for maternal health and infectious disease reduction. Adult literacy (r = +0.785) exhibits the strongest linear association, suggesting that educational attainment strongly reinforces health awareness and preventative behaviors.
  </p>

  <blockquote class="editorial-note">
    <strong>Methodological Scope & Causal Disclaimer:</strong> This study is strictly descriptive and cross-sectional. The observed correlations (r = +0.66 to +0.79) do not establish causal relationships. Confounding variables—such as governance quality, geographical factors, and peacetime stability—simultaneously influence both economic metrics and health outcomes.
  </blockquote>

  <h2 class="sec-title">7. Conclusions</h2>
  <ul style="margin: 0 0 6px 18px; padding: 0; font-size: 8.8pt; color: #333;">
    <li><strong>Socioeconomic Foundations:</strong> Longevity is closely tied to national economic capacity and foundational education, with literacy rate showing the strongest linear association.</li>
    <li><strong>Diminishing Economic Returns:</strong> Wealth improvements yield the largest life expectancy gains at lower income thresholds, with plateauing effects observed in high-income economies.</li>
    <li><strong>Addressing Disparities:</strong> Narrowing the 18.3-year lifespan gap between lower-income regions and developed nations requires coordinated investments in both healthcare capacity and general education.</li>
  </ul>

  <div class="footer-note">
    <span>Global Life Expectancy & Socioeconomic Factors | Research Report</span>
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

print(f"Wrote humanized report HTML to: {report_html_path}")

cmd = [
    "brave", "--headless", "--disable-gpu", "--no-sandbox",
    "--print-to-pdf-no-header",
    f"--print-to-pdf={report_pdf_path}",
    report_html_path
]

res = subprocess.run(cmd, capture_output=True, text=True)
print("Brave PDF Output:", res.stdout, res.stderr)
print(f"Generated humanized PDF at: {report_pdf_path}")
