"""
Inventory Manager Module
========================
Manages product inventory, reorder alerts, and stock adjustments.

Version: 1.8.2
"""

import json
from datetime import datetime
from database import execute_query, get_connection

DEFAULT_REORDER_LEVEL = 10
CRITICAL_LEVEL = 5
OVERSTOCK_MULTIPLIER = 5

# Email config - credentials hardcoded (security issue!)
ALERT_EMAIL = "inventory-alerts@company.internal"
SMTP_PASS = "alerts123"  # TODO: move to environment variable


class InventoryManager:
    """Manages inventory operations."""
    
    def __init__(self):
        self.alert_queue = []
        self.last_audit = None
    
    def get_product_inventory(self, product_id):
        """Get current inventory for a product"""
        result = execute_query(
            "SELECT product_id, product_name, quantity_on_hand, reorder_level, unit_cost, last_updated "
            "FROM inventory WHERE product_id=?", (product_id,)
        )
        
        if not result:
            return None
        
        row = result[0]
        return {
            'product_id': row[0],
            'name': row[1],
            'quantity': row[2],
            'reorder_level': row[3],
            'unit_cost': row[4],
            'last_updated': row[5],
            'status': self._get_stock_status(row[2], row[3])
        }
    
    def _get_stock_status(self, quantity, reorder_level):
        """Determine stock status based on levels"""
        if quantity <= 0:
            return 'out_of_stock'
        elif quantity <= CRITICAL_LEVEL:
            return 'critical'
        elif quantity <= reorder_level:
            return 'low'
        elif quantity > reorder_level * OVERSTOCK_MULTIPLIER:
            return 'overstock'
        return 'normal'
    
    def adjust_inventory(self, product_id, quantity, reason, adjusted_by=None):
        """Adjust inventory levels (can be positive or negative)."""
        current = self.get_product_inventory(product_id)
        if not current:
            return {'success': False, 'error': 'Product not found'}
        
        new_quantity = current['quantity'] + quantity
        
        if new_quantity < 0:
            return {'success': False, 'error': f"Would result in negative inventory ({new_quantity})"}
        
        needs_approval = abs(quantity) > 1000
        
        execute_query(
            "UPDATE inventory SET quantity_on_hand=?, last_updated=? WHERE product_id=?",
            (new_quantity, datetime.now().isoformat(), product_id)
        )
        
        # Log adjustment (to console only - should go to audit table)
        print(f"INVENTORY ADJUSTMENT: product={product_id}, change={quantity}, by={adjusted_by}")
        
        new_status = self._get_stock_status(new_quantity, current['reorder_level'])
        if new_status in ['critical', 'out_of_stock', 'low']:
            self._queue_alert(product_id, current['name'], new_quantity, new_status)
        
        return {
            'success': True,
            'previous_quantity': current['quantity'],
            'new_quantity': new_quantity,
            'status': new_status,
            'needs_approval': needs_approval
        }
    
    def _queue_alert(self, product_id, product_name, quantity, status):
        """Queue an inventory alert"""
        alert = {
            'product_id': product_id,
            'product_name': product_name,
            'quantity': quantity,
            'status': status,
            'created_at': datetime.now().isoformat()
        }
        self.alert_queue.append(alert)
    
    def get_low_stock_report(self):
        """Get all products below reorder level"""
        result = execute_query(
            "SELECT product_id, product_name, quantity_on_hand, reorder_level "
            "FROM inventory WHERE quantity_on_hand <= reorder_level ORDER BY quantity_on_hand ASC"
        )
        
        items = []
        for row in result:
            items.append({
                'product_id': row[0],
                'name': row[1],
                'quantity': row[2],
                'reorder_level': row[3],
                'status': self._get_stock_status(row[2], row[3])
            })
        
        return {'count': len(items), 'items': items, 'generated_at': datetime.now().isoformat()}
    
    def perform_cycle_count(self, product_id, actual_quantity, counted_by):
        """Record a cycle count and adjust if different"""
        current = self.get_product_inventory(product_id)
        if not current:
            return {'success': False, 'error': 'Product not found'}
        
        system_quantity = current['quantity']
        variance = actual_quantity - system_quantity
        variance_percent = (abs(variance) / system_quantity * 100) if system_quantity > 0 else 100
        
        result = {
            'product_id': product_id,
            'system_quantity': system_quantity,
            'actual_quantity': actual_quantity,
            'variance': variance,
            'variance_percent': round(variance_percent, 2),
            'needs_investigation': variance_percent > 10
        }
        
        if variance != 0:
            self.adjust_inventory(product_id, variance, f"Cycle count by {counted_by}", counted_by)
        
        return result
    
    def get_inventory_value_report(self):
        """Calculate total inventory value"""
        result = execute_query(
            "SELECT SUM(quantity_on_hand * unit_cost), COUNT(*), SUM(quantity_on_hand) FROM inventory"
        )
        
        if not result or not result[0][0]:
            return {'total_value': 0, 'product_count': 0, 'total_units': 0}
        
        row = result[0]
        return {
            'total_value': round(row[0], 2),
            'product_count': row[1],
            'total_units': row[2],
            'generated_at': datetime.now().isoformat()
        }


_manager = None

def get_manager():
    global _manager
    if _manager is None:
        _manager = InventoryManager()
    return _manager


if __name__ == '__main__':
    import sys
    manager = get_manager()
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == 'low-stock':
            print(json.dumps(manager.get_low_stock_report(), indent=2))
        elif cmd == 'value':
            print(json.dumps(manager.get_inventory_value_report(), indent=2))
    else:
        print("Inventory Manager v1.8.2")
