from src.accounts.admin.admin_customer import INITIAL_DATA
from src.accounts.models import Customer, User
import random
import string

def generate_random_name(first_names, second_names):
    first_name = random.choice(first_names)
    last_name = random.choice(second_names)
    while last_name == first_name:  # Ensure first and last names are not the same
        last_name = random.choice(second_names)
    return first_name, last_name

def generate_code(name, phone):
    return f"{name[0][0]}{name[1][0]}-{phone[-4:]}"

def generate_address(apartments, area_info):
    apartment = random.choice(apartments)
    apartments.remove(apartment)  # Ensure unique apartment numbers
    return f"{area_info}, Apt {apartment}"

def generate_email(first_name, last_name):
    return f"{first_name.lower()}.{last_name.lower()}@email.com"

def generate_phone(country_code, area_codes, start_range, end_range):
    area_code = random.choice(area_codes)
    third_part = random.randint(start_range, end_range)
    last_part = random.randint(1000, 9999)
    return f"{country_code}-{area_code}-{third_part}-{last_part}"

def create_fake_customers(first_names, second_names, apartments, area_info, country_code, area_codes, start_range, end_range, num_customers):
    customers = []
    for _ in range(num_customers):
        first_name, last_name = generate_random_name(first_names, second_names)
        phone = generate_phone(country_code, area_codes, start_range, end_range)
        address = generate_address(apartments, area_info)
        email = generate_email(first_name, last_name)
        code = generate_code((first_name, last_name), phone)
        customer = {
            'name': f"{first_name} {last_name}",
            'code': code,
            'address': address,
            'email': email,
            'phone': phone,
            'is_customer': True,
            'is_supplier': False,
            'is_enabled': True
        }
        customers.append(customer)
    return customers

# Example usage:
first_names = [
    "Rawand", "Sazan", "Rezan", "Daban", "Sakar", "Shaswar", 
    "Shirin", "Sarwar", "Dana", "Darya","Nare", "Saya", "Shalaw", 
    "Shapol", "Mohammed", 
    # Male Names (25)
    "Aram", "Diyar", "Baran", "Dara", "Hawar",
    "Roj", "Zanyar", "Shvan", "Dilshad", "Kawa",
    "Rojhat", "Bakir", "Soran", "Berzan", "Diyari",
    "Heval", "Karwan", "Nazhad", "Rebin", "Sipan",
    "Tarik", "Xebat", "Yadgar", "Zardasht", "Hemn",
    
    # Female Names (25)
    "Ava", "Dilan", "Jiyan", "Rozh", "Shiler",
    "Berivan", "Darya", "Hana", "Khanzad", "Lina",
    "Miya", "Nishtiman", "Pelin", "Rojin", "Shno",
    "Tara", "Viyan", "Xezal", "Zara", "Avesta",
    "Binevsh", "Daryan", "Gulistan", "Havin", "Rengin"
]
second_names = ["Mustafa", "Abdulla", "Mohammed", "Ali", "Khalid", "Sabah","Mahmoud"]
apartments = [f"{i}" for i in range(1, 101)]  # 100 unique apartments
area_info = "Iraq, Slemani, Raparrin"
country_code = "+964"
area_codes = ["770", "771", "772", "773", "774", "775"]
start_range = 450
end_range = 950








def initial_data():
    fake_customers = create_fake_customers(first_names, second_names, apartments, area_info, country_code, area_codes, start_range, end_range, 65)
    for index, cus in enumerate(fake_customers):
        customer = Customer.objects.filter(email=cus['email']).first()
        if not customer:
            user = User.objects.get(email='root@root.com')
            customer = Customer(**cus)
            customer.user = user
            customer.save(force_insert=True)
            print(f"Fake customer: {index} created successfully.")
        else:
            customer.code = cus['code']
            customer.save(force_update=True)



def run():
    initial_data()
