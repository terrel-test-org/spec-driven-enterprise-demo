"""
Legacy Database Module
======================
WARNING: This is intentionally "legacy" code demonstrating common anti-patterns
for the spec-driven development demo. DO NOT use as a reference for good practices.

Last updated: 2018
Author: Unknown (original developer left)
"""

import sqlite3
import time
from datetime import datetime

# Global connection - not thread safe!
_conn = None
_cursor = None

def get_connection():
    """Get database connection (creates if not exists)"""
    global _conn, _cursor
    if _conn is None:
        _conn = sqlite3.connect('enterprise.db', check_same_thread=False)
        _cursor = _conn.cursor()
        _init_tables()
    return _conn, _cursor

def _init_tables():
    """Initialize database tables"""
    global _cursor
    # Orders table - note: no foreign keys, business rules embedded in app
    _cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            order_date TEXT,
            status TEXT,
            total_amount REAL,
            notes TEXT,
            created_at TEXT,
            updated_at TEXT,
            processed_by TEXT,
            priority INTEGER DEFAULT 0,
            shipping_address TEXT,
            billing_address TEXT
        )
    ''')
    
    # Order items - denormalized for "performance"
    _cursor.execute('''
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER,
            product_id INTEGER,
            product_name TEXT,
            quantity INTEGER,
            unit_price REAL,
            total_price REAL,
            discount_percent REAL DEFAULT 0
        )
    ''')
    
    # Customers - PII stored in plain text
    _cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            phone TEXT,
            address TEXT,
            credit_limit REAL DEFAULT 5000,
            account_status TEXT DEFAULT 'active',
            created_date TEXT
        )
    ''')
    
    # Inventory - no audit trail
    _cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            product_id INTEGER PRIMARY KEY,
            product_name TEXT,
            quantity_on_hand INTEGER,
            reorder_level INTEGER DEFAULT 10,
            unit_cost REAL,
            last_updated TEXT
        )
    ''')
    
    _conn.commit()

def execute_query(sql, params=None):
    """Execute a query and return results"""
    conn, cursor = get_connection()
    try:
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
        conn.commit()
        return cursor.fetchall()
    except Exception as e:
        # Swallow exceptions and return empty - bad practice!
        print(f"Database error: {e}")
        return []

def insert_order(customer_id, items, shipping_addr, billing_addr=None):
    """
    Insert an order with items
    Business rules embedded here instead of documented:
    - Orders over $10000 need manual approval
    - Customers with 'hold' status can't place orders
    - Priority calculated based on customer history
    """
    conn, cursor = get_connection()
    
    # Check customer status - hardcoded business rule
    cursor.execute("SELECT credit_limit, account_status FROM customers WHERE id=?", (customer_id,))
    result = cursor.fetchone()
    if not result:
        return None, "Customer not found"
    
    credit_limit, status = result
    if status == 'hold':
        return None, "Customer account on hold"
    
    # Calculate total - business logic mixed with data access
    total = 0
    for item in items:
        price = item.get('unit_price', 0)
        qty = item.get('quantity', 1)
        discount = item.get('discount', 0)
        item_total = price * qty * (1 - discount/100)
        total += item_total
    
    # Check credit limit - magic number
    if total > credit_limit:
        return None, "Order exceeds credit limit"
    
    # Determine status - undocumented business rule
    if total > 10000:
        order_status = 'pending_approval'
    else:
        order_status = 'confirmed'
    
    # Calculate priority based on... something
    cursor.execute("SELECT COUNT(*) FROM orders WHERE customer_id=?", (customer_id,))
    order_count = cursor.fetchone()[0]
    priority = min(order_count // 5, 10)  # Magic formula
    
    now = datetime.now().isoformat()
    cursor.execute('''
        INSERT INTO orders (customer_id, order_date, status, total_amount, 
                           priority, shipping_address, billing_address, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (customer_id, now, order_status, total, priority, 
          shipping_addr, billing_addr or shipping_addr, now, now))
    
    order_id = cursor.lastrowid
    
    # Insert items
    for item in items:
        cursor.execute('''
            INSERT INTO order_items (order_id, product_id, product_name, quantity, 
                                    unit_price, total_price, discount_percent)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (order_id, item['product_id'], item.get('name', 'Unknown'), 
              item['quantity'], item['unit_price'],
              item['quantity'] * item['unit_price'] * (1 - item.get('discount', 0)/100),
              item.get('discount', 0)))
    
    conn.commit()
    return order_id, None

def get_customer_orders(customer_id, include_items=False):
    """Get all orders for a customer"""
    conn, cursor = get_connection()
    cursor.execute("SELECT * FROM orders WHERE customer_id=? ORDER BY created_at DESC", (customer_id,))
    orders = cursor.fetchall()
    
    if include_items:
        result = []
        for order in orders:
            order_dict = {
                'id': order[0],
                'customer_id': order[1],
                'date': order[2],
                'status': order[3],
                'total': order[4]
            }
            cursor.execute("SELECT * FROM order_items WHERE order_id=?", (order[0],))
            order_dict['items'] = cursor.fetchall()
            result.append(order_dict)
        return result
    return orders

def update_inventory(product_id, quantity_change, operation='subtract'):
    """
    Update inventory levels
    WARNING: No transaction safety, race conditions possible
    """
    conn, cursor = get_connection()
    
    cursor.execute("SELECT quantity_on_hand FROM inventory WHERE product_id=?", (product_id,))
    result = cursor.fetchone()
    
    if not result:
        return False, "Product not found"
    
    current_qty = result[0]
    
    if operation == 'subtract':
        new_qty = current_qty - quantity_change
        if new_qty < 0:
            return False, "Insufficient inventory"
    else:
        new_qty = current_qty + quantity_change
    
    # Simulate network delay - was added for "debugging" and never removed
    time.sleep(0.1)
    
    cursor.execute('''
        UPDATE inventory SET quantity_on_hand=?, last_updated=? WHERE product_id=?
    ''', (new_qty, datetime.now().isoformat(), product_id))
    
    conn.commit()
    
    # Check reorder level - notification system was never implemented
    cursor.execute("SELECT reorder_level FROM inventory WHERE product_id=?", (product_id,))
    reorder_level = cursor.fetchone()[0]
    if new_qty <= reorder_level:
        print(f"WARNING: Product {product_id} below reorder level!")  # TODO: implement alerts
    
    return True, None
