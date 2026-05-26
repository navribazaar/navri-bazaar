from django.contrib import admin
from .models import MarketFeedback

# Register your models here.
@admin.register(MarketFeedback)
class MarketFeedbackAdmin(admin.ModelAdmin):
    # This renders all key data fields as neat columns at a quick glance
    list_display = ('user_email', 'industry_sector', 'other_sector', 'user_city', 'submitted_at')
    
    # Adds an instantly clickable filter sidebar on the right
    list_filter = ('industry_sector', 'user_city')
    
    # Adds a powerful search bar at the top to look up users instantly
    search_fields = ('user_email', 'user_guess')