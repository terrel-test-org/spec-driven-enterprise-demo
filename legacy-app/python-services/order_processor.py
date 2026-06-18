"""
Order Processing Module
=======================
Handles order lifecycle: creation, validation, fulfillment, and status updates.

NOTE: This module was written in 2016 and has been patched many times.
Some business rules may conflict with current policies.

Last major update: 2019
"""

import json
import time
from datetime import datetime, timedelta
from database import insert_order, get_customer_orders, update_inventory, execute_query

# Configuration - hardcoded values that should be in config
MAX_ORDER_AMOUNT = 50000
RUSH_ORDER_THRESHOLD = 100  # Units
BULK_DISCOUNT_THRESHOLD = 1000
BULK_DISCOUNT_PERCENT = 15
TAX_RATE = 0.0825  # Should vary by state...

# Status constants - not used consistently throughout codebase
STATUS_PENDING = 'pending'
STATUS_CONFIRMED = 'confirmed'
STATUS_PROCESSING = 'processing'
STATUS_SHIPPED = 'shipped'
STATUS_DELIVERED = 'delivered'
STATUS_CANCELLED = 'cancelled'

class OrderProcessor:
    """
    Main order processing class.
    Handles business logic that was originally spread across multiple scripts.
    """
    
    def __init__(self):
        self.pending_orders = []  # In-memory queue - lost on restart!
        self.processed_today = 0
        self.errors = []
    
    def create_order(self, customer_id, items, shipping_info, options=None):
        """
        Create a new order.
        
        Business rules (some documented, some discovered through production issues):
        1. Validate customer exists and is active
        2. Check inventory for all items
        3. Apply discounts (bulk, promotional, loyalty)
        4. Calculate tax (simplified - just uses default rate)
        5. Create order record
        6. Reserve inventory
        7. Send notifications (currently broken - TODO fix)
        """
        options = options or {}
        
        # Validate items
        if not items or len(items) == 0:
            return {'success': False, 'error': 'No items in order'}
        
        # Check each item's inventory
        for item in items:
            inv_check = self._check_inventory(item['product_id'], item['quantity'])
            if not inv_check['available']:
                return {
                    'success': False, 
                    'error': f"Insufficient inventory for product {item['product_id']}"
                }
        
        # Calculate pricing
        subtotal = 0
        processed_items = []
        for item in items:
            item_total = item['unit_price'] * item['quantity']
            
            # Apply bulk discount - undocumented business rule
            if item['quantity'] >= BULK_DISCOUNT_THRESHOLD:
                item['discount'] = BULK_DISCOUNT_PERCENT
                item_total *= (1 - BULK_DISCOUNT_PERCENT/100)
            
            subtotal += item_total
            processed_items.append(item)
        
        # Check max order amount
        if subtotal > MAX_ORDER_AMOUNT:
            return {
                'success': False,
                'error': f'Order amount ${subtotal:.2f} exceeds maximum ${MAX_ORDER_AMOUNT}'
            }
        
        # Calculate tax - should use shipping address state
        tax = subtotal * TAX_RATE
        total = subtotal + tax
        
        # Add rush fee if applicable
        if options.get('rush_delivery'):
            total_units = sum(i['quantity'] for i in items)
            if total_units > RUSH_ORDER_THRESHOLD:
                return {
                    'success': False,
                    'error': 'Rush delivery not available for orders over 100 units'
                }
            rush_fee = 50.00  # Flat fee
            total += rush_fee
        
        # Create the order
        order_id, error = insert_order(
            customer_id, 
            processed_items,
            json.dumps(shipping_info) if isinstance(shipping_info, dict) else shipping_info
        )
        
        if error:
            return {'success': False, 'error': error}
        
        # Reserve inventory
        for item in processed_items:
            success, err = update_inventory(item['product_id'], item['quantity'], 'subtract')
            if not success:
                # Rollback logic was never fully implemented
                self.errors.append(f"Inventory update failed for order {order_id}: {err}")
        
        # Add to processing queue
        self.pending_orders.append({
            'order_id': order_id,
            'created_at': datetime.now(),
            'priority': options.get('priority', 0)
        })
        
        self.processed_today += 1
        
        return {
            'success': True,
            'order_id': order_id,
            'subtotal': subtotal,
            'tax': tax,
            'total': total
        }
    
    def _check_inventory(self, product_id, quantity):
        """Check if sufficient inventory exists"""
        result = execute_query(
            "SELECT quantity_on_hand FROM inventory WHERE product_id=?",
            (product_id,)
        )
        if not result:
            return {'available': False, 'message': 'Product not found'}
        
        on_hand = result[0][0]
        return {
            'available': on_hand >= quantity,
            'on_hand': on_hand,
            'requested': quantity
        }
    
    def process_pending_orders(self):
        """
        Process all pending orders in queue.
        Called by cron job every 5 minutes (see /etc/cron.d/order_processor)
        """
        processed = 0
        failed = 0
        
        # Sort by priority - higher priority first
        self.pending_orders.sort(key=lambda x: x.get('priority', 0), reverse=True)
        
        for order in self.pending_orders[:]:  # Copy list to allow modification
            try:
                result = self._process_single_order(order['order_id'])
                if result['success']:
                    self.pending_orders.remove(order)
                    processed += 1
                else:
                    failed += 1
            except Exception as e:
                self.errors.append(f"Error processing order {order['order_id']}: {str(e)}")
                failed += 1
        
        return {'processed': processed, 'failed': failed}
    
    def _process_single_order(self, order_id):
        """Process a single order - update status, trigger fulfillment"""
        result = execute_query(
            "SELECT status, customer_id, total_amount FROM orders WHERE id=?",
            (order_id,)
        )
        
        if not result:
            return {'success': False, 'error': 'Order not found'}
        
        status, customer_id, total = result[0]
        
        if status == 'pending_approval':
            return {'success': False, 'error': 'Awaiting manual approval'}
        
        execute_query(
            "UPDATE orders SET status=?, updated_at=? WHERE id=?",
            (STATUS_PROCESSING, datetime.now().isoformat(), order_id)
        )
        
        time.sleep(0.5)  # Simulate processing
        
        execute_query(
            "UPDATE orders SET status=?, updated_at=? WHERE id=?",
            (STATUS_SHIPPED, datetime.now().isoformat(), order_id)
        )
        
        return {'success': True, 'order_id': order_id}
    
    def cancel_order(self, order_id, reason=None):
        """Cancel an order and restore inventory"""
        result = execute_query("SELECT status FROM orders WHERE id=?", (order_id,))
        
        if not result:
            return {'success': False, 'error': 'Order not found'}
        
        current_status = result[0][0]
        
        if current_status not in [STATUS_PENDING, STATUS_CONFIRMED, 'pending_approval']:
            return {'success': False, 'error': f'Cannot cancel order in {current_status} status'}
        
        items = execute_query("SELECT product_id, quantity FROM order_items WHERE order_id=?", (order_id,))
        
        for product_id, quantity in items:
            update_inventory(product_id, quantity, 'add')
        
        execute_query(
            "UPDATE orders SET status=?, notes=?, updated_at=? WHERE id=?",
            (STATUS_CANCELLED, f"Cancelled: {reason or 'No reason provided'}", 
             datetime.now().isoformat(), order_id)
        )
        
        return {'success': True}
    
    def get_order_status(self, order_id):
        """Get current order status with details"""
        result = execute_query("SELECT * FROM orders WHERE id=?", (order_id,))
        
        if not result:
            return None
        
        order = result[0]
        items = execute_query("SELECT * FROM order_items WHERE order_id=?", (order_id,))
        
        return {
            'order_id': order[0],
            'customer_id': order[1],
            'date': order[2],
            'status': order[3],
            'total': order[4],
            'priority': order[8],
            'items': [{'product_id': i[2], 'quantity': i[4], 'price': i[5]} for i in items]
        }


# Singleton instance
_processor = None

def get_processor():
    global _processor
    if _processor is None:
        _processor = OrderProcessor()
    return _processor


if __name__ == '__main__':
    import sys
    processor = get_processor()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == 'process':
            result = processor.process_pending_orders()
            print(f"Processed: {result['processed']}, Failed: {result['failed']}")
        elif command == 'status' and len(sys.argv) > 2:
            status = processor.get_order_status(int(sys.argv[2]))
            print(json.dumps(status, indent=2))
        elif command == 'report':
            print("Daily report not implemented")
    else:
        print("Order Processor v2.3.1 (legacy)")
