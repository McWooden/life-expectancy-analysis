# =============================================================================
# Global Life Expectancy and Socioeconomic Factors - Data Analysis
# =============================================================================
# Author : Data Analysis Project
# Date   : October 2026
# Topic  : Analysis of global life expectancy in relation to GDP per capita,
#           healthcare expenditure, and adult literacy rate across 50 countries.
# Source  : Compiled from World Bank Open Data (https://data.worldbank.org)
#           and WHO Global Health Observatory (https://www.who.int/data/gho)
# =============================================================================

# --- 1. Install and Load Required Packages -----------------------------------

# List of required packages
required_packages <- c("readr", "writexl", "ggplot2", "dplyr", "tidyr",
                       "scales", "gridExtra", "knitr")

# Install packages that are not yet installed
new_packages <- required_packages[!(required_packages %in% installed.packages()[, "Package"])]
if (length(new_packages)) {
  install.packages(new_packages, repos = "https://cran.r-project.org")
}

# Load libraries
library(readr)
library(writexl)
library(ggplot2)
library(dplyr)
library(tidyr)
library(scales)
library(gridExtra)

cat("========================================\n")
cat("  GLOBAL LIFE EXPECTANCY ANALYSIS\n")
cat("========================================\n\n")

# --- 2. Read and Inspect the Dataset -----------------------------------------

# Read the CSV dataset
df <- read_csv("data/life_expectancy_data.csv", show_col_types = FALSE)

# Display basic structure
cat("--- Dataset Structure ---\n")
str(df)
cat("\n")

# Display first 10 rows
cat("--- First 10 Rows ---\n")
print(head(df, 10))
cat("\n")

# Check for missing values
cat("--- Missing Values per Column ---\n")
print(colSums(is.na(df)))
cat("\n")

# --- 3. Export Dataset to Excel (.xlsx) ---------------------------------------

write_xlsx(df, "data/life_expectancy_data.xlsx")
cat("Dataset exported to: data/life_expectancy_data.xlsx\n\n")

# --- 4. Descriptive Statistics ------------------------------------------------

cat("=== DESCRIPTIVE STATISTICS ===\n\n")

# Summary of all variables
cat("--- Overall Summary ---\n")
print(summary(df))
cat("\n")

# Detailed statistics for numeric columns
numeric_cols <- c("Life_Expectancy", "GDP_Per_Capita",
                  "Healthcare_Expenditure_Pct", "Population_Millions",
                  "Adult_Literacy_Rate")

cat("--- Detailed Descriptive Statistics ---\n")
desc_stats <- df %>%
  summarise(across(all_of(numeric_cols),
                   list(
                     Mean   = ~round(mean(., na.rm = TRUE), 2),
                     Median = ~round(median(., na.rm = TRUE), 2),
                     SD     = ~round(sd(., na.rm = TRUE), 2),
                     Min    = ~round(min(., na.rm = TRUE), 2),
                     Max    = ~round(max(., na.rm = TRUE), 2)
                   ),
                   .names = "{.col}__{.fn}"))

# Reshape for better readability
desc_long <- desc_stats %>%
  pivot_longer(everything(),
               names_to = c("Variable", "Statistic"),
               names_sep = "__") %>%
  pivot_wider(names_from = Statistic, values_from = value)

print(as.data.frame(desc_long))
cat("\n")

# Summary by Region
cat("--- Average Life Expectancy by Region ---\n")
region_summary <- df %>%
  group_by(Region) %>%
  summarise(
    Count             = n(),
    Avg_Life_Exp      = round(mean(Life_Expectancy, na.rm = TRUE), 1),
    Avg_GDP           = round(mean(GDP_Per_Capita, na.rm = TRUE), 0),
    Avg_Healthcare    = round(mean(Healthcare_Expenditure_Pct, na.rm = TRUE), 1),
    Avg_Literacy      = round(mean(Adult_Literacy_Rate, na.rm = TRUE), 1),
    .groups = "drop"
  ) %>%
  arrange(desc(Avg_Life_Exp))

print(as.data.frame(region_summary))
cat("\n")

# --- 5. Create Output Directory -----------------------------------------------

if (!dir.exists("output")) dir.create("output")

# --- 6. Visualizations --------------------------------------------------------

