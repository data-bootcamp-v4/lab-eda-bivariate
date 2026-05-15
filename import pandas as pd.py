import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency
import matplotlib.pyplot as plt
import seaborn as sns

# Search for potential datasets in the current directory
import os
csv_files = [f for f in os.listdir('.') if f.endswith('.csv')]

if csv_files:
    # Use the first available CSV
    df = pd.read_csv(csv_files[0])
else:
    # Generate synthetic data for demonstration if no file is found
    np.random.seed(42)
    categories = ['Electronics', 'Books', 'Clothing', 'Home', 'Toys']
    data = {
        'category': np.random.choice(categories, 500),
        'isBestSeller': np.random.choice([True, False], 500, p=[0.2, 0.8])
    }
    # Bias the 'Books' category to have more best-sellers
    df = pd.DataFrame(data)
    df.loc[df['category'] == 'Books', 'isBestSeller'] = np.random.choice([True, False], len(df[df['category'] == 'Books']), p=[0.4, 0.6])

# 1. Crosstab Analysis
crosstab = pd.crosstab(df['category'], df['isBestSeller'])
crosstab_prop = pd.crosstab(df['category'], df['isBestSeller'], normalize='index')

# Sorting categories by proportion of best-sellers (True)
sorted_proportions = crosstab_prop[True].sort_values(ascending=False)

print("Crosstab (Counts):")
print(crosstab)
print("\nProportion of Best-Sellers by Category (Sorted):")
print(sorted_proportions)

# 2. Statistical Tests
# Chi-square test
chi2, p_val, dof, expected = chi2_contingency(crosstab)

# Cramér's V
n = crosstab.sum().sum()
phi2 = chi2 / n
r, k = crosstab.shape
# Bias correction for Cramer's V is often omitted for simplicity unless specified
cramers_v = np.sqrt(phi2 / min(k - 1, r - 1))

print(f"\nChi-square statistic: {chi2:.4f}")
print(f"P-value: {p_val:.4f}")
print(f"Cramér's V: {cramers_v:.4f}")

# 3. Visualization
plt.figure(figsize=(12, 7))
crosstab_prop.plot(kind='bar', stacked=True, color=['#7fb3d5', '#f39c12'], ax=plt.gca())
plt.title('Proportion of Best-Sellers by Category', fontsize=14)
plt.ylabel('Proportion')
plt.xlabel('Category')
plt.legend(title='Is Best Seller', labels=['False', 'True'], loc='upper right')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('bestseller_stacked_bar.png')
plt.show() 
