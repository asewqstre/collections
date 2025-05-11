from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Collection, Word

class inlineUser(admin.TabularInline):
    model = Collection
    fields = ['name', 'lang']
    extra = 0

class UserAdmin(admin.ModelAdmin):
    inlines = [inlineUser]

class inlineWord(admin.TabularInline):
    model = Word.collections.through
    extra = 0

class WordAdmin(admin.ModelAdmin):
    inlines = [inlineWord]

admin.site.register(Collection)
admin.site.unregister(get_user_model())
admin.site.register(get_user_model(), UserAdmin)
admin.site.register(Word, WordAdmin)
