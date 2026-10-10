import pandas as pd

# 1. Load data

orders_payments_reviews = pd.read_csv(
    "data/processed/orders_payments_reviews.csv"
)

order_products = pd.read_csv(
    "data/processed/order_products.csv"
)

order_payments = pd.read_csv(
    "data/raw/olist_order_payments_dataset.csv"
)

customers = pd.read_csv(
    "data/raw/olist_customers_dataset.csv"
)

# 2. Temporal sales analysis

orders_payments_reviews["order_purchase_timestamp"] = pd.to_datetime(
    orders_payments_reviews["order_purchase_timestamp"]
)

orders_quarterly = (
    orders_payments_reviews
    .groupby(
        orders_payments_reviews["order_purchase_timestamp"].dt.to_period("Q")
    )["payment_value"]
    .sum()
)

orders_monthly = (
    orders_payments_reviews
    .groupby(
        orders_payments_reviews["order_purchase_timestamp"].dt.to_period("M")
    )["payment_value"]
    .sum()
)

orders_count_monthly = (
    orders_payments_reviews
    .groupby(
        orders_payments_reviews["order_purchase_timestamp"].dt.to_period("M")
    )["order_id"]
    .nunique()
)

monthly_mean_order_value = (
    orders_monthly / orders_count_monthly
)

print("\n--- Quarterly Revenue ---")
print(orders_quarterly)

print("\n--- Monthly Revenue ---")
print(orders_monthly)

print("\n--- Monthly Order Count ---")
print(orders_count_monthly)

print("\n--- Monthly Average Order Value ---")
print(monthly_mean_order_value)

# 3. Category performance

category_sales = (
    order_products
    .groupby("product_category_name")["price"]
    .sum()
    .sort_values(ascending=False)
)

print("\n--- Sales by Category ---")
print(category_sales)

missing_categories = order_products["product_category_name"].isna().sum()
print("\nMissing product categories:", missing_categories)

category_sales_with_nan = (
    order_products
    .groupby("product_category_name", dropna=False)["price"]
    .sum()
)

print("\n--- Sales by Category Including Missing ---")
print(category_sales_with_nan)

total_price = order_products["price"].sum()
price_without_category = category_sales_with_nan[
    category_sales_with_nan.index.isna()
].sum()
percentage_without_category = price_without_category / total_price * 100

print("\nPercentage of sales without category:", percentage_without_category)

quantity_sold_by_category = (
    order_products
    .groupby("product_category_name")
    .size()
    .sort_values(ascending=False)
)

mean_price_per_category = category_sales / quantity_sold_by_category

category_performance = pd.DataFrame({
    "total_sales": category_sales,
    "quantity_sold": quantity_sold_by_category,
    "mean_price": mean_price_per_category,
})

category_performance_mean_sorted = category_performance.sort_values(
    "mean_price",
    ascending=False,
)

print("\n--- Category Performance ---")
print(category_performance)

print("\n--- Categories by Average Price ---")
print(category_performance_mean_sorted)

# 4. Product performance

product_sales = (
    order_products
    .groupby("product_id")["price"]
    .sum()
    .sort_values(ascending=False)
)

quantity_sold_per_product = (
    order_products
    .groupby("product_id")
    .size()
    .sort_values(ascending=False)
)

mean_price_per_product = product_sales / quantity_sold_per_product

product_performance = pd.DataFrame({
    "total_value": product_sales,
    "quantity_sold": quantity_sold_per_product,
    "mean_price": mean_price_per_product,
})

# Top 10 products by total sales

top_10_products_by_value = (
    product_performance
    .sort_values("total_value", ascending=False)
    .head(10)
)

print("\n--- Top 10 Products by Sales Value ---")
print(top_10_products_by_value)

# Top 10 products by quantity

top_10_products_by_quantity = (
    product_performance
    .sort_values("quantity_sold", ascending=False)
    .head(10)
)

print("\n--- Top 10 Products by Quantity Sold ---")
print(top_10_products_by_quantity)

# Products appearing in both Top 10 rankings

common_products = top_10_products_by_value.index.intersection(
    top_10_products_by_quantity.index
)

common_top_products = product_performance.loc[common_products]

print("\n--- Products in Both Top 10 Rankings ---")
print(common_top_products)

# 5. Seller performance

seller_total_value = (
    order_products
    .groupby("seller_id")["price"]
    .sum()
    .sort_values(ascending=False)
)

seller_quantity_sold = (
    order_products
    .groupby("seller_id")
    .size()
    .sort_values(ascending=False)
)

mean_price_per_seller = seller_total_value / seller_quantity_sold

seller_performance = pd.DataFrame({
    "total_value": seller_total_value,
    "quantity_sold": seller_quantity_sold,
    "mean_price": mean_price_per_seller,
})

