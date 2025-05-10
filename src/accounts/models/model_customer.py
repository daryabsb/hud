from django.db import models
from django.core.cache import cache
from src.accounts.models import User
from src.core.modules import upload_image_file_path
from src.accounts import cache_key as ck # CUSTOMER_LIST, USER_CUSTOMER_LIST

CACHE_TIMEOUT = 604800  # 1 week

def get_customers_from_db(user=None, is_customer=True, is_supplier=False):
    customers = Customer.objects.filter(is_enabled=True, is_customer=is_customer, is_supplier=is_supplier)

    if user and not (user.is_staff or user.is_superuser):
        customers = customers.filter(user=user)
        
    customer_list = []

    for customer in customers:
        customer_data = {
            "id": customer.id,
            "code": customer.code,
            "name": customer.name,
            "address": customer.address,
            "postal_code": customer.postal_code,
            "city": customer.city,
            "tax_number": customer.tax_number,
            "email": customer.email,
            "phone": customer.phone,
            "is_customer": customer.is_customer,
            "is_supplier": customer.is_supplier,
            "due_date_period": customer.due_date_period,
            "image": customer.image,
            "created": customer.created,
            "updated": customer.updated,
        }
        customer_list.append(customer_data)
    return customer_list

def get_customers(user=None, is_supplier=False, refresh=False):
    if user and not (user.is_staff or user.is_superuser):
        cache_key = ck.USER_CUSTOMERS_LIST % user.id
    else:
        cache_key = ck.CUSTOMERS_LIST
    
    if refresh:
        print(f"1 - Cache miss, fetching customers from DB - refresh: {refresh}")
        customers = get_customers_from_db(user=user, is_customer=True, is_supplier=False)
        cache.set(cache_key, customers, CACHE_TIMEOUT)
    else:
        customers = cache.get(cache_key)

        if customers is None:
            print("2 - Cache miss, fetching customers DB")
            customers = get_customers_from_db(user=user, is_customer=True, is_supplier=False)
            cache.set(cache_key, customers, CACHE_TIMEOUT)
    return customers

def get_suppliers(user=None, is_supplier=True, refresh=False):
    if user and not (user.is_staff or user.is_superuser):
        cache_key = ck.USER_SUPPLIERS_LIST % user.id
    else:
        cache_key = ck.SUPPLIERS_LIST

    if refresh:
        print(f"1 - Cache miss, fetching customers from DB - refresh: {refresh}")
        suppliers = get_customers_from_db(user=user, is_customer=False, is_supplier=True)
        cache.set(cache_key, suppliers, CACHE_TIMEOUT)
        
        if suppliers is None:
            print("2 - Cache miss, fetching customers DB")
            suppliers = get_customers_from_db(user=user, is_customer=False, is_supplier=True)
            cache.set(cache_key, suppliers, CACHE_TIMEOUT)

    return suppliers

def refresh_customer_cache(user=None):
    get_customers(user=user, refresh=True)
    get_suppliers(user=user, refresh=True)

        
class Customer(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="customers")
    code = models.CharField(max_length=30, null=True, blank=True)
    name = models.CharField(max_length=100, unique=True)
    address = models.CharField(max_length=300, null=True, blank=True)
    postal_code = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    # country = models.ForeignKey(
    #     "Country", default=1, on_delete=models.CASCADE, related_name="customers"
    # )
    tax_number = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    is_enabled = models.BooleanField(default=True)
    is_customer = models.BooleanField(default=True)
    is_supplier = models.BooleanField(default=False)
    due_date_period = models.SmallIntegerField(default=0)
    image = models.ImageField(
        null=True, blank=True, default='user.png',
        upload_to=upload_image_file_path)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ('id',)


class CustomerDiscount(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="customer_discounts"
    )
    customer = models.ForeignKey(
        "Customer", on_delete=models.CASCADE, related_name="discounts"
    )
    type = models.SmallIntegerField(default=0)
    uid = models.SmallIntegerField(default=0)
    value = models.FloatField(default=0)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["customer", "type", "uid"], name="unique_customer_discounts"
            )
        ]

    def __str__(self):
        return f"{self.customer.name} - {self.type} | {self.uid}"

    def generate_code(name, phone):
        return f"{name[0][0]}{name[1][0]}-{phone[-4:]}"
    
    def save(self, *args, **kwargs):
        if self.code is None:
            self.code = self.generate_code(self.name, self.phone)

        # self.update_items_subtotal()
        super().save(*args, **kwargs)
        self.refresh_cache()  # <-- parentheses to call it

    def refresh_cache(self):
        refresh_customer_cache(user=self.user)