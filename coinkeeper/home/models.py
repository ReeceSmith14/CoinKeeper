from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone

# Create your models here.

#Extend the built in user model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    
    def __str__(self):
        return self.user.username


class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    source = models.CharField(max_length=100)  # e.g., salary, freelance, etc.
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_received = models.DateField()

    def __str__(self):
        return f"{self.source} - {self.amount}"

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)  # e.g., grocery, rent, subscription
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    is_recurring = models.BooleanField(default=False)
    card_used = models.CharField(max_length=100, null=True, blank=True)  # e.g., "Visa", "MasterCard"
    payment_expiry_date = models.DateField(null=True, blank=True)  # Only relevant if recurring
    
    def __str__(self):
        return f"{self.description} - {self.amount}"

#Category for the income/expense
class Category(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name


class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=100)  # e.g., "groceries", "entertainment"
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # budget limit
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"Budget for {self.category}: {self.amount}"


class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    report_type = models.CharField(max_length=100)  # e.g., "monthly", "yearly", "custom"
    generated_on = models.DateTimeField(auto_now_add=True)
    content = models.TextField()  # Store the report data (optional)

    def __str__(self):
        return f"Report {self.report_type} generated on {self.generated_on}"


class Subscription(models.Model):
    PLAN_CHOICES = [
        ('FREE', 'Free'),
        ('PREMIUM', 'Premium'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    plan = models.CharField(max_length=10, choices=PLAN_CHOICES, default='FREE')
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.plan}"

    def activate(self, plan='PREMIUM', duration_days=30):
        self.plan = plan
        self.start_date = timezone.now()
        self.end_date = self.start_date + timedelta(days=duration_days)
        self.is_active = True
        self.save()

    def deactivate(self):
        self.plan = 'FREE'
        self.is_active = False
        self.end_date = None
        self.save()

    @property
    def has_active_subscription(self):
        # Check if the subscription is currently active
        if self.end_date and self.end_date > timezone.now():
            return True
        return False


