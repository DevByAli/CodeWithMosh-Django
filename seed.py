import random
from faker import Faker
from datetime import datetime

fake = Faker()

NUM_CUSTOMERS = 1000
NUM_ADDRESSES = 1000
NUM_PROMOTIONS = 50
NUM_COLLECTIONS = 50
NUM_PRODUCTS = 1000
NUM_ORDERS = 200
MAX_ITEMS_PER_ORDER = 20

sql_lines = []

# Customers
for i in range(1, NUM_CUSTOMERS + 1):
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = fake.unique.email()
    phone = fake.phone_number()
    birth_date = fake.date_of_birth(minimum_age=18, maximum_age=65)
    membership = random.choice(['B', 'S', 'G'])
    sql_lines.append(
        f"INSERT INTO store_customer (first_name, last_name, email, phone, birth_date, membership) "
        f"VALUES ('{first_name}', '{last_name}', '{email}', '{phone}', '{birth_date}', '{membership}');"
    )

# Addresses
for i in range(1, NUM_ADDRESSES + 1):
    street = fake.street_address().replace("'", "")
    city = fake.city().replace("'", "")
    zip_code = fake.postcode()
    customer_id = random.randint(1, NUM_CUSTOMERS)
    sql_lines.append(
        f"INSERT INTO store_address (street, city, zip, customer_id) "
        f"VALUES ('{street}', '{city}', '{zip_code}', {customer_id});"
    )

# Promotions
for i in range(1, NUM_PROMOTIONS + 1):
    desc = fake.catch_phrase().replace("'", "")
    discount = round(random.uniform(0.05, 0.5), 2)
    sql_lines.append(
        f"INSERT INTO store_promotion (description, discount) "
        f"VALUES ('{desc}', {discount});"
    )

# Collections
for i in range(1, NUM_COLLECTIONS + 1):
    title = fake.word().capitalize()
    sql_lines.append(
        f"INSERT INTO store_collection (title, featured_product_id) "
        f"VALUES ('{title}', NULL);"
    )

# Products
for i in range(1, NUM_PRODUCTS + 1):
    title = fake.word().capitalize()
    slug = f"{title.lower()}-{i}"
    description = fake.text(max_nb_chars=200).replace("'", "")
    unit_price = round(random.uniform(5.0, 2000.0), 2)
    inventory = random.randint(1, 100)
    collection_id = random.randint(1, NUM_COLLECTIONS)
    sql_lines.append(
        f"INSERT INTO store_product (title, slug, description, unit_price, inventory, last_update, collection_id) "
        f"VALUES ('{title}', '{slug}', '{description}', {unit_price}, {inventory}, NOW(), {collection_id});"
    )

# Product ↔ Promotions (Many-to-Many)
seen_pairs = set()

for i in range(1, NUM_PRODUCTS + 1):
    promo_count = random.randint(0, 2)  # 0-2 promotions per product
    chosen_promos = random.sample(range(1, NUM_PROMOTIONS + 1), promo_count)
    for promotion_id in chosen_promos:
        pair = (i, promotion_id)
        if pair not in seen_pairs:
            seen_pairs.add(pair)
            sql_lines.append(
                f"INSERT INTO store_product_promotions (product_id, promotion_id) "
                f"VALUES ({i}, {promotion_id});"
            )

# Orders
for i in range(1, NUM_ORDERS + 1):
    placed_at = fake.date_time_this_year()
    payment_status = random.choice(['P', 'C', 'F'])  # Pending, Complete, Failed
    customer_id = random.randint(1, NUM_CUSTOMERS)
    sql_lines.append(
        f"INSERT INTO store_order (placed_at, payment_status, customer_id) "
        f"VALUES ('{placed_at}', '{payment_status}', {customer_id});"
    )

# OrderItems
order_item_id = 1
for order_id in range(1, NUM_ORDERS + 1):
    num_items = random.randint(1, MAX_ITEMS_PER_ORDER)
    chosen_products = random.sample(range(1, NUM_PRODUCTS + 1), num_items)
    for product_id in chosen_products:
        quantity = random.randint(1, 5)
        unit_price = round(random.uniform(5.0, 2000.0), 2)
        sql_lines.append(
            f"INSERT INTO store_orderitem (order_id, product_id, quantiy, unit_price) "
            f"VALUES ({order_id}, {product_id}, {quantity}, {unit_price});"
        )
        order_item_id += 1


# Save to file
with open("seed.sql", "w") as f:
    f.write("-- AUTO-GENERATED SEED DATA\n")
    f.write(f"-- Generated at {datetime.now()}\n\n")
    f.write("\n".join(sql_lines))

print("✅ seed.sql generated successfully!")
