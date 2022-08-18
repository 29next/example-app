from django.contrib import admin

from .models import Store, StoreUser


class StoreUserInline(admin.TabularInline):
    raw_id_fields = ['user']
    model = StoreUser
    extra = 1


class StoreUserAdmin(admin.ModelAdmin):
    raw_id_fields = ['user', 'store']
    list_display = ['user', 'store']

admin.site.register(StoreUser, StoreUserAdmin)


class StoreAdmin(admin.ModelAdmin):
    search_fields = ['reference_id']
    list_filter = ['status']
    list_display = ['reference_id', 'status']

    inlines = [StoreUserInline]


admin.site.register(Store, StoreAdmin)
