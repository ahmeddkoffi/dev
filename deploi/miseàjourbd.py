import os
import csv
import django
from decimal import Decimal  # Don't forget to import Decimal
from datetime import datetime

# Set the correct path to your Django project's settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "deploi.settings")
django.setup()

# Now you can import your Django models
from myapp.models import Events

csv_file_path = r"Classeur1.csv"

with open(csv_file_path, 'r') as file:
    csv_reader = csv.reader(file, delimiter = ';')
    next(csv_reader)  # Skip header row
    
    for row in csv_reader:
        print(row)
        if not row[1]:
            continue
        start_date_str, price_str = row
        start_date = datetime.strptime(start_date_str, '%d/%m/%Y')
        price = Decimal(price_str.replace(',', '.'))
        
        event = Events(start_date=start_date, price=price)
        event.save()
