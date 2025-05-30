from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Collection

class inlineUser(admin.TabularInline):
    model = Collection
    fields = ['name', 'lang']
    extra = 0

class UserAdmin(admin.ModelAdmin):
    inlines = [inlineUser]

admin.site.register(Collection)
admin.site.unregister(get_user_model())
admin.site.register(get_user_model(), UserAdmin)