from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import Account, UserProfile
from django.utils.html import format_html

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
    

class UserProfileAdmin(admin.ModelAdmin):
    def thumbnail(self,object):
        return format_html ('<img src="{}" width="30" style="border-radius:50%;" >'.format(object.profile_picture.url))
    
    thumbnail.short_description='profile picture'
    list_display=['thumbnail','user','city','state','country']
    
admin.site.register(Account,AccountAdmin)
admin.site.register(UserProfile,UserProfileAdmin)

