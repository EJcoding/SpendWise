from django.db import models

# Create your models here.
class Expense(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    amount = models.FloatField(null=True)
    budget = models.FloatField(null=True)

    def __str__(self):
        return f"Expense: {self.name}, {self.category}, ${self.amount:.2f}"
    
    
from django.db import models

class Budget(models.Model):
    amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Budget: ${self.amount:.2f} (Created at: {self.created_at})"

