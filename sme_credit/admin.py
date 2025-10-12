from django.contrib import admin
from .models import BorrowerApplication
from .models import BorrowerApplication
from .models import BorrowerApplication

@admin.register(BorrowerApplication)
class BorrowerApplicationAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        return False


