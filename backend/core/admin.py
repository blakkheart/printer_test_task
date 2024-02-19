from django.contrib import admin

from core.models import Printer, Check


@admin.register(Printer)
class PrinterAdmin(admin.ModelAdmin):
    pass


@admin.register(Check)
class CheckAdmin(admin.ModelAdmin):
    list_filter = ['printer_id', 'type', 'status']
