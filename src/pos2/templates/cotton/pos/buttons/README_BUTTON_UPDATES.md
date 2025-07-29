# Button Template Updates

## Overview

This document describes the updates made to the button templates in the `cotton/pos/buttons` folder to standardize their behavior to update the `#pos` element directly, similar to how `order_status.html` works.

## Changes Made

### Button Templates Updated

The following button templates were updated to target the `#pos` element instead of their individual targets:

1. **Generic Button Templates**:
   - `generic_update_button.html` - Now targets `#pos` with `innerHTML` swap
   - `order_status.html` - Updated to use the generic order update view

2. **Specialized Button Templates in `pos/` directory**:
   - `comment.html` - Now targets `#pos` for note updates
   - `internal_note.html` - Now targets `#pos` for internal note updates
   - `discount.html` - Now targets `#pos` for discount updates
   - `customer.html` - Now targets `#pos` for customer updates
   - `delete.html` - Now targets `#pos` for status updates (void)
   - `lock.html` - Now targets `#pos` for lock status updates
   - `payment.html` - Now targets `#pos` for payment updates
   - `transfer.html` - Now targets `#pos` for transfer updates

### Example Templates Updated

The following example templates were also updated to reflect the new pattern:

1. `generic_update_example.html` - All buttons now target `#pos`
2. `inline_generic_update_example.html` - All forms now target `#pos`

## Implementation Details

### HTMX Attributes

Each button template now includes the following HTMX attributes:

```html
hx-get="{% url 'pos2:update-order-generic' active_order.number %}?fields=field1,field2"
hx-target="#pos"
hx-swap="innerHTML"
```

This ensures that when a button is clicked, it loads the appropriate form into the `#pos` element, replacing its entire content.

### Benefits

1. **Consistency** - All buttons now behave in the same way, updating the entire POS interface
2. **Simplified Code** - Uses the generic order update view for all button actions
3. **Improved UX** - Ensures the entire POS interface is refreshed after any action
4. **Maintainability** - Centralizes the update logic in one place

## Usage Example

To create a new button that updates specific fields:

```html
<div class="flex-fill" id="customButton">
    <a href="#modalCustom"
       class="w-100 pt-3 px-4 btn btn-outline-default rounded-2 mb-2"
       hx-get="{% url 'pos2:update-order-generic' active_order.number %}?fields=field1,field2"
       hx-target="#pos"
       hx-swap="innerHTML"
       data-bs-toggle="modal">
        <i class="fas fa-2xl fa-icon"></i><br>
        <span class="small">Button Label</span>
    </a>
</div>
```

Replace `field1,field2` with the specific fields you want to update.