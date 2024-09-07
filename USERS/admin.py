from django.contrib import admin
from .models import HomeOwner, Resident

# Register your models here.
class HomeOwnerAdmin(admin.ModelAdmin):
	exclude = ('password',)

admin.site.register(HomeOwner, HomeOwnerAdmin)


admin.site.register(Resident)
