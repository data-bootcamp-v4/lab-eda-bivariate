""" Load dataset and importing libraries """
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy.stats import chi2_contingency
from scipy.stats.contingency import association
import scipy.stats as stats

df = pd.read_csv('amz_uk_price_prediction_dataset.csv')


""" Part 1: Analyzing Best-Seller Trends Across Product Categories """

# 1. Crosstab Analysis:
crosstab_result = pd.crosstab(df['category'], df['isBestSeller'])

# 2. Statistical Tests:
# Chi-square test for 'MSZoning' and 'SaleCondition'
_, chi2_pvalue, _, _  = chi2_contingency(crosstab_result)
print(float(chi2_pvalue) < 0.05)
# Computing the association between variables in 'crosstab_result' using the "cramer" method
print(association(crosstab_result, method='cramer'))

# 3. Visualizations:
# Plotting a stacked bar chart for the 'crosstab_result' data
crosstab_result.head().plot(kind='bar', stacked=True, figsize=(12,6))
plt.show()

""" Part 2: Exploring Product Prices and Ratings Across Categories and Brands """
# 0. Preliminary Step: Remove outliers in product prices.
Q1 = df['price'].quantile(0.25)
Q3 = df['price'].quantile(0.75)
IQR = Q3 - Q1

# Define bounds for the outliers
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

df_without_outliers = df[(df['price'] > lower_bound) | (df['price'] < upper_bound)]

top_categories = df['category'].value_counts()
top_10_cat = df_without_outliers[df_without_outliers['category'].isin(top_categories.head(10).index)]

# 1. Violin Plots:
plt.figure(figsize=(14,8))
sns.violinplot(data=df_without_outliers[df_without_outliers['category'].isin(top_categories.head(20).index)], x="price", y="category", palette="Set2")
plt.tight_layout()
plt.show()
print(f"The product category with highest median price is: {df_without_outliers.groupby('category')['price'].mean().head(1).index}")

# 2. Bar Charts:
plt.figure(figsize=(12,8))

top_10_cat_avg_price = top_10_cat.groupby('category')['price'].mean().reset_index()
sns.barplot(data=top_10_cat_avg_price, x="price", y="category")
plt.show()
print(f"The product category with highest average price is:{top_10_cat_avg_price[top_10_cat_avg_price['price'] == top_10_cat_avg_price['price'].max()]['category']}")

# 3. Box Plots
plt.figure(figsize=(12,8))
sns.boxplot(x='stars', y='category', data=top_10_cat, palette='Set2')
plt.show()

"""Part 3: Investigating the Interplay Between Product Prices and Ratings"""

# 1. Correlation Coefficients
correlation = df_without_outliers['price'].corr(df_without_outliers['stars'])
print(f"Correlation coefficient between price and rating: {correlation:.2f}")

# 2. Visualization
plt.figure(figsize=(10, 6))
sns.scatterplot(x='stars', y='price', data=df, color='blue')
plt.tight_layout()
plt.show()

# 3. Correlation heatmap for all numerical variables
correlation_matrix = df.corr()

plt.figure(figsize=(10, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=1)
plt.tight_layout()
plt.show()

# 4. QQ plot to check if product prices follow a normal distribution
plt.figure(figsize=(8, 6))
stats.probplot(df['price'].dropna(), dist="norm", plot=plt)
plt.title('QQ Plot: Product Prices', fontsize=14)
plt.tight_layout()
plt.show()