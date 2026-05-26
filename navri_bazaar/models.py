# navri_bazaar/models.py
from django.db import models

class MarketFeedback(models.Model):
    INDUSTRY_CHOICES = [
        ('clothing', 'Clothing Store'),
        ('accessories', 'Accessories Store'),
        ('crm', 'CRM Management'),
        ('web_dev', 'Web Development'),
        ('events', 'Event Planning'),
        ('dating', 'Dates Planner'),
        ('other', 'Other'),
    ]

    user_guess = models.TextField()
    industry_sector = models.CharField(max_length=50, choices=INDUSTRY_CHOICES)
    other_sector = models.CharField(max_length=150, blank=True, null=True) # <-- New Field
    user_city = models.CharField(max_length=100)
    user_email = models.EmailField(unique=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_email} - {self.industry_sector}"