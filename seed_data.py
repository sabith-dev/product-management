import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Category, Product

categories = ['Electronics', 'Books', 'Clothing']
objs = [Category.objects.get_or_create(name=c) for c in categories]
cat_objs = [o[0] for o in objs]

sample = [
    ('Wireless Mouse', 'ELEC-001', 0, 29.99, 45),
    ('Mechanical Keyboard', 'ELEC-002', 0, 89.99, 12),
    ('USB-C Hub', 'ELEC-003', 0, 39.99, 3),      # low stock
    ('Django for Beginners', 'BOOK-001', 1, 24.50, 30),
    ('Python Cookbook', 'BOOK-002', 1, 45.00, 0),  # out of stock
    ('T-Shirt (M)', 'CLOT-001', 2, 15.99, 100),
]

for name, sku, cat_idx, price, stock in sample:
    Product.objects.get_or_create(
        sku=sku,
        defaults={'name': name, 'category': cat_objs[cat_idx], 'price': price, 'stock': stock},
    )

print('Seeded successfully!')
