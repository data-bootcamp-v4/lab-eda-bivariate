import os
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import chi2_contingency, probplot

DATA_PATH = "amz_uk_price_prediction_dataset.csv"
PLOTS_DIR = "plots_bivariate"

# For big datasets, sampling makes plots faster and still representative
PLOT_SAMPLE_SIZE = 250_000
RANDOM_SEED = 42

sns.set_theme()


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def normalize_best_seller(series: pd.Series) -> pd.Series:
    """
    Normalize isBestSeller to 0/1.
    Handles booleans, 0/1, and string forms.
    """
    s = series.astype(str).str.strip().str.lower()
    mapped = s.map({"true": 1, "1": 1, "yes": 1, "false": 0, "0": 0, "no": 0})
    return mapped.fillna(0).astype(int)


def cramers_v(ct: pd.DataFrame) -> float:
    """
    Cramér's V for association strength between two categorical vars.
    """
    chi2, _, _, _ = chi2_contingency(ct)
    n = ct.to_numpy().sum()
    if n == 0:
        return float("nan")
    r, k = ct.shape
    denom = n * (min(r - 1, k - 1))
    if denom == 0:
        return float("nan")
    return float(math.sqrt(chi2 / denom))


def sample_df(df: pd.DataFrame, n: int = PLOT_SAMPLE_SIZE) -> pd.DataFrame:
    if len(df) > n:
        return df.sample(n, random_state=RANDOM_SEED)
    return df


def remove_outliers_iqr(df: pd.DataFrame, col: str) -> tuple[pd.DataFrame, float, float]:
    """
    Remove outliers using IQR rule for col.
    Returns cleaned_df, lower_bound, upper_bound
    """
    s = df[col].dropna()
    q1 = s.quantile(0.25)
    q3 = s.quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    cleaned = df[(df[col] >= lower) & (df[col] <= upper)].copy()
    return cleaned, float(lower), float(upper)


