from django.db import models
from django.core.exceptions import ValidationError

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    age = models.IntegerField()
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class TransactionHistory(models.Model):
    from_user = models.ForeignKey(
        User, related_name="from_user", on_delete=models.PROTECT
    )
    to_user = models.ForeignKey(User, related_name="to_user", on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.from_user == self.to_user:
            raise ValidationError("From user and To user cannot be the same.")