# Set a consistent theme
theme_analysis <- theme_minimal(base_size = 12) +
  theme(
    plot.title    = element_text(face = "bold", hjust = 0.5, size = 14),
    plot.subtitle = element_text(hjust = 0.5, color = "gray40", size = 10),
    axis.title    = element_text(face = "bold"),
    legend.position = "bottom"
  )

# --- 6a. Histogram: Distribution of Life Expectancy --------------------------

p1 <- ggplot(df, aes(x = Life_Expectancy)) +
  geom_histogram(binwidth = 3, fill = "#3498db", color = "white", alpha = 0.85) +
  geom_vline(aes(xintercept = mean(Life_Expectancy)),
             color = "#e74c3c", linetype = "dashed", linewidth = 1) +
  annotate("text",
           x = mean(df$Life_Expectancy) + 1.5,
           y = Inf, vjust = 2, hjust = 0,
           label = paste("Mean =", round(mean(df$Life_Expectancy), 1)),
           color = "#e74c3c", fontface = "bold", size = 3.5) +
  labs(
    title    = "Distribution of Life Expectancy Across Countries",
    subtitle = "50 Countries Worldwide (2023 Estimates)",
    x        = "Life Expectancy (Years)",
    y        = "Number of Countries"
  ) +
  theme_analysis

ggsave("output/01_histogram_life_expectancy.png", p1,
       width = 8, height = 5, dpi = 300)
cat("Saved: output/01_histogram_life_expectancy.png\n")

# --- 6b. Boxplot: Life Expectancy by Region -----------------------------------

region_order <- df %>%
  group_by(Region) %>%
  summarise(med = median(Life_Expectancy)) %>%
  arrange(med) %>%
  pull(Region)

p2 <- ggplot(df, aes(x = factor(Region, levels = region_order),
                      y = Life_Expectancy, fill = Region)) +
  geom_boxplot(alpha = 0.75, outlier.color = "#e74c3c", outlier.size = 3) +
  geom_jitter(width = 0.15, alpha = 0.4, size = 1.5) +
  scale_fill_brewer(palette = "Set2") +
  labs(
    title    = "Life Expectancy by Region",
    subtitle = "Boxplot showing spread, median, and potential outliers",
    x        = "Region",
    y        = "Life Expectancy (Years)"
  ) +
  theme_analysis +
  theme(legend.position = "none")

ggsave("output/02_boxplot_life_expectancy_by_region.png", p2,
       width = 8, height = 5, dpi = 300)
cat("Saved: output/02_boxplot_life_expectancy_by_region.png\n")

# --- 6c. Scatter Plot: Life Expectancy vs GDP Per Capita ----------------------

p3 <- ggplot(df, aes(x = GDP_Per_Capita, y = Life_Expectancy, color = Region)) +
  geom_point(size = 3, alpha = 0.8) +
  geom_smooth(method = "loess", se = TRUE, color = "gray30",
              linetype = "dashed", linewidth = 0.8, alpha = 0.15) +
  scale_x_continuous(labels = comma) +
  scale_color_brewer(palette = "Set1") +
  labs(
    title    = "Life Expectancy vs. GDP Per Capita",
    subtitle = "Higher GDP tends to be associated with higher life expectancy",
    x        = "GDP Per Capita (USD)",
    y        = "Life Expectancy (Years)",
    color    = "Region"
  ) +
  theme_analysis

ggsave("output/03_scatter_life_exp_vs_gdp.png", p3,
       width = 9, height = 6, dpi = 300)
cat("Saved: output/03_scatter_life_exp_vs_gdp.png\n")

# --- 6d. Bar Chart: Average Life Expectancy by Region -------------------------

p4 <- ggplot(region_summary,
             aes(x = reorder(Region, Avg_Life_Exp), y = Avg_Life_Exp,
                 fill = Region)) +
  geom_col(alpha = 0.85, width = 0.6) +
  geom_text(aes(label = paste0(Avg_Life_Exp, " yrs")),
            hjust = -0.1, fontface = "bold", size = 3.5) +
  scale_fill_brewer(palette = "Set2") +
  coord_flip() +
  ylim(0, 95) +
  labs(
    title    = "Average Life Expectancy by Region",
    subtitle = "Comparison of regional averages (2023 Estimates)",
    x        = "",
    y        = "Average Life Expectancy (Years)"
  ) +
  theme_analysis +
  theme(legend.position = "none")

ggsave("output/04_bar_avg_life_exp_by_region.png", p4,
       width = 8, height = 5, dpi = 300)
