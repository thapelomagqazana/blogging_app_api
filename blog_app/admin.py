from django.contrib import admin
from.models import Post

# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at", "updated_at", "is_published")
    list_filter = ("is_published", "created_at")
    search_fields = ("title", "content")
