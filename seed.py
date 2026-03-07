import random
from faker import Faker
from datetime import datetime

fake = Faker()

# Adjust these if your app names are different
USER_TABLE = "core_user" 
CUSTOMER_TABLE = "store_customer"

NUM_CUSTOMERS = 1000
NUM_ADDRESSES = 1000
NUM_PROMOTIONS = 50
NUM_COLLECTIONS = 50
NUM_PRODUCTS = 1000
NUM_ORDERS = 200
MAX_ITEMS_PER_ORDER = 20

sql_lines = []

# 1. Users & Customers (Linked 1-to-1)
for i in range(1, NUM_CUSTOMERS + 1):
    # Create User Entry
    username = fake.unique.user_name()
    first_name = fake.first_name().replace("'", "")
    last_name = fake.last_name().replace("'", "")
    email = fake.unique.email()
    password = "pbkdf2_sha256$600000$encryptedpassword" # Dummy hash
    
    sql_lines.append(
        f"INSERT INTO {USER_TABLE} (id, password, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) "
        f"VALUES ({i}, '{password}', 0, '{username}', '{first_name}', '{last_name}', '{email}', 0, 1, NOW());"
    )

    # Create Customer Entry (linked to User ID)
    phone = fake.phone_number()
    birth_date = fake.date_of_birth(minimum_age=18, maximum_age=65)
    membership = random.choice(['B', 'S', 'G'])
    sql_lines.append(
        f"INSERT INTO {CUSTOMER_TABLE} (phone, birth_date, membership, user_id) "
        f"VALUES ('{phone}', '{birth_date}', '{membership}', {i});"
    )

# 2. Addresses
for i in range(1, NUM_ADDRESSES + 1):
    street = fake.street_address().replace("'", "")
    city = fake.city().replace("'", "")
    zip_code = fake.postcode()
    customer_id = random.randint(1, NUM_CUSTOMERS)
    sql_lines.append(
        f"INSERT INTO store_address (street, city, zip, customer_id) "
        f"VALUES ('{street}', '{city}', '{zip_code}', {customer_id});"
    )

# 3. Promotions
for i in range(1, NUM_PROMOTIONS + 1):
    desc = fake.catch_phrase().replace("'", "")
    discount = round(random.uniform(0.05, 0.5), 2)
    sql_lines.append(
        f"INSERT INTO store_promotion (id, description, discount) "
        f"VALUES ({i}, '{desc}', {discount});"
    )

# 4. Collections
for i in range(1, NUM_COLLECTIONS + 1):
    title = fake.word().capitalize()
    sql_lines.append(
        f"INSERT INTO store_collection (id, title, featured_product_id) "
        f"VALUES ({i}, '{title}', NULL);"
    )

# 5. Products
for i in range(1, NUM_PRODUCTS + 1):
    title = fake.word().capitalize()
    slug = f"{title.lower()}-{i}"
    description = fake.text(max_nb_chars=200).replace("'", "")
    unit_price = round(random.uniform(5.0, 2000.0), 2)
    inventory = random.randint(1, 100)
    collection_id = random.randint(1, NUM_COLLECTIONS)
    sql_lines.append(
        f"INSERT INTO store_product (id, title, slug, description, unit_price, inventory, last_update, collection_id) "
        f"VALUES ({i}, '{title}', '{slug}', '{description}', {unit_price}, {inventory}, NOW(), {collection_id});"
    )

# 6. Product ↔ Promotions (Many-to-Many)
seen_pairs = set()
for i in range(1, NUM_PRODUCTS + 1):
    promo_count = random.randint(0, 2)
    if promo_count > 0:
        chosen_promos = random.sample(range(1, NUM_PROMOTIONS + 1), promo_count)
        for promotion_id in chosen_promos:
            sql_lines.append(
                f"INSERT INTO store_product_promotions (product_id, promotion_id) "
                f"VALUES ({i}, {promotion_id});"
            )

# 7. Orders
for i in range(1, NUM_ORDERS + 1):
    placed_at = fake.date_time_this_year()
    payment_status = random.choice(['P', 'C', 'F'])
    customer_id = random.randint(1, NUM_CUSTOMERS)
    sql_lines.append(
        f"INSERT INTO store_order (id, placed_at, payment_status, customer_id) "
        f"VALUES ({i}, '{placed_at}', '{payment_status}', {customer_id});"
    )

# 8. OrderItems (Fixed typo: 'quantiy')
for i in range(1, NUM_ORDERS + 1):
    num_items = random.randint(1, MAX_ITEMS_PER_ORDER)
    chosen_products = random.sample(range(1, NUM_PRODUCTS + 1), num_items)
    for product_id in chosen_products:
        quantity = random.randint(1, 5)
        unit_price = round(random.uniform(5.0, 2000.0), 2)
        sql_lines.append(
            f"INSERT INTO store_orderitem (order_id, product_id, quantiy, unit_price) "
            f"VALUES ({i}, {product_id}, {quantity}, {unit_price});"
        )

# Save to file
with open("seed.sql", "w") as f:
    f.write("SET FOREIGN_KEY_CHECKS = 0;\n") # Faster & prevents order issues
    f.write("\n".join(sql_lines))
    f.write("\nSET FOREIGN_KEY_CHECKS = 1;")

print("✅ seed.sql generated with User/Customer link and OrderItem typo fix!")
