import pandas as pd

customers = pd.read_csv("data/raw/olist_customers_dataset.csv")
geolocation = pd.read_csv("data/raw/olist_geolocation_dataset.csv")
order_items = pd.read_csv("data/raw/olist_order_items_dataset.csv")
order_payments = pd.read_csv("data/raw/olist_order_payments_dataset.csv")
order_reviews = pd.read_csv("data/raw/olist_order_reviews_dataset.csv")
orders = pd.read_csv("data/raw/olist_orders_dataset.csv")
products = pd.read_csv("data/raw/olist_products_dataset.csv")
sellers = pd.read_csv("data/raw/olist_sellers_dataset.csv")
product_category_name_translation = pd.read_csv("data/raw/product_category_name_translation.csv")

datasets = {
    "customers": customers,
    "geolocation": geolocation,
    "order_items": order_items,
    "order_payments": order_payments,
    "order_reviews": order_reviews,
    "orders": orders,
    "products": products,
    "sellers": sellers,
    "product_category_name_translation": product_category_name_translation
}

for name, df in datasets.items():
    print(name, "\n")
    print("Shape:\n", df.shape, "\n")
    print("Columns:\n", df.columns, "\n")
    print("Column types:\n", df.dtypes, "\n")
    print("Missing Values:\n", df.isna().sum(), "\n")
    print("Duplicated Values:\n", df.duplicated().sum(), "\n")

print("--- Key analysis ---\n")
print(customers["customer_id"].nunique())
print(orders["order_id"].nunique())
print(products["product_id"].nunique())
print(sellers["seller_id"].nunique())
print(order_items["order_id"].nunique())
print(order_items["product_id"].nunique())
print(order_items["seller_id"].nunique())

items_per_order = order_items.groupby(order_items["order_id"]).size()

print("Greatest number of items in an order:", items_per_order.max())
print("Orders with multiple items:", (items_per_order > 1).sum())
print("Mean number of items per order:", items_per_order.mean())

payments_per_order = order_payments.groupby(order_payments["order_id"]).size()

print("Unique orders with payments:", payments_per_order.count())
print("Total payment records:", order_payments["order_id"].count())
print("Orders with multiple payments:", (payments_per_order > 1).sum())

reviews_per_order = order_reviews.groupby(order_reviews["order_id"]).size()

print("Unique orders with reviews:", reviews_per_order.count())
print("Total review records:", order_reviews["order_id"].count())
print("Orders with multiple reviews:", (reviews_per_order > 1).sum())