cat("Saved: output/04_bar_avg_life_exp_by_region.png\n")

# --- 6e. Scatter Plot: Life Expectancy vs Healthcare Expenditure --------------

p5 <- ggplot(df, aes(x = Healthcare_Expenditure_Pct, y = Life_Expectancy,
                      color = Region)) +
  geom_point(size = 3, alpha = 0.8) +
  geom_smooth(method = "lm", se = TRUE, color = "gray30",
              linetype = "dashed", linewidth = 0.8, alpha = 0.15) +
  scale_color_brewer(palette = "Set1") +
  labs(
    title    = "Life Expectancy vs. Healthcare Expenditure",
    subtitle = "Relationship between health spending and life expectancy",
    x        = "Healthcare Expenditure (% of GDP)",
    y        = "Life Expectancy (Years)",
    color    = "Region"
  ) +
  theme_analysis

ggsave("output/05_scatter_life_exp_vs_healthcare.png", p5,
       width = 9, height = 6, dpi = 300)
cat("Saved: output/05_scatter_life_exp_vs_healthcare.png\n")

# --- 6f. Scatter Plot: Life Expectancy vs Adult Literacy Rate -----------------

p6 <- ggplot(df, aes(x = Adult_Literacy_Rate, y = Life_Expectancy,
                      color = Region)) +
  geom_point(size = 3, alpha = 0.8) +
  geom_smooth(method = "lm", se = TRUE, color = "gray30",
              linetype = "dashed", linewidth = 0.8, alpha = 0.15) +
  scale_color_brewer(palette = "Set1") +
  labs(
    title    = "Life Expectancy vs. Adult Literacy Rate",
    subtitle = "Countries with higher literacy tend to have higher life expectancy",
    x        = "Adult Literacy Rate (%)",
    y        = "Life Expectancy (Years)",
    color    = "Region"
  ) +
  theme_analysis

ggsave("output/06_scatter_life_exp_vs_literacy.png", p6,
       width = 9, height = 6, dpi = 300)
cat("Saved: output/06_scatter_life_exp_vs_literacy.png\n")

# --- 7. Correlation Analysis --------------------------------------------------

cat("\n=== CORRELATION MATRIX (Numeric Variables) ===\n")
cor_matrix <- cor(df[, numeric_cols], use = "complete.obs")
print(round(cor_matrix, 3))
cat("\n")

# --- 8. Key Findings and Interpretation ---------------------------------------

cat("=== KEY FINDINGS ===\n\n")

cat("1. DISTRIBUTION OF LIFE EXPECTANCY:\n")
cat("   - The global average life expectancy across the 50 countries is",
    round(mean(df$Life_Expectancy), 1), "years.\n")
cat("   - Values range from", min(df$Life_Expectancy), "years (",
    df$Country[which.min(df$Life_Expectancy)], ") to",
    max(df$Life_Expectancy), "years (",
    df$Country[which.max(df$Life_Expectancy)], ").\n\n")

cat("2. REGIONAL DIFFERENCES:\n")
cat("   - Europe and Oceania have the highest average life expectancy.\n")
cat("   - Africa has the lowest average, with the widest spread.\n")
cat("   - The boxplot reveals notable variation within each region.\n\n")

cat("3. GDP AND LIFE EXPECTANCY:\n")
cat("   - There is a positive association (r =",
    round(cor(df$Life_Expectancy, df$GDP_Per_Capita), 3), ").\n")
cat("   - The relationship appears logarithmic: gains in life expectancy\n")
cat("     diminish at higher GDP levels.\n\n")

cat("4. HEALTHCARE EXPENDITURE:\n")
cat("   - Positive correlation with life expectancy (r =",
    round(cor(df$Life_Expectancy, df$Healthcare_Expenditure_Pct), 3), ").\n")
cat("   - Countries spending more on healthcare tend to have longer\n")
cat("     life expectancy, though other factors also play a role.\n\n")

cat("5. LITERACY RATE:\n")
cat("   - Strong positive association with life expectancy (r =",
    round(cor(df$Life_Expectancy, df$Adult_Literacy_Rate), 3), ").\n")
cat("   - Education is closely linked to health outcomes.\n\n")

cat("NOTE: These are observational associations. Causal relationships\n")
cat("cannot be established from descriptive analysis alone.\n\n")

cat("========================================\n")
cat("  Analysis Complete. Check output/ for graphs.\n")
cat("========================================\n")
