from django.contrib import admin

# Register your models here.

from .models import Node_Data,Node_Relations

class NodeDataAdmin(admin.ModelAdmin):
    list_display = ["__unicode__","group","updated"]
    # list_display = []
    class Meta:
        model = Node_Data


class NodeRelAdmin(admin.ModelAdmin):
    list_display = ["source","target","value"]
    class Meta:
        model = Node_Relations

admin.site.register(Node_Relations,NodeRelAdmin)
admin.site.register(Node_Data,NodeDataAdmin)