TODO LATER:
- Name shows None when not set - user must input a name at initial setup

# when order is processed (status decides what to do):
- order_status = is_enabled, paid_status, status
- when paid in full: order_status = False, True, Fullfilled (7) => 1 document + 1 payment
- when not paid and customer received the items:
    order_status = True, False, To be paid later (4) => 1 document + 0 payment
- when partially paid (multiple payments created):
    order_status =  True, False, Partially paid (5)
                    => 1 document + multiple payment (for each payment or payment_type)

- orders will be filtered by status:
    - if fullfilled or cancelled: the orders will be filtered (status.ordinal < 7)