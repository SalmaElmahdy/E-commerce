from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import Account


class AccountAdmin(UserAdmin):
    # make those fields displayed on accounts dashboard
    list_display=['email','first_name','last_name','username','last_login','date_joined','is_active']
    # make those fields clickable
    list_display_links=('email','first_name','last_name')
    
    readonly_fields=('last_login','date_joined')
    # show in dsc order
    ordering=('-date_joined',)
    filter_horizontal=()
    list_filter=()
    fieldsets=() # make password read only
    
# Register your models here.
admin.site.register(Account,AccountAdmin)

