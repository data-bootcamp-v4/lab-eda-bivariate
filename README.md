## Lab - EDA Bivariate Analysis: Diving into Amazon UK Product Insights Part II

**Objective**: Delve into the dynamics of product pricing on Amazon UK to uncover insights that can inform business strategies and decision-making.

**Dataset**: This lab utilizes the [Amazon UK product dataset](https://www.kaggle.com/datasets/asaniczka/uk-optimal-product-price-prediction/)
which provides information on product categories, brands, prices, ratings, and more from from Amazon UK. You'll need to download it to start working with it.

---

### Part 1: Analyzing Best-Seller Trends Across Product Categories

**Objective**: Understand the relationship between product categories and their best-seller status.

1. **Crosstab Analysis**:
    - Create a crosstab between the product `category` and the `isBestSeller` status.
    Best-sellers are rare overall: only 7,980 of 2,443,651 listings (0.33%) carry the isBestSeller flag. That baseline matters — any category well above 0.33% is meaningfully over-indexed.
    - Are there categories where being a best-seller is more prevalent? 
    	
    	*Hint: one option is to calculate the proportion of best-sellers for each category and then sort the categories based on this proportion in descending order.*
    Yes, best-seller prevalence varies a lot by category. Grocery and Health & Personal Care both sit at ~5.8% — nearly 18x the overall rate. Meanwhile, 36 of the 296 categories (12%) have zero best-sellers at all. Best-seller status is clearly not evenly distributed across the catalogue — it concentrates in consumable/repeat-purchase categories (groceries, health items, pet supplies) more than one-off purchase categories.


2. **Statistical Tests**:
    - Conduct a Chi-square test to determine if the best-seller distribution is independent of the product category.
    Chi-square: the p-value is essentially zero, so we reject the null hypothesis of independence — best-seller status is statistically significantly associated with category. With 2.4M rows, though, almost any non-zero association will hit statistical significance, so the p-value alone doesn't tell you whether the relationship is practically meaningful.
    - Compute Cramér's V to understand the strength of association between best-seller status and category.
    Cramér's V (0.122): this is where practical significance comes in — 0.122 indicates a weak association (V ranges 0–1; under ~0.1 is negligible, ~0.1–0.3 is weak, ~0.3–0.5 moderate). So while category and best-seller status aren't independent, category alone explains only a small part of what makes a product a best-seller — other factors (price, reviews, rating, demand) are likely doing more of the work.

3. **Visualizations**:
	- Visualize the relationship between product categories and the best-seller status using a stacked bar chart.
    Reading the chart: every bar is overwhelmingly grey (Not Best Seller) because even the "best" categories only reach ~5-6% best-seller share — there's no category where best-sellers form a large visible chunk of the bar. Grocery and Health & Personal Care edge out the rest, but the differences that felt dramatic in the table (5.8% vs 0.33% baseline) look subtle on a 0–100% stacked chart, since best-seller status is rare everywhere. That visual understatement is itself consistent with the weak Cramér's V — category tilts the odds, but doesn't come close to determining best-seller status.

---

### Part 2: Exploring Product Prices and Ratings Across Categories and Brands

**Objective**: Investigate how different product categories influence product prices.
Products priced below the first quartile minus 1.5 times the IQR or above the third quartile plus 1.5 times the IQR will be considered outliers and removed from the dataset. The next steps will be done with the dataframe without outliers.

0. **Preliminary Step: Remove outliers in product prices.**

	For this purpose, we can use the IQR (Interquartile Range) method. Products priced below the first quartile minus 1.5 times the IQR or above the third quartile plus 1.5 times the IQR will be considered outliers and removed from the dataset. The next steps will be done with the dataframe without outliers.
	
	*Hint: you can check the last Check For Understanding at the end of the lesson EDA Bivariate Analysis for a hint on how to do this.*

1. **Violin Plots**:
    - Use a violin plot to visualize the distribution of `price` across different product `categories`. Filter out the top 20 categories based on count for better visualization.
    Highest median price (unfiltered, min 30 listings for reliability): Desktop PCs, at a median of £74.00 (post-outlier-removal) — followed closely by Boxing Shoes (£69.79) and Tablets (£69.00). Note this is after removing the >£99.99 outliers, so this reflects the "everyday, non-extreme" price ceiling for that category rather than premium/flagship pricing.
    - Which product category tends to have the highest median price? Don't filter here by top categories.
    Within the top-20-by-volume categories shown in the violin plot, the shapes vary a lot — some (like Sports & Outdoors, given its massive size) show a wide, multi-modal spread, while niche accessory categories show tighter, lower-priced distributions clustered near the bottom of the price range.

2. **Bar Charts**:
    - Create a bar chart comparing the average price of products for the top 10 product categories (based on count).
    Sports & Outdoors	£25.17
Birthday Gifts	£18.60
Handmade Gifts	£17.40
Skin Care	£15.65
Bath & Body	£14.68
Hair Care	£13.46
Handmade Clothing, Shoes & Accessories	£12.96
Beauty	£12.52
Make-up	£10.61
Manicure & Pedicure Products	£10.23
    - Which product category commands the highest average price? Don't filter here by top categories.
    Within the top 10 categories by volume: Sports & Outdoors has by far the highest average price (£25.17), well ahead of Birthday Gifts (£18.60) and Handmade Gifts (£17.40).

3. **Box Plots**:
    - Visualize the distribution of product `ratings` based on their `category` using side-by-side box plots. Filter out the top 10 categories based on count for better visualization.
     Within the top 10 categories by volume: Handmade Clothing, Shoes & Accessories has the highest median rating (4.9), with Birthday Gifts and Handmade Gifts tied close behind at 4.8.
    - Which category tends to receive the highest median rating from customers? Don't filter here by top categories.
    Unfiltered — highest median rating across all categories (min 30 rated listings): a perfect 5.0 median, shared by Handmade Baby Products, Handmade Artwork, and Made in Italy Handmade. Notice the pattern — handmade/artisan categories dominate the top of both this list and the top-10 list. That tracks with intuition: handmade goods tend to be low-volume, purpose-bought items from small sellers, and buyers who go out of their way to purchase them are more likely to be satisfied (or more likely to leave a glowing review specifically).

---

### Part 3: Investigating the Interplay Between Product Prices and Ratings

**Objective**: Analyze how product ratings (`stars`) correlate with product prices.

1. **Correlation Coefficients**:
    - Calculate the correlation coefficient between `price` and `stars`.
    Pearson r	0.0067	1.08×10⁻¹²
Spearman r	0.0247	1.98×10⁻¹⁴⁹
    - Is there a significant correlation between product price and its rating?
    Statistically, technically yes (p-values are near zero) — but this is another case of a huge sample size making even a trivial effect "statistically significant." The actual correlation coefficients (0.007 and 0.025) are essentially zero in practical terms. Price tells you almost nothing about how a product will be rated — cheap products and expensive products get rated about the same, on average. Don't read anything meaningful into "significant" here; it's a sample-size artifact, not a real relationship.
	
2. **Visualizations**:
    - Use a scatter plot to visualize the relationship between product rating and price. What patterns can you observe?
    Scatter/density plot (price vs. rating): with 1.1M points, a raw scatter plot is just a solid blob, so I used a hexbin density plot instead. The pattern confirms the near-zero correlation: density is heaviest around 4–4.5 stars across every price band from £0 to £100 — there's no visible upward or downward slope. Cheap and expensive products alike concentrate at high ratings; price simply isn't a predictor of rating.
    - Use a correlation heatmap to visualize correlations between all numerical variables.
    Every off-diagonal value is weak (all under 0.12 in magnitude). The strongest relationships in the whole dataset are between stars, reviews, and boughtInLastMonth (all ~0.08–0.11) — a faint but sensible "popular products get bought more, reviewed more, and rated slightly higher" pattern — but even these are far too weak to call meaningful. Price is essentially uncorrelated with all three engagement metrics.
    - Examine if product prices typically follow a normal distribution using a QQ plot. 
    No, clearly not. The left panel (raw price, even after IQR outlier removal) bows sharply away from the diagonal reference line in the upper tail — actual price values shoot up far faster than a normal distribution would predict. This matches the skewness of 1.64 (positive/right-skewed) I calculated, plus a Shapiro-Wilk test (n=5,000 sample) that firmly rejects normality (p ≈ 5.5×10⁻⁶⁰). The right panel shows what happens if you log-transform price first (log(1+price)) — the points hug the diagonal much more closely, and skewness drops to just 0.09. Practical takeaway: if any downstream modeling assumes normally-distributed price (e.g. linear regression, certain hypothesis tests), log-transforming price first is the standard fix, and this QQ plot is the direct evidence that transformation is needed.

---

**Submission**: Submit a Jupyter Notebook which contains code and a business-centric report summarizing your findings. 

**Bonus**: 

- Do the same analysis without taking out the outliers. What are your insights?
Correlation coefficients (Pearson especially) are not robust here — a handful of extreme-price products were enough to flip the sign of the price↔stars Pearson correlation. Any conclusion drawn from Pearson r alone, without checking Spearman or visualizing the data, would be shaky.
The scatter/hexbin plot's shape barely changes where the bulk of the data lives (£0–£100, 4–4.5 stars) — the outliers add a sparse scatter of points at the very top of the price axis but don't change the core story: price and rating aren't meaningfully related.
The QQ plot is the most dramatically affected. It goes from "clearly non-normal, right-skewed" to "almost unusable as a diagnostic" — the extreme tail dominates the visual so much that you can't easily assess the shape of the other 99% of the distribution anymore.
Practical takeaway: for this dataset, outlier removal doesn't change the substantive conclusion (price and rating are weakly related), but it dramatically changes the reliability and readability of the statistics and diagnostics used to reach that conclusion. This is a good illustration of why IQR-trimming or at least robust statistics (Spearman, median, log-transforms) matter before trusting Pearson correlation or QQ plots on real-world, long-tailed pricing data — a small number of extreme values can silently mislead a linear-correlation-based analysis even when the median-level pattern hasn't actually shifted.
