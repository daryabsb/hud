To improve your POS system's design, we need to address the key issues you've identified:

1. **Handling partial and split payments** for orders.
2. **Supporting multiple document types** (e.g., Sales, Purchase, Proforma) with flexible payment scenarios, including delayed or split payments for purchases.
3. Ensuring the system is robust and scalable for different workflows (e.g., POS sales vs. vendor purchases).

Below, I’ll propose a revised approach to your system’s design, focusing on flexibility, clarity, and scalability. I’ll describe the changes to your models, workflows, and logic, and explain how they address the problems. I’ll also provide a high-level implementation guide.

---

### Revised System Design

#### Key Improvements

1. **Decouple Orders and Documents**: Treat `PosOrder` as a temporary entity for the POS workflow (e.g., sales in progress) and `Document` as the final record of a transaction (e.g., Invoice, Purchase, Proforma). This allows flexibility for non-POS workflows like purchases.
2. **Support Multiple Payments per Document**: Modify the `Payment` model to support partial and split payments explicitly, with a clear link to the associated document.
3. **Flexible Document Creation**: Allow documents to be created independently of orders for non-POS scenarios (e.g., purchases, inventory counts) and support delayed or split payments.
4. **Track Payment Status Dynamically**: Instead of a boolean `paid_status` on `Document`, calculate the payment status based on the sum of associated payments compared to the document’s total.
5. **Enhance Document Types**: Use `DocumentType` to control workflows (e.g., stock movements, payment requirements) and ensure the system can handle diverse scenarios.

---

### Revised Models

#### 1. DocumentType Model

Your existing `DocumentType` list is well-structured but can be enhanced to include additional metadata to control workflows. For example:

- Add a field `requires_payment` (boolean) to indicate whether a document type requires immediate payment (e.g., Sales) or allows delayed payments (e.g., Purchase, Proforma).
- Add a field `is_pos_related` (boolean) to indicate whether the document type is tied to the POS workflow.

Example `DocumentType` schema (conceptual):

```python
class DocumentType(models.Model):
    name = models.CharField(max_length=50)  # e.g., Sales, Purchase, Proforma
    code = models.CharField(max_length=10)  # e.g., 100, 200, 230
    category = models.SmallIntegerField()  # e.g., 1=Sales, 2=Purchase
    warehouse = models.ForeignKey(Warehouse, null=True, blank=True)
    stock_direction = models.SmallIntegerField()  # 1=In, 2=Out, 0=None
    editor_type = models.SmallIntegerField(default=0)
    print_template = models.CharField(max_length=50)
    price_type = models.SmallIntegerField()  # 0=None, 1=SalePrice, 2=PurchasePrice
    language = models.CharField(max_length=10, blank=True)
    requires_payment = models.BooleanField(default=True)  # Immediate payment required?
    is_pos_related = models.BooleanField(default=False)  # Tied to POS workflow?
```

#### 2. Document Model

The `Document` model is the core record of a transaction. Key changes:

- Remove `paid_status` and compute it dynamically by comparing `total` to the sum of associated `Payment` amounts.
- Add a `status` field to track the document’s lifecycle (e.g., Draft, Open, Paid, Closed).
- Allow `order` to be nullable for non-POS documents (e.g., purchases).

Revised `Document` model:

```python
class Document(models.Model):
    STATUS_CHOICES = (
        (0, 'Draft'),  # Document is being created
        (1, 'Open'),   # Document is finalized but not fully paid
        (2, 'Paid'),   # Document is fully paid
        (3, 'Closed'), # Document is archived/completed
    )

    number = models.CharField(max_length=30, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="documents")
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING, null=True, blank=True)
    cash_register = models.ForeignKey(CashRegister, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey('PosOrder', on_delete=models.SET_NULL, null=True, blank=True)
    document_type = models.ForeignKey(DocumentType, on_delete=models.DO_NOTHING)
    warehouse = models.ForeignKey(Warehouse, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    reference_document_number = models.CharField(max_length=100, unique=True)
    internal_note = models.TextField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    discount = models.FloatField(default=0)
    discount_type = models.SmallIntegerField(default=0)
    discount_apply_rule = models.SmallIntegerField(default=0)
    total = models.FloatField(default=0)
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=0)
    stock_date = models.DateTimeField(auto_now_add=True)
    is_clocked_out = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_payment_status(self):
        """Calculate if the document is fully paid."""
        total_paid = sum(payment.amount for payment in self.payments.all())
        return total_paid >= self.total
```

