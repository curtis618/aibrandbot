from django.contrib import admin
from .models import Activity

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('name', 'end_date', 'location', 'description', 'image_url', 'activity_link')
    search_fields = ('name', 'location')
