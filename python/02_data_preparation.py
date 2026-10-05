import pandas as pd

order_payments = pd.read_csv("data/raw/olist_order_payments_dataset.csv")

payments = order_payments.copy()

payments_aggregated = payments.groupby("order_id").agg({
    "payment_value": "sum",
    "payment_type": lambda x: " + ".join(x.unique())
})

print(payments_aggregated.shape)
print(payments_aggregated.index.nunique())
print(payments_aggregated["payment_value"].sum())

order_reviews = pd.read_csv("data/raw/olist_order_reviews_dataset.csv")

reviews = order_reviews.copy()

reviews_aggregated = reviews.groupby("order_id").agg({
    "review_score": "mean"
})

print(reviews_aggregated.shape)
print(reviews_aggregated.index.nunique())
print(reviews_aggregated["review_score"].describe())
print(reviews_aggregated["review_score"].isna().sum())

orders = pd.read_csv("data/raw/olist_orders_dataset.csv")

orders_payments = pd.merge(
    orders,
    payments_aggregated,
    on= "order_id",
    how="left"
)

print(orders.shape)
print(orders_payments.shape)
print(orders_payments["order_id"].nunique())

print(orders_payments["payment_value"].isna().sum())

print(orders_payments.head())

orders_payments_reviews = pd.merge(
    orders_payments,
    reviews_aggregated,
    on= "order_id",
    how= "left"
)

print(orders_payments_reviews.shape)
print(orders_payments_reviews["order_id"].nunique())
print(orders_payments_reviews["review_score"].isna().sum())
print(orders_payments_reviews["order_status"].value_counts())

orders_payments_reviews["no_review"] = orders_payments_reviews["review_score"].isna()
print(orders_payments_reviews.groupby("order_status")["no_review"].sum())

order_items = pd.read_csv("data/raw/olist_order_items_dataset.csv")

print(order_items[["price", "freight_value"]].dtypes)

products = pd.read_csv("data/raw/olist_products_dataset.csv")

products_selected = products[[
    "product_id",
    "product_category_name"
]]

order_products = pd.merge(
    order_items,
    products_selected, 
    on= "product_id", 
    how= "left"
)

print(order_products.shape)
print(order_products["order_id"].nunique())
print(order_products["product_category_name"].isna().sum())
print(order_products["product_id"].nunique())
print(order_products.head())

orders_payments_reviews.to_csv(
    "data/processed/orders_payments_reviews.csv",
    index=False
)

order_products.to_csv(
    "data/processed/order_products.csv",
    index=False
)