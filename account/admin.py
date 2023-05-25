from django.contrib import admin
from account.models import User

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email','username','first_name','last_name','is_superuser','is_staff','is_email_verified']