# Top 10 sellers by total value

top_10_sellers_by_value = (
    seller_performance
    .sort_values("total_value", ascending=False)
    .head(10)
)

print("\n--- Top 10 Sellers by Sales Value ---")
print(top_10_sellers_by_value)

# Top 10 sellers by quantity sold

top_10_sellers_by_quantity = (
    seller_performance
    .sort_values("quantity_sold", ascending=False)
    .head(10)
)

print("\n--- Top 10 Sellers by Quantity Sold ---")
print(top_10_sellers_by_quantity)

# Sellers appearing in both Top 10 rankings

common_sellers = top_10_sellers_by_value.index.intersection(
    top_10_sellers_by_quantity.index
)

common_top_sellers = seller_performance.loc[common_sellers]

print("\n--- Sellers in Both Top 10 Rankings ---")
print(common_top_sellers)

# Top 10 sellers by average price

top_10_sellers_by_mean_price = (
    seller_performance
    .sort_values("mean_price", ascending=False)
    .head(10)
)

print("\n--- Top 10 Sellers by Average Price ---")
print(top_10_sellers_by_mean_price)

# 6. Payment type performance

payment_value_by_type = (
    order_payments
    .groupby("payment_type")["payment_value"]
    .sum()
    .sort_values(ascending=False)
)

payment_count_by_type = (
    order_payments
    .groupby("payment_type")["order_id"]
    .count()
    .sort_values(ascending=False)
)

unique_orders_by_payment_type = (
    order_payments
    .groupby("payment_type")["order_id"]
    .nunique()
    .sort_values(ascending=False)
)

mean_payment_record_value_by_type = (
    order_payments
    .groupby("payment_type")["payment_value"]
    .mean()
    .sort_values(ascending=False)
)

total_value_order_payments = order_payments["payment_value"].sum()

percentage_of_total_by_payment_type = (
    payment_value_by_type / total_value_order_payments * 100
).sort_values(ascending=False)

print("\n--- Payment Value by Type ---")
print(payment_value_by_type)

print("\n--- Payment Records by Type ---")
print(payment_count_by_type)

print("\n--- Unique Orders by Payment Type ---")
print(unique_orders_by_payment_type)

print("\n--- Mean Payment Record Value by Type ---")
print(mean_payment_record_value_by_type)

print("\n--- Percentage of Total Value by Payment Type ---")
print(percentage_of_total_by_payment_type)

# 7. Order status performance

order_value_by_status = (
    orders_payments_reviews
    .groupby("order_status")["payment_value"]
    .sum()
    .sort_values(ascending=False)
)

order_count_by_status = (
    orders_payments_reviews
    .groupby("order_status")["order_id"]
    .nunique()
    .sort_values(ascending=False)
)

percentage_of_total_by_status = (
    order_value_by_status / order_value_by_status.sum() * 100
).sort_values(ascending=False)

print("\n--- Order Value by Status ---")
print(order_value_by_status)

print("\n--- Order Count by Status ---")
print(order_count_by_status)

print("\n--- Percentage of Total Value by Status ---")
print(percentage_of_total_by_status)

# 8. Customer performance

customer_orders = pd.merge(
    orders_payments_reviews,
    customers[
        [
            "customer_id",
            "customer_unique_id",
            "customer_city",
            "customer_state",
        ]
    ],
    on="customer_id",
    how="left",
    validate="many_to_one",
)

# Orders per unique customer

orders_per_customer = (
    customer_orders
    .groupby("customer_unique_id")["order_id"]
    .nunique()
    .sort_values(ascending=False)
)

# Multiple customer IDs

customer_ids = (
    customer_orders
    .groupby("customer_unique_id")["customer_id"]
    .nunique()
)

print("\nCustomers with multiple IDs:", (customer_ids > 1).sum())

# Multiple cities

customer_cities = (
    customer_orders
    .groupby("customer_unique_id")["customer_city"]
    .nunique()
)

print("Customers with multiple cities:", (customer_cities > 1).sum())

# Multiple states

customer_states = (
    customer_orders
    .groupby("customer_unique_id")["customer_state"]
    .nunique()
)

print("Customers with multiple states:", (customer_states > 1).sum())

# One-order customers vs repeat customers

one_order_customers = orders_per_customer[orders_per_customer == 1].index
repeat_customers = orders_per_customer[orders_per_customer > 1].index

one_order = customer_orders[
    customer_orders["customer_unique_id"].isin(one_order_customers)
]

repeat_order = customer_orders[
    customer_orders["customer_unique_id"].isin(repeat_customers)
]

# Total revenue by customer type

one_order_value = one_order["payment_value"].sum()
repeat_order_value = repeat_order["payment_value"].sum()

# Mean revenue per customer

