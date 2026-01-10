# Amazon UK Product Dataset — Bivariate EDA Report

## Part 1 — Best-seller trends across categories

### Crosstab insights
We created a crosstab between `category` and `isBestSeller` and computed the best-seller rate per category.

Top categories by best-seller rate (note: very small categories can appear here):

- **Grocery**: best-seller rate=5.81%, n=9,564
- **Smart Home Security & Lighting**: best-seller rate=5.77%, n=104
- **Health & Personal Care**: best-seller rate=5.77%, n=9,569
- **Mobile Phone Accessories**: best-seller rate=4.25%, n=259
- **Power & Hand Tools**: best-seller rate=3.53%, n=8,659
- **Billiard, Snooker & Pool**: best-seller rate=3.21%, n=249
- **Pet Supplies**: best-seller rate=3.02%, n=9,437
- **Home Brewing & Wine Making**: best-seller rate=2.85%, n=246
- **Wind Instruments**: best-seller rate=2.80%, n=250
- **Mirrors**: best-seller rate=2.80%, n=250

### Statistical tests
- Chi-square test: chi2=36540.20, dof=295, p-value=0
- Cramér’s V: 0.1223

Interpretation guidance:
- If p-value < 0.05, category and best-seller status are not independent.
- Cramér’s V ~0.1 small, ~0.3 medium, ~0.5 large association (rule of thumb).

Chart: `plots_bivariate/stacked_bar_best_seller_top20.png`

## Part 2 — Prices and ratings across categories (outliers removed with IQR)

Outlier bounds for price using IQR: lower=-44.01, upper=99.99

- Highest **median** price category (overall): **Desktop PCs** (median=74.00)
- Highest **average** price category (overall): **Motherboards** (mean=68.77)
- Highest **median** rating category (overall): **Computer Memory** (median=4.70)

Charts:
- `plots_bivariate/violin_price_top20_no_outliers.png`
- `plots_bivariate/bar_avg_price_top10_no_outliers.png`
- `plots_bivariate/box_stars_top10_no_outliers.png`

## Part 3 — Relationship between price and stars

- Pearson correlation (price vs stars, outliers removed): **-0.0777**

Charts:
- `plots_bivariate/scatter_price_vs_stars_no_outliers.png`
- `plots_bivariate/heatmap_correlations_no_outliers.png`
- `plots_bivariate/qqplot_price_no_outliers.png`

## Bonus — Without removing outliers

- Pearson correlation (price vs stars, with outliers): **-0.1249**
Insight:
- Outliers often distort plots and can change correlations.
- QQ plots with outliers typically show stronger deviation from normality.

Chart: `plots_bivariate/qqplot_price_with_outliers.png`
