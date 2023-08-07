# myapp/models.py
from django.db import models

class Events(models.Model):
    start_date = models.DateTimeField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Event {self.id} - Start Date: {self.start_date}, Price: {self.price}"
