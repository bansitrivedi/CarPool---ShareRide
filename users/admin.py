from django.contrib import admin
from .models import Profile
from django.contrib.auth.admin import UserAdmin
from .models import User
# Register your models here.


# admin.site.register(User)
admin.site.register(Profile)



from django.forms import TextInput, Textarea
from django.db import models
class UserModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'20'})},
        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40})},
    }

admin.site.register(User, UserModelAdmin)