one_order_mean_revenue = one_order_value / len(one_order_customers)
repeat_order_mean_revenue = repeat_order_value / len(repeat_customers)

print("\n--- Revenue per Customer ---")
print("One-order customers:", one_order_mean_revenue)
print("Repeat customers:", repeat_order_mean_revenue)

# Mean order value

one_order_mean_order_value = one_order["payment_value"].mean()
repeat_order_mean_order_value = repeat_order["payment_value"].mean()

print("\n--- Mean Order Value ---")
print("One-order customers:", one_order_mean_order_value)
print("Repeat customers:", repeat_order_mean_order_value)

# Average number of orders among repeat customers

repeat_mean_order_quantity = orders_per_customer[
    orders_per_customer > 1
].mean()

print("\nAverage orders per repeat customer:", repeat_mean_order_quantity)

# Customer counts

total_customers = len(orders_per_customer)

print("\n--- Customer Counts ---")
print("Customers with one order:", len(one_order_customers))
print("Repeat customers:", len(repeat_customers))
print("Total customers:", total_customers)

# Repeat customer percentages

repeat_customer_percentage = len(repeat_customers) / total_customers * 100

repeat_customer_revenue_percentage = (
    repeat_order_value / customer_orders["payment_value"].sum() * 100
)

print("\nPercentage of repeat customers:", repeat_customer_percentage)
print(
    "Percentage of revenue from repeat customers:",
    repeat_customer_revenue_percentage,
)

# Validate order uniqueness after the customer merge

duplicate_orders = customer_orders["order_id"].duplicated().sum()
unique_orders = customer_orders["order_id"].nunique()
total_customer_order_rows = len(customer_orders)
order_uniqueness_check = (
    duplicate_orders == 0
    and unique_orders == total_customer_order_rows
)

print("\n--- Order Uniqueness Check ---")
print("Duplicated order IDs:", duplicate_orders)
print("Unique orders:", unique_orders)
print("Total rows:", total_customer_order_rows)
print("Order uniqueness check:", order_uniqueness_check)

# 9. Customer frequency analysis

customers_by_order_count = (
    orders_per_customer
    .value_counts()
    .sort_index()
)

customer_order_frequency = (
    orders_per_customer
    .rename("order_count")
    .reset_index()
)

customer_orders_analysis = customer_orders.merge(
    customer_order_frequency,
    on="customer_unique_id",
    how="left",
)

# Revenue by customer order frequency

revenue_by_order_frequency = (
    customer_orders_analysis
    .groupby("order_count")["payment_value"]
    .sum()
)

# Revenue per customer

revenue_per_customer = (
    customer_orders_analysis
    .groupby(["customer_unique_id", "order_count"])["payment_value"]
    .sum()
    .reset_index()
)

# Mean revenue per customer by order frequency

mean_revenue_by_order_frequency = (
    revenue_per_customer
    .groupby("order_count")["payment_value"]
    .mean()
)

# Percentage of customers by order frequency

percentage_of_customers = (
    customers_by_order_count / total_customers * 100
)

# Percentage of revenue by order frequency

total_customer_revenue = customer_orders_analysis["payment_value"].sum()

percentage_of_revenue = (
    revenue_by_order_frequency / total_customer_revenue * 100
)

# Final customer frequency analysis

customer_frequency_analysis = pd.DataFrame({
    "customer_count": customers_by_order_count,
    "percentage_of_customers": percentage_of_customers,
    "total_revenue": revenue_by_order_frequency,
    "percentage_of_revenue": percentage_of_revenue,
    "mean_revenue_per_customer": mean_revenue_by_order_frequency,
})

print("\n--- Customer Frequency Analysis ---")
print(customer_frequency_analysis)

# 10. Region performance

# Revenue generated by each state

revenue_by_state = (
    customer_orders
    .groupby("customer_state")["payment_value"]
    .sum()
    .sort_values(ascending=False)
)

customers_by_state = (
    customer_orders
    .groupby("customer_state")["customer_unique_id"]
    .nunique()
    .sort_values(ascending=False)
)

# Number of orders in each state

orders_by_state = (
    customer_orders
    .groupby("customer_state")["order_id"]
    .nunique()
    .sort_values(ascending=False)
)

# Average revenue generated by each customer in each state

mean_revenue_by_state = (
    revenue_by_state / customers_by_state
).sort_values(ascending=False)

# Average value of an order in each state

mean_order_value_by_state = (
    customer_orders
    .groupby("customer_state")["payment_value"]
    .mean()
    .sort_values(ascending=False)
)

# Count orders with a non-missing payment value for a consistent denominator
orders_with_payment_by_state = (
    customer_orders
    .groupby("customer_state")["payment_value"]
    .count()
)

