from django.contrib import admin
from django.contrib.auth.models import User

from .models import Job, History, Status, Address
from accounts.models import Profile

# Register your models here.
class HistoryInline(admin.TabularInline):
    model = History
    extra = 1

class UserInline(admin.StackedInline):
    model = User
    can_delete = False

class JobAdmin(admin.ModelAdmin):
    model = Job
    list_display = ('get_user_profile', 'entry_date', 'product', 'problem')
    list_editable = ['problem']
    readonly_fields = ['entry_date']
    
    search_fields = ['user__username','product']
    list_filter = ['entry_date']
    
    inlines = [HistoryInline]
    
    def get_user_profile(self, obj):
        return Profile.objects.get(user=obj.user)
    get_user_profile.short_description = 'User'

class AddressAdmin(admin.ModelAdmin):
    model = Address
    list_display = ('id','full_name')

admin.site.register(Status)
admin.site.register(Job,JobAdmin)
admin.site.register(Address,AddressAdmin)