def main():
    ensure_dir(PLOTS_DIR)

    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(
            f"Dataset not found: {DATA_PATH}\n"
            "Place it in the same folder as this script (do NOT commit it)."
        )

    # Load only needed columns to reduce memory
    usecols = ["category", "isBestSeller", "price", "stars", "reviews", "boughtInLastMonth", "title"]
    df = pd.read_csv(DATA_PATH, usecols=usecols)

    # Basic cleaning
    df["category"] = df["category"].fillna("Unknown")
    df["isBestSeller"] = normalize_best_seller(df["isBestSeller"])
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["stars"] = pd.to_numeric(df["stars"], errors="coerce")
    df["reviews"] = pd.to_numeric(df["reviews"], errors="coerce")
    df["boughtInLastMonth"] = pd.to_numeric(df["boughtInLastMonth"], errors="coerce")

    
    # Part 1: Best-seller trends across categories
    
    ct = pd.crosstab(df["category"], df["isBestSeller"])

    # Make sure both columns exist (0 and 1)
    for col in [0, 1]:
        if col not in ct.columns:
            ct[col] = 0
    ct = ct[[0, 1]]

    ct["total"] = ct[0] + ct[1]
    ct["best_seller_rate"] = np.where(ct["total"] > 0, ct[1] / ct["total"], 0.0)

    # Categories where best-seller is more prevalent:
    # Sort by best-seller rate, but also show counts to avoid tiny-category noise.
    best_rate_sorted = ct.sort_values("best_seller_rate", ascending=False)

    # Chi-square test
    chi2, p_value, dof, _ = chi2_contingency(ct[[0, 1]])
    v = cramers_v(ct[[0, 1]])

    # Stacked bar for top 20 categories by total count (readable)
    top20 = ct.sort_values("total", ascending=False).head(20)

    plt.figure(figsize=(12, 6))
    plt.bar(top20.index, top20[0], label="Not Best Seller")
    plt.bar(top20.index, top20[1], bottom=top20[0], label="Best Seller")
    plt.xticks(rotation=90)
    plt.title("Best-seller status by category (Top 20 categories by listings)")
    plt.ylabel("Number of products")
    plt.legend()
    plt.tight_layout()
    stacked_path = os.path.join(PLOTS_DIR, "stacked_bar_best_seller_top20.png")
    plt.savefig(stacked_path, dpi=200)
    plt.close()

    
    # Part 2: Prices and ratings across categories (remove outliers)
    
    df_no_outliers, lower_b, upper_b = remove_outliers_iqr(df, "price")

    # Filter top 20 categories by count for violin plot readability
    top20_cats = df_no_outliers["category"].value_counts().head(20).index
    df_top20 = df_no_outliers[df_no_outliers["category"].isin(top20_cats)]
    df_top20_plot = sample_df(df_top20)

    # Violin plot: price by category (top 20 by count)
    plt.figure(figsize=(14, 6))
    sns.violinplot(data=df_top20_plot, x="category", y="price", inner="quartile", cut=0)
    plt.xticks(rotation=90)
    plt.title("Price distribution by category (Top 20 categories, outliers removed)")
    plt.tight_layout()
    violin_path = os.path.join(PLOTS_DIR, "violin_price_top20_no_outliers.png")
    plt.savefig(violin_path, dpi=200)
    plt.close()

    # Highest median price category overall (DO NOT filter)
    median_price_by_cat = df_no_outliers.groupby("category")["price"].median().sort_values(ascending=False)
    highest_median_price_category = median_price_by_cat.index[0]
    highest_median_price_value = float(median_price_by_cat.iloc[0])

    # Bar chart: avg price top 10 categories by count (as requested)
    top10_cats = df_no_outliers["category"].value_counts().head(10).index
    avg_price_top10 = (
        df_no_outliers[df_no_outliers["category"].isin(top10_cats)]
        .groupby("category")["price"]
        .mean()
        .sort_values(ascending=False)
    )

    plt.figure(figsize=(10, 5))
    avg_price_top10.plot(kind="bar")
    plt.xticks(rotation=45, ha="right")
    plt.title("Average price by category (Top 10 categories by listings, outliers removed)")
    plt.ylabel("Average price")
    plt.tight_layout()
    avg_bar_path = os.path.join(PLOTS_DIR, "bar_avg_price_top10_no_outliers.png")
    plt.savefig(avg_bar_path, dpi=200)
    plt.close()

    # Highest average price category overall (DO NOT filter)
    mean_price_by_cat = df_no_outliers.groupby("category")["price"].mean().sort_values(ascending=False)
    highest_avg_price_category = mean_price_by_cat.index[0]
    highest_avg_price_value = float(mean_price_by_cat.iloc[0])

    # Box plots: stars by category (top 10 categories by count for readability)
    df_stars_top10 = df_no_outliers[df_no_outliers["category"].isin(top10_cats)].copy()
    df_stars_plot = sample_df(df_stars_top10)

    plt.figure(figsize=(12, 6))
    sns.boxplot(data=df_stars_plot, x="category", y="stars")
    plt.xticks(rotation=45, ha="right")
    plt.title("Stars rating by category (Top 10 categories, price outliers removed)")
    plt.tight_layout()
    stars_box_path = os.path.join(PLOTS_DIR, "box_stars_top10_no_outliers.png")
    plt.savefig(stars_box_path, dpi=200)
    plt.close()

    # Highest median rating category overall (DO NOT filter)
    median_stars_by_cat = df_no_outliers.groupby("category")["stars"].median().sort_values(ascending=False)
    highest_median_rating_category = median_stars_by_cat.index[0]
    highest_median_rating_value = float(median_stars_by_cat.iloc[0])

   
    # Part 3: Price vs Stars
    
    numeric_cols = ["price", "stars", "reviews", "boughtInLastMonth"]
    corr_df = df_no_outliers[numeric_cols].dropna()

    price_stars_corr = float(corr_df["price"].corr(corr_df["stars"]))

    # Scatter plot (sample)
    scatter_df = sample_df(df_no_outliers[["price", "stars"]].dropna())

    plt.figure(figsize=(7, 5))
    plt.scatter(scatter_df["stars"], scatter_df["price"], s=5)
    plt.title("Price vs Stars (scatter, outliers removed)")
    plt.xlabel("Stars")
    plt.ylabel("Price")
    plt.tight_layout()
    scatter_path = os.path.join(PLOTS_DIR, "scatter_price_vs_stars_no_outliers.png")
    plt.savefig(scatter_path, dpi=200)
    plt.close()

    # Heatmap of correlations among numeric variables
    corr_matrix = corr_df.corr(numeric_only=True)

    plt.figure(figsize=(6, 5))
    sns.heatmap(corr_matrix, annot=True, fmt=".2f")
    plt.title("Correlation heatmap (numeric variables, outliers removed)")
    plt.tight_layout()
    heatmap_path = os.path.join(PLOTS_DIR, "heatmap_correlations_no_outliers.png")
    plt.savefig(heatmap_path, dpi=200)
    plt.close()

    # QQ plot for price normality (outliers removed; sample)
    qq_series = df_no_outliers["price"].dropna()
    if len(qq_series) > PLOT_SAMPLE_SIZE:
        qq_series = qq_series.sample(PLOT_SAMPLE_SIZE, random_state=RANDOM_SEED)

    plt.figure(figsize=(6, 5))
    probplot(qq_series, dist="norm", plot=plt)
    plt.title("QQ Plot: Price vs Normal (outliers removed)")
    plt.tight_layout()
    qq_path = os.path.join(PLOTS_DIR, "qqplot_price_no_outliers.png")
    plt.savefig(qq_path, dpi=200)
    plt.close()

    # BONUS: Repeat key analysis WITHOUT removing outliers
    corr_df_full = df[numeric_cols].dropna()
    price_stars_corr_full = float(corr_df_full["price"].corr(corr_df_full["stars"]))

    qq_full = df["price"].dropna()
    if len(qq_full) > PLOT_SAMPLE_SIZE:
        qq_full = qq_full.sample(PLOT_SAMPLE_SIZE, random_state=RANDOM_SEED)

    plt.figure(figsize=(6, 5))
    probplot(qq_full, dist="norm", plot=plt)
    plt.title("QQ Plot: Price vs Normal (WITH outliers)")
    plt.tight_layout()
    qq_full_path = os.path.join(PLOTS_DIR, "qqplot_price_with_outliers.png")
    plt.savefig(qq_full_path, dpi=200)
    plt.close()

    # Write business report
    report_path = "report_bivariate.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# Amazon UK Product Dataset — Bivariate EDA Report\n\n")

        f.write("## Part 1 — Best-seller trends across categories\n\n")
        f.write("### Crosstab insights\n")
        f.write("We created a crosstab between `category` and `isBestSeller` and computed the best-seller rate per category.\n\n")
        f.write("Top categories by best-seller rate (note: very small categories can appear here):\n\n")
        for cat, row in best_rate_sorted.head(10).iterrows():
            f.write(f"- **{cat}**: best-seller rate={row['best_seller_rate']:.2%}, n={int(row['total']):,}\n")

        f.write("\n### Statistical tests\n")
        f.write(f"- Chi-square test: chi2={chi2:.2f}, dof={dof}, p-value={p_value:.6g}\n")
        f.write(f"- Cramér’s V: {v:.4f}\n\n")
        f.write("Interpretation guidance:\n")
        f.write("- If p-value < 0.05, category and best-seller status are not independent.\n")
        f.write("- Cramér’s V ~0.1 small, ~0.3 medium, ~0.5 large association (rule of thumb).\n\n")
        f.write(f"Chart: `{stacked_path}`\n\n")

        f.write("## Part 2 — Prices and ratings across categories (outliers removed with IQR)\n\n")
        f.write(f"Outlier bounds for price using IQR: lower={lower_b:.2f}, upper={upper_b:.2f}\n\n")
        f.write(f"- Highest **median** price category (overall): **{highest_median_price_category}** (median={highest_median_price_value:.2f})\n")
        f.write(f"- Highest **average** price category (overall): **{highest_avg_price_category}** (mean={highest_avg_price_value:.2f})\n")
        f.write(f"- Highest **median** rating category (overall): **{highest_median_rating_category}** (median={highest_median_rating_value:.2f})\n\n")
        f.write("Charts:\n")
        f.write(f"- `{violin_path}`\n")
        f.write(f"- `{avg_bar_path}`\n")
        f.write(f"- `{stars_box_path}`\n\n")

        f.write("## Part 3 — Relationship between price and stars\n\n")
        f.write(f"- Pearson correlation (price vs stars, outliers removed): **{price_stars_corr:.4f}**\n\n")
        f.write("Charts:\n")
        f.write(f"- `{scatter_path}`\n")
        f.write(f"- `{heatmap_path}`\n")
        f.write(f"- `{qq_path}`\n\n")

        f.write("## Bonus — Without removing outliers\n\n")
        f.write(f"- Pearson correlation (price vs stars, with outliers): **{price_stars_corr_full:.4f}**\n")
        f.write("Insight:\n")
        f.write("- Outliers often distort plots and can change correlations.\n")
        f.write("- QQ plots with outliers typically show stronger deviation from normality.\n\n")
        f.write(f"Chart: `{qq_full_path}`\n")

    # Console summary
    print("Bivariate EDA complete.")
    print(f"Saved plots to: {PLOTS_DIR}/")
    print(f"Saved report to: {report_path}\n")

    print("Key results:")
    print(f"- Chi-square p-value: {p_value:.6g}")
    print(f"- Cramér’s V: {v:.4f}")
    print(f"- Corr(price, stars) no outliers: {price_stars_corr:.4f}")
    print(f"- Corr(price, stars) with outliers: {price_stars_corr_full:.4f}")
    print(f"- Highest median price category: {highest_median_price_category} ({highest_median_price_value:.2f})")
    print(f"- Highest avg price category: {highest_avg_price_category} ({highest_avg_price_value:.2f})")
    print(f"- Highest median rating category: {highest_median_rating_category} ({highest_median_rating_value:.2f})")


if __name__ == "__main__":
    main()