mean_order_value_by_state_check = (
    revenue_by_state / orders_with_payment_by_state
)

order_value_differences = (
    mean_order_value_by_state.sort_index()
    - mean_order_value_by_state_check.sort_index()
).abs()

order_value_check = order_value_differences.lt(1e-8).all()

print("\n--- Revenue by State ---")
print(revenue_by_state)

print("\n--- Unique Customers by State ---")
print(customers_by_state)

print("\n--- Orders by State ---")
print(orders_by_state)

print("\n--- Mean Revenue per Customer by State ---")
print(mean_revenue_by_state)

print("\n--- Mean Order Value by State ---")
print(mean_order_value_by_state)

print("\nOrder value calculation check:", order_value_check)
print("Maximum difference between calculations:", order_value_differences.max())

# 11. Customer frequency by state

orders_per_customer_state = (
    customer_orders
    .groupby(["customer_state", "customer_unique_id"])["order_id"]
    .nunique()
    .rename("order_count")
    .reset_index()
)

# Average number of orders per customer in each state

mean_orders_per_customer_by_state = (
    orders_per_customer_state
    .groupby("customer_state")["order_count"]
    .mean()
    .sort_values(ascending=False)
)

print("\n--- Mean Orders per Customer by State ---")
print(mean_orders_per_customer_by_state)


# 12. Logistics performance

# Convert delivery dates to datetime
orders_payments_reviews["order_delivered_carrier_date"] = pd.to_datetime(
    orders_payments_reviews["order_delivered_carrier_date"]
)

orders_payments_reviews["order_delivered_customer_date"] = pd.to_datetime(
    orders_payments_reviews["order_delivered_customer_date"]
)

orders_payments_reviews["order_estimated_delivery_date"] = pd.to_datetime(
    orders_payments_reviews["order_estimated_delivery_date"]
)

# Calculate delivery time in days
orders_payments_reviews["carrier_to_customer_days"] = (
    orders_payments_reviews["order_delivered_customer_date"]
    - orders_payments_reviews["order_delivered_carrier_date"]
).dt.days

print("\n--- Carrier-to-Customer Delivery Time ---")
print("Mean days:", orders_payments_reviews["carrier_to_customer_days"].mean())

# Calculate difference between actual and estimated delivery dates
orders_payments_reviews["delivery_date_difference_days"] = (
    orders_payments_reviews["order_delivered_customer_date"]
    - orders_payments_reviews["order_estimated_delivery_date"]
).dt.days

print("\n--- Difference Between Actual and Estimated Delivery ---")
print("Negative = early; zero = on time; positive = delayed")

# Count deliveries by estimated delivery date
after_estimated_date = (
    orders_payments_reviews["delivery_date_difference_days"] > 0
).sum()

before_estimated_date = (
    orders_payments_reviews["delivery_date_difference_days"] < 0
).sum()

at_estimated_date = (
    orders_payments_reviews["delivery_date_difference_days"] == 0
).sum()

on_time_orders = orders_payments_reviews[
    orders_payments_reviews["delivery_date_difference_days"] <= 0
]

print("\n--- Delivery Status Counts ---")
print("After estimated date:", after_estimated_date)
print("Before estimated date:", before_estimated_date)
print("At estimated date:", at_estimated_date)

# Calculate percentage of delayed deliveries
total_delivered_orders = (
    orders_payments_reviews["delivery_date_difference_days"].notna().sum()
)

percentage_delayed = (
    after_estimated_date
    / total_delivered_orders
) * 100

print("\n--- Delayed Deliveries ---")
print("Total deliveries with valid dates:", total_delivered_orders)
print("Percentage of delayed deliveries:", percentage_delayed)

# Calculate average delay in days
delayed_orders = orders_payments_reviews[
    orders_payments_reviews["delivery_date_difference_days"] > 0
]

mean_delay_days = delayed_orders["delivery_date_difference_days"].mean()

print("\n--- Mean Delay in Days ---")
print(mean_delay_days)

mean_review_on_time_orders = on_time_orders["review_score"].mean()

mean_review_delayed_orders = delayed_orders["review_score"].mean()

print("\n--- Review Scores by Delivery Punctuality ---")
print("On-time or early average review score:", mean_review_on_time_orders)
print("Delayed average review score:", mean_review_delayed_orders)
print("On-time or early reviews:", on_time_orders["review_score"].count())
print("Delayed reviews:", delayed_orders["review_score"].count())

median_delivery_time = orders_payments_reviews["carrier_to_customer_days"].median()
max_delivery_time = orders_payments_reviews["carrier_to_customer_days"].max()

print("\n--- Delivery Time Distribution ---")
print("Median carrier-to-customer days:", median_delivery_time)
print("Maximum carrier-to-customer days:", max_delivery_time)