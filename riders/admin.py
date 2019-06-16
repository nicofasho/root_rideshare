from django.contrib import admin
from .models import Profile, Route, Location, Car

#extra includes to make Profile admin console work
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


# Register your models here.
admin.site.register(Route)
admin.site.register(Location)
admin.site.register(Car)

#Profile admin stuff

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )
    list_display = ('username', 'email', 'first_name', 'last_name', 'picture', 'employer', 'isDriver')
    list_select_related = ('profile', )

    def picture(self, instance):
        return instance.profile.picture
    picture.short_description = 'Picture'

    def employer(self, instance):
        return instance.profile.employer
    employer.short_description = 'Employer'

    def isDriver(self, instance):
        return instance.profile.isDriver
    isDriver.short_description = 'isDriver'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)