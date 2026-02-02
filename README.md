# =========================================================
# LAB - EDA BIVARIATE ANALYSIS
# Amazon UK Product Insights - Part II
# Single code cell (GitHub ready)
# =========================================================

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import scipy.stats as st

sns.set(style="whitegrid")

# ===============================
# LOAD DATA
# ===============================
df = pd.read_csv("data/amazon_uk_products.csv")

print("Dataset shape:", df.shape)

# =========================================================
# PART 1 — BEST-SELLER TRENDS
# =========================================================

print("\n=== PART 1: Best-Seller Analysis ===")

# Crosstab
crosstab = pd.crosstab(df["category"], df["isBestSeller"])
print("\nCrosstab (head):")
print(crosstab.head())

# Proportion of best-sellers
best_seller_prop = (
    crosstab.div(crosstab.sum(axis=1), axis=0)
    .sort_values(by=True, ascending=False)
)

print("\nTop categories by best-seller proportion:")
print(best_seller_prop.head(10))

# Chi-square test
chi2, p_value, dof, expected = st.chi2_contingency(crosstab)

print(f"\nChi-square statistic: {chi2:.2f}")
print(f"p-value: {p_value:.4f}")

if p_value < 0.05:
    print("Conclusion: Best-seller status depends on product category.")
else:
    print("Conclusion: Best-seller status is independent of product category.")

# Cramér's V
n = crosstab.sum().sum()
cramers_v = np.sqrt(chi2 / (n * (min(crosstab.shape) - 1)))
print(f"Cramér's V: {cramers_v:.3f}")

# Visualization
best_seller_prop.head(15).plot(
    kind="bar",
    stacked=True,
    figsize=(12,6)
)
plt.title("Best-Seller Proportion by Category (Top 15)")
plt.ylabel("Proportion")
plt.xlabel("Category")
plt.legend(title="Is Best Seller")
plt.tight_layout()
plt.show()

# =========================================================
# PART 2 — PRICES & RATINGS
# =========================================================

print("\n=== PART 2: Prices and Ratings ===")

# Remove price outliers (IQR)
Q1 = df["price"].quantile(0.25)
Q3 = df["price"].quantile(0.75)
IQR = Q3 - Q1

df_no_outliers = df[
    (df["price"] >= Q1 - 1.5 * IQR) &
    (df["price"] <= Q3 + 1.5 * IQR)
]

print("Shape after removing outliers:", df_no_outliers.shape)

# ----- Violin plot (Top 20 categories)
top20_categories = (
    df_no_outliers["category"]
    .value_counts()
    .head(20)
    .index
)

plt.figure(figsize=(14,6))
sns.violinplot(
    data=df_no_outliers[df_no_outliers["category"].isin(top20_categories)],
    x="category",
    y="price"
)
plt.xticks(rotation=90)
plt.title("Price Distribution Across Top 20 Categories")
plt.tight_layout()
plt.show()

# Highest median price (no filter)
print("\nHighest median prices by category:")
print(
    df_no_outliers
    .groupby("category")["price"]
    .median()
    .sort_values(ascending=False)
    .head(5)
)

# ----- Bar chart (Average price)
top10_categories = (
    df_no_outliers["category"]
    .value_counts()
    .head(10)
    .index
)

avg_price = (
    df_no_outliers[df_no_outliers["category"].isin(top10_categories)]
    .groupby("category")["price"]
    .mean()
    .sort_values(ascending=False)
)

avg_price.plot(kind="bar", figsize=(10,5))
plt.title("Average Price by Category (Top 10)")
plt.ylabel("Average Price")
plt.tight_layout()
plt.show()

# ----- Box plot (Ratings)
plt.figure(figsize=(14,6))
sns.boxplot(
    data=df_no_outliers[df_no_outliers["category"].isin(top10_categories)],
    x="category",
    y="stars"
)
plt.xticks(rotation=90)
plt.title("Ratings Distribution by Category (Top 10)")
plt.tight_layout()
plt.show()

print("\nHighest median ratings by category:")
print(
    df_no_outliers
    .groupby("category")["stars"]
    .median()
    .sort_values(ascending=False)
    .head(5)
)

# =========================================================
# PART 3 — PRICE VS RATINGS
# =========================================================

print("\n=== PART 3: Price vs Ratings ===")

# Correlation
corr, corr_p = st.pearsonr(
    df_no_outliers["price"],
    df_no_outliers["stars"]
)

print(f"Pearson correlation: {corr:.3f}")
print(f"p-value: {corr_p:.4f}")

# Scatter plot
plt.figure(figsize=(8,6))
sns.scatterplot(
    data=df_no_outliers,
    x="stars",
    y="price",
    alpha=0.3
)
plt.title("Price vs Rating")
plt.tight_layout()
plt.show()

# Correlation heatmap
plt.figure(figsize=(8,6))
sns.heatmap(
    df_no_outliers.select_dtypes("number").corr(),
    annot=True,
    cmap="coolwarm",
    fmt=".2f"
)
plt.title("Correlation Heatmap")
plt.tight_layout()
plt.show()

# QQ plot (price normality)
st.probplot(df_no_outliers["price"], plot=plt)
plt.title("QQ Plot — Price Distribution")
plt.tight_layout()
plt.show()

print("\n=== END OF ANALYSIS ===")
