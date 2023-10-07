from django.contrib import admin
from .models import Tier, CustomUser
from django.contrib.auth.admin import UserAdmin


# Register your models here.
class TierAdmin(admin.ModelAdmin):
    model = Tier
    list_display = ('name',)

admin.site.register(Tier, TierAdmin)
admin.site.register(CustomUser)