#### 3. Payment Model

The `Payment` model should support multiple payments per document and track payment methods explicitly. Add a `payment_date` to support delayed payments.

Revised `Payment` model:

```python
class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payments")
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="payments")
    payment_type = models.ForeignKey("PaymentType", on_delete=models.DO_NOTHING)
    amount = models.FloatField(default=0)
    payment_date = models.DateTimeField(auto_now_add=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
```

#### 4. PosOrder Model

The `PosOrder` model (assumed to be similar to `Document`) remains largely unchanged but is used only for POS-specific workflows. Key points:

- `PosOrder` is a temporary entity used during the POS sale process.
- When the order is finalized (e.g., customer pays), it converts to a `Document` with `document_type=Sales`.
- Add a `status` field to track whether the order is active, pending payment, or archived.

Example `PosOrder` schema (conceptual):

```python
class PosOrder(models.Model):
    STATUS_CHOICES = (
        (0, 'Active'),   # Order is being created
        (1, 'Pending'),  # Awaiting payment
        (2, 'Completed'),# Converted to Document
        (3, 'Archived'), # Disabled after completion
    )

    number = models.CharField(max_length=30, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING, null=True, blank=True)
    cash_register = models.ForeignKey(CashRegister, on_delete=models.SET_NULL, null=True, blank=True)
    document_type = models.ForeignKey(DocumentType, on_delete=models.DO_NOTHING, default=2)  # Default to Sales
    warehouse = models.ForeignKey(Warehouse, null=True, blank=True)
    total = models.FloatField(default=0)
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
```

#### 5. PaymentType Model (Assumed)

Ensure the `PaymentType` model supports various payment methods (e.g., Cash, Credit Card, Bank Transfer) and includes any necessary metadata (e.g., processing fees, reconciliation details).

---

### Revised Workflow

#### 1. POS Sales Workflow

- **Step 1: Create PosOrder**

  - A cashier creates a `PosOrder` with `document_type=Sales` (ID=2).
  - Add items to the order, calculate `total`.

- **Step 2: Process Payments**

  - The customer may pay fully or partially using one or more payment methods (e.g., $50 cash, $30 credit card).
  - For each payment, create a `Payment` record linked to the `PosOrder` (temporarily) with the appropriate `payment_type` and `amount`.

- **Step 3: Finalize Order**

  - When the customer completes payment (or partially pays), convert the `PosOrder` to a `Document`:
    - Create a `Document` with `document_type=Sales`, copying fields like `total`, `customer`, etc.
    - Link all `Payment` records to the new `Document`.
    - Set `PosOrder.status=Completed` and `PosOrder.archived=True`.
  - If partially paid, set `Document.status=Open`. If fully paid, set `Document.status=Paid`.
  - Generate an invoice (using `print_template=Invoice`).

- **Step 4: Activate Next Order**
  - If there are pending `PosOrder` records (e.g., `status=Active` or `Pending`), activate the next one. Otherwise, create a new `PosOrder`.

#### 2. Purchase Workflow

- **Step 1: Create Document Directly**

  - For purchases, skip `PosOrder` and create a `Document` with `document_type=Purchase` (ID=1).
  - Set `status=Draft` while adding items, then finalize to `status=Open`.
  - Record vendor details, items, and `total`.

- **Step 2: Process Payments**

  - Payments may be delayed or split (e.g., 50% now, 50% in 30 days).
  - Create one or more `Payment` records linked to the `Document`, each with `payment_type`, `amount`, and `payment_date`.

- **Step 3: Update Status**
  - Dynamically calculate if the `Document` is fully paid (`get_payment_status`).
  - If fully paid, set `Document.status=Paid`. If all processes are complete (e.g., goods received), set `status=Closed`.

#### 3. Other Document Types

- **Proforma, Refund, etc.**: Follow a similar process to Purchases. Create a `Document` directly with the appropriate `document_type`. Payments are optional if `requires_payment=False` (e.g., Proforma).
- **Inventory Count, Loss And Damage**: These may not involve payments. Create a `Document` with `stock_direction` to adjust inventory, set `status=Closed` once completed.

---

### Addressing the Problems

