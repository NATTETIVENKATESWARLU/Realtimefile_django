from django.contrib import admin
from db.models.asset import Asset
from db.models.employee import Employee
from db.models.assignment_log import AssetAssignmentLog



admin.site.register(Asset)
admin.site.register(Employee)
admin.site.register(AssetAssignmentLog)