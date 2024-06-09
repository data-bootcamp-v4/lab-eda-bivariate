## Week 5 Lab 2 report

### Part 1: Analyzing Best-Seller Trends Across Product Categories

1. **Crosstab Analysis**:
    
    - Are there categories where being a best-seller is more prevalent? 
    
    Yes, the 'Grocery' and 'Health & Personal Care' categories had a high number of Best Seller products (both in excess of 550). A further column calculating the percentage of Best Sellers in a category to adjust for different category sizes. While the two leading initial columns still had a high percentage of Best Sellers (~5.8%), a further category: 'Smart Home Security & Lighting' was also a top performer with 5.77%.

2. **Statistical Tests**:
    - Conduct a Chi-square test to determine if the best-seller distribution is independent of the product category.
    - Compute Cramér's V to understand the strength of association between best-seller status and category.

    The low (p) value of 0 would suggest that there is a relationship between the Best Seller distribution and the category as variables. However, the low Cramér result of 0.12 suggests that the association is not strong at all.
    
    
### Part 2: Exploring Product Prices and Ratings Across Categories and Brands

**Objective**: Investigate how different product categories influence product prices.

1. **Violin Plots**:
    - Which product category tends to have the highest median price? Don't filter here by top categories.
    
    Without filtering for top categories (but having eliminated outliers), the category with the top median price is Desktop PCs at $74.00.

2. **Bar Charts**:
    - Create a bar chart comparing the average price of products for the top 10 product categories (based on count).
    - Which product category commands the highest average price? Don't filter here by top categories.

3. **Box Plots**:
    - Visualize the distribution of product `ratings` based on their `category` using side-by-side box plots. Filter out the top 10 categories based on count for better visualization.
    - Which category tends to receive the highest median rating from customers? Don't filter here by top categories.

    Based on their category, computer memory products receive the highest median ratings.
---

### Part 3: Investigating the Interplay Between Product Prices and Ratings

**Objective**: Analyze how product ratings (`stars`) correlate with product prices.

1. **Correlation Coefficients**:
    - Is there a significant correlation between product price and its rating?
    
    No, there is a slight negative linear and monotonic relationship between the variables but it is not significant.
    
	
2. **Visualizations**:
    - Use a scatter plot to visualize the relationship between product rating and price. What patterns can you observe?
    
    There are few observable trends in the visualisation aside from a concentration of ratings at 0 stars and none between 0 and 1 star. There is a concentration of values near to 5 stars and between 0-20 USD.
    
    - Examine if product prices typically follow a normal distribution using a QQ plot. 
    
    Product prices are somewhat normally distributed for the majority of the population, however there is a significant right skew, as shown in the elevated upper tail. This reflects the scatter plot pattern of a high concentration of values in the upper 4.8-5.0 star range. 