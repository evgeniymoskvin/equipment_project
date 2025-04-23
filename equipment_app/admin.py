from django.contrib import admin

# Register your models here.
from .models import EquipmentModel, EquipmentSpecificationsModel, TypeOfEquipmentModel, TypeOfCoreModel, \
    TypeOfHardDiskModel, TypeOfVideoCardModel, TypeOfRAMModel, EquipmentEmployeeModel


class EquipmentSpecificationsAdmin(admin.ModelAdmin):
    ordering = ['equipment_type', 'equipment_specifications_name']
    search_fields = ["equipment_specifications_name"]
    list_filter = ("equipment_type", "core", "ram", 'video_card', 'disk', 'diagonal', 'type_of_print', 'paper_format',
                   'count_ethernet_ports')
    list_display = ('equipment_type', 'equipment_specifications_name', 'description')


class EquipmentAdmin(admin.ModelAdmin):
    ordering = ['equipment_type', 'equipment_spec', 'equipment_name', 'equipment_model', 'equipment_serial_number']
    search_fields = ["equipment_name", "equipment_serial_number", "equipment_inventory_number", "barcode"]
    list_filter = ["equipment_model", "equipment_type", "equipment_spec"]
    list_display = ('equipment_type', 'equipment_name', 'equipment_model', 'equipment_spec', 'equipment_serial_number',
                    'equipment_inventory_number', 'barcode', 'description')


class TypeOfEquipmentAdmin(admin.ModelAdmin):
    ordering = ['equipment_type_name']


class TypeOfCoreAdmin(admin.ModelAdmin):
    ordering = ['core_name']
    search_fields = ['core_name']
    list_filter = ['count_of_core', 'core_frequency', 'core_manufacturer']
    list_display = ('core_name', 'count_of_core', 'core_frequency', 'core_manufacturer')


class TypeOfHardDiskAdmin(admin.ModelAdmin):
    ordering = ['type_disk', 'disk_memory_size', 'disk_manufacturer', 'disk_interface']
    list_filter = ['type_disk', 'disk_memory_size', 'disk_manufacturer', 'disk_interface']
    search_fields = ['type_disk', 'disk_memory_size', 'disk_manufacturer', 'disk_interface']
    list_display = ('type_disk', 'disk_memory_size', 'disk_manufacturer', 'disk_interface')


class TypeOfVideoCardAdmin(admin.ModelAdmin):
    ordering = ['video_card_name', 'video_card_memory_size']
    search_fields = ['video_card_name', 'video_card_memory_size']
    list_filter = ['video_card_memory_size']
    list_display = ['video_card_name', 'video_card_memory_size']


class TypeOfRAMAdmin(admin.ModelAdmin):
    ordering = ['ram_type_name', 'ram_memory_size', 'ram_memory_standard']
    search_fields = ['ram_type_name', 'ram_memory_size', 'ram_memory_standard', 'ram_manufacturer']
    list_filter = ['ram_manufacturer', 'ram_frequency', 'ram_memory_size', 'ram_memory_standard']
    list_display = ('ram_type_name', 'ram_memory_size', 'ram_frequency', 'ram_manufacturer', 'ram_memory_standard')


class EquipmentEmployeeAdmin(admin.ModelAdmin):
    ordering = ['emp']
    search_fields = ['emp__last_name', 'equipment__equipment_serial_number', 'equipment__equipment_inventory_number',
                     'equipment__barcode', 'equipment__equipment_name', 'room']
    list_display = ('emp', 'equipment', 'room')
    list_filter = ['room']
    raw_id_fields = ['equipment', ]


admin.site.register(EquipmentSpecificationsModel, EquipmentSpecificationsAdmin)
admin.site.register(EquipmentModel, EquipmentAdmin)
admin.site.register(TypeOfEquipmentModel, TypeOfEquipmentAdmin)
admin.site.register(TypeOfCoreModel, TypeOfCoreAdmin)
admin.site.register(TypeOfHardDiskModel, TypeOfHardDiskAdmin)
admin.site.register(TypeOfVideoCardModel, TypeOfVideoCardAdmin)
admin.site.register(TypeOfRAMModel, TypeOfRAMAdmin)
admin.site.register(EquipmentEmployeeModel, EquipmentEmployeeAdmin)