1. **Partial and Split Payments**

   - The revised `Payment` model supports multiple payments per `Document` or `PosOrder`.
   - The `get_payment_status` method dynamically checks if the document is fully paid, eliminating the need for a static `paid_status` field.
   - Example: A $100 sales order can have two `Payment` records ($60 cash, $40 credit card), and the system tracks the remaining balance.

2. **Support for Multiple Document Types**

   - By decoupling `PosOrder` (POS-specific) from `Document` (general transactions), the system supports non-POS workflows like purchases.
   - The `DocumentType` model’s `requires_payment` and `is_pos_related` fields guide the workflow, ensuring flexibility for purchases (delayed payments) vs. sales (immediate payments).
   - Example: A purchase `Document` can have multiple `Payment` records over time, and the system tracks the outstanding balance.

3. **Scalability and Clarity**
   - The `status` field on `Document` and `PosOrder` provides clear lifecycle tracking.
   - Dynamic payment status calculation simplifies maintenance and ensures accuracy.
   - The system supports diverse scenarios (e.g., refunds, inventory counts) without forcing them into the POS workflow.

---

“

System: ### Implementation Guide

#### 1. Update Database Models

- Modify the `Document` and `Payment` models as shown above.
- Add the `requires_payment` and `is_pos_related` fields to `DocumentType`.
- Ensure `PosOrder` has a `status` field and is linked to `Document` via a nullable foreign key.

#### 2. Implement Payment Logic

- Create a utility function to calculate payment status:
  ```python
  def calculate_document_status(document):
      total_paid = sum(payment.amount for payment in document.payments.all())
      document.status = 2 if total_paid >= document.total else 1  # Paid or Open
      document.save()
  ```
- Call this function after creating or updating `Payment` records.

#### 3. Revise POS Workflow

- Update the POS interface to allow multiple payment methods per order.
- When finalizing a `PosOrder`:
  - Create a `Document` with `document_type=Sales`.
  - Transfer `Payment` records from `PosOrder` to `Document`.
  - Archive the `PosOrder` and activate the next one.

#### 4. Support Non-POS Workflows

- Create a separate interface for creating `Document` records directly (e.g., for purchases).
- Allow users to specify `document_type`, items, and payment schedules.
- Update the payment interface to support adding multiple payments over time.

#### 5. Enhance Reporting

- Add reports to track:
  - Outstanding balances for `Document` records with `status=Open`.
  - Total payments by `payment_type` or `document_type`.
  - Profit margins for purchases vs. sales (using `price_type`).

#### 6. Testing and Validation

- Test partial payment scenarios (e.g., $50 now, $50 later).
- Test split payment scenarios (e.g., $30 cash, $70 credit card).
- Test non-POS workflows (e.g., creating a purchase `Document` with delayed payments).
- Ensure stock movements align with `stock_direction` for each `document_type`.

---

### Example Scenarios

#### Scenario 1: POS Sale with Split Payment

- Cashier creates a `PosOrder` with `total=$100`.
- Customer pays $60 cash, $40 credit card.
- System creates two `Payment` records linked to the `PosOrder`.
- On finalization, create a `Document` with `document_type=Sales`, transfer payments, set `Document.status=Paid`, and archive the `PosOrder`.

#### Scenario 2: Purchase with Delayed Payments

- Create a `Document` with `document_type=Purchase`, `total=$1000`.
- Vendor agrees to pay $500 now, $500 in 30 days.
- Create a `Payment` record for $500 now, set `Document.status=Open`.
- Later, add another `Payment` for $500, update `Document.status=Paid`.

#### Scenario 3: Proforma Invoice

- Create a `Document` with `document_type=Proforma`, `total=$200`, `requires_payment=False`.
- No payments are required; set `Document.status=Closed` after sending to the customer.

---

### Additional Recommendations

- **Audit Trail**: Add a `History` model to log changes to `Document` and `Payment` records for traceability.
- **Payment Schedules**: For purchases, add a `PaymentSchedule` model to track expected payment dates and amounts.
- **Error Handling**: Validate that the sum of `Payment` amounts does not exceed `Document.total`.
- **UI/UX**: Enhance the POS interface to clearly display partial payment status and allow easy addition of multiple payment methods.

This design provides a flexible, scalable solution that addresses your current problems while supporting diverse workflows. Let me know if you need help with specific code snippets, database migrations, or further clarification!
