# Migration Guide: HTMX Views to Item Views

This guide shows how to migrate from the old function-based views in `htmx_views.py` to the new class-based views in `item_views.py`.

## New Item Update Views

The following new views have been created in `src/pos2/views/item_views.py`:

### 1. UpdateItemQuantityView
- **Purpose**: Update item quantity with a specific value
- **URL**: `update/item-quantity/<order_number>/<item_number>/`
- **URL Name**: `pos2:update-item-quantity`
- **Form Fields**: `['quantity']`
- **Replaces**: `change_quantity` function in htmx_views.py

### 2. AddItemQuantityView
- **Purpose**: Add 1 to item quantity
- **URL**: `add/item-quantity/<order_number>/<item_number>/`
- **URL Name**: `pos2:add-item-quantity`
- **Replaces**: `add_quantity` function in htmx_views.py

### 3. SubtractItemQuantityView
- **Purpose**: Subtract 1 from item quantity (deletes if quantity becomes 0)
- **URL**: `subtract/item-quantity/<order_number>/<item_number>/`
- **URL Name**: `pos2:subtract-item-quantity`
- **Replaces**: `subtract_quantity` function in htmx_views.py

### 4. UpdateItemDiscountView
- **Purpose**: Update item discount and discount type
- **URL**: `update/item-discount/<order_number>/<item_number>/`
- **URL Name**: `pos2:update-item-discount`
- **Form Fields**: `['discount', 'discount_type']`
- **Replaces**: `item_discount` function in htmx_views.py

### 5. DeleteItemView
- **Purpose**: Delete an item from the order
- **URL**: `delete/item/<order_number>/<item_number>/`
- **URL Name**: `pos2:delete-item`
- **Replaces**: `remove_item` and `delete_order_item_with_no_response` functions in htmx_views.py

## Migration Examples

### Old HTMX Function-Based Approach:
```python
# In htmx_views.py
def change_quantity(request, item_number):
    item = get_object_or_404(PosOrderItem, number=item_number)
    quantity = request.POST.get("display", None)
    if quantity:
        item.quantity = quantity
        item.save()
    # ... render logic
```

### New Class-Based Approach:
```python
# In item_views.py
class UpdateItemQuantityView(AddOrderItemMixin, View):
    form_fields = ['quantity']
    template_name = active_order_template
    
    def post(self, request, **kwargs):
        # Handles both order_number and item_number from URL
        # Uses mixin methods for consistent behavior
        # Automatically refreshes order cache
        # Returns full order context targeting #pos element
```

## Key Benefits of Migration

1. **Consistent URL Structure**: All views now use both `order_number` and `item_number`
2. **Unified Template**: All views render `active_order_template` targeting `#pos` element
3. **Form Field Specification**: Views can specify which fields they handle via `form_fields`
4. **Mixin Reuse**: All views use `AddOrderItemMixin` for consistent behavior
5. **Automatic Cache Refresh**: Order calculations are automatically updated
6. **Better Error Handling**: Form validation and error handling built-in

## Template Integration

All new views render the same template (`active_order_template`) and target the `#pos` HTML element, ensuring consistent UI updates across all item operations.

## Next Steps

1. Update frontend HTMX calls to use the new URL patterns
2. Test each view to ensure proper functionality
3. Remove deprecated functions from `htmx_views.py` once migration is complete
4. Update any documentation or API references