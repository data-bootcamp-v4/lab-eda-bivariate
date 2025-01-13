## Lab - EDA Bivariate Analysis: Diving into Amazon UK Product Insights Part II

**Objective**: Delve into the dynamics of product pricing on Amazon UK to uncover insights that can inform business strategies and decision-making.

**Dataset**: This lab utilizes the [Amazon UK product dataset](https://www.kaggle.com/datasets/asaniczka/uk-optimal-product-price-prediction/)
which provides information on product categories, brands, prices, ratings, and more from from Amazon UK. You'll need to download it to start working with it.

---

### Part 1: Analyzing Best-Seller Trends Across Product Categories

**Objective**: Understand the relationship between product categories and their best-seller status.

1. **Crosstab Analysis**:
    - Create a crosstab between the product `category` and the `isBestSeller` status.
    
    - Are there categories where being a best-seller is more prevalent? 
    	
    	*Hint: one option is to calculate the proportion of best-sellers for each category and then sort the categories based on this proportion in descending order.*


2. **Statistical Tests**:
    - Conduct a Chi-square test to determine if the best-seller distribution is independent of the product category.
    - Compute Cramér's V to understand the strength of association between best-seller status and category.

3. **Visualizations**:
	- Visualize the relationship between product categories and the best-seller status using a stacked bar chart.

---

### Part 2: Exploring Product Prices and Ratings Across Categories and Brands

**Objective**: Investigate how different product categories influence product prices.

0. **Preliminary Step: Remove outliers in product prices.**

	For this purpose, we can use the IQR (Interquartile Range) method. Products priced below the first quartile minus 1.5 times the IQR or above the third quartile plus 1.5 times the IQR will be considered outliers and removed from the dataset. The next steps will be done with the dataframe without outliers.
	
	*Hint: you can check the last Check For Understanding at the end of the lesson EDA Bivariate Analysis for a hint on how to do this.*

1. **Violin Plots**:
    - Use a violin plot to visualize the distribution of `price` across different product `categories`. Filter out the top 20 categories based on count for better visualization.
    - Which product category tends to have the highest median price? Don't filter here by top categories.

2. **Bar Charts**:
    - Create a bar chart comparing the average price of products for the top 10 product categories (based on count).
    - Which product category commands the highest average price? Don't filter here by top categories.

3. **Box Plots**:
    - Visualize the distribution of product `ratings` based on their `category` using side-by-side box plots. Filter out the top 10 categories based on count for better visualization.
    - Which category tends to receive the highest median rating from customers? Don't filter here by top categories.

---

### Part 3: Investigating the Interplay Between Product Prices and Ratings

**Objective**: Analyze how product ratings (`stars`) correlate with product prices.

1. **Correlation Coefficients**:
    - Calculate the correlation coefficient between `price` and `stars`.
    - Is there a significant correlation between product price and its rating?
	
2. **Visualizations**:
    - Use a scatter plot to visualize the relationship between product rating and price. What patterns can you observe?
    - Use a correlation heatmap to visualize correlations between all numerical variables.
    - Examine if product prices typically follow a normal distribution using a QQ plot. 

---

**Submission**: Submit a Jupyter Notebook which contains code and a business-centric report summarizing your findings. 

**Bonus**: 

- Do the same analysis without taking out the outliers. What are your insights?

###Solution
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import chi2_contingency, pearsonr, probplot
from sklearn.preprocessing import LabelEncoder

# Load dataset
data = pd.read_csv('amazon_uk_product_dataset.csv')  # Replace with actual file path

# Part 1: Analyzing Best-Seller Trends Across Product Categories

# 1. Crosstab Analysis
crosstab = pd.crosstab(data['category'], data['isBestSeller'])
crosstab_prop = crosstab.div(crosstab.sum(axis=1), axis=0)
crosstab_prop_sorted = crosstab_prop.sort_values(by=1, ascending=False)
print(crosstab_prop_sorted)

# 2. Chi-square Test
chi2, p, dof, ex = chi2_contingency(crosstab)
print(f"Chi-square Statistic: {chi2}, p-value: {p}")

# Cramér's V
n = crosstab.sum().sum()
cramers_v = np.sqrt(chi2 / (n * (min(crosstab.shape) - 1)))
print(f"Cramér's V: {cramers_v}")

# 3. Stacked Bar Chart
crosstab.plot(kind='bar', stacked=True, figsize=(10, 6))
plt.title('Best-Seller Distribution Across Categories')
plt.xlabel('Category')
plt.ylabel('Count')
plt.legend(title='Is Best Seller')
plt.tight_layout()
plt.show()

# Part 2: Exploring Product Prices and Ratings Across Categories and Brands

# 0. Remove Outliers in Product Prices
Q1 = data['price'].quantile(0.25)
Q3 = data['price'].quantile(0.75)
IQR = Q3 - Q1
filtered_data = data[(data['price'] >= Q1 - 1.5 * IQR) & (data['price'] <= Q3 + 1.5 * IQR)]

# 1. Violin Plot
top_20_categories = filtered_data['category'].value_counts().nlargest(20).index
sns.violinplot(x='category', y='price', data=filtered_data[filtered_data['category'].isin(top_20_categories)])
plt.xticks(rotation=90)
plt.title('Price Distribution Across Top 20 Categories')
plt.show()

# 2. Bar Chart for Average Price
avg_price = filtered_data.groupby('category')['price'].mean().nlargest(10)
avg_price.plot(kind='bar', figsize=(10, 6))
plt.title('Average Price of Top 10 Categories')
plt.xlabel('Category')
plt.ylabel('Average Price')
plt.show()

# 3. Box Plot for Ratings
sns.boxplot(x='category', y='stars', data=filtered_data[filtered_data['category'].isin(top_20_categories)])
plt.xticks(rotation=90)
plt.title('Ratings Distribution Across Top 10 Categories')
plt.show()

# Part 3: Investigating the Interplay Between Product Prices and Ratings

# 1. Correlation Coefficient
corr, _ = pearsonr(filtered_data['price'], filtered_data['stars'])
print(f"Correlation between Price and Stars: {corr}")

# 2. Scatter Plot
sns.scatterplot(x='stars', y='price', data=filtered_data)
plt.title('Price vs. Rating')
plt.xlabel('Rating')
plt.ylabel('Price')
plt.show()

# Correlation Heatmap
sns.heatmap(filtered_data.corr(), annot=True, cmap='coolwarm')
plt.title('Correlation Heatmap')
plt.show()

# QQ Plot for Price Distribution
probplot(filtered_data['price'], dist="norm", plot=plt)
plt.title('QQ Plot for Price Distribution')
plt.show()
