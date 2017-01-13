from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Profile
# Register your models here.


# Define an inline admin descriptor for Profile model
# which acts a bit like a singleton
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, )


class MyUser(User):
    class Meta:
        proxy = True
    
    def get_fullname(self):
        return "%s %s" % (self.first_name, self.last_name)


class MyUserAdmin(admin.ModelAdmin):
    inlines = [ProfileInline]
    list_display = ('username', 'email' ,'get_fullname','get_company_name')
    search_fields = ['username','email','first_name']
    
#    fieldsets = (
#        ('User', {'fields':[ 'username', 'first_name', 'last_name', 'email']} ),
#        ('Profile',{'fields':['company_name','contact_number']}),
#        (None, {'fields':['groups']})
#    )
    
    def get_company_name(self, obj):
        return obj.profile.company_name
    

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(MyUser, MyUserAdmin)
