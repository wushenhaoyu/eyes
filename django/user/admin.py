from django.contrib import admin
from .models import Doctor,Patient,Hospital,MedicalRecords,HistoryRecords

# Register your models here.
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Hospital)
admin.site.register(MedicalRecords)
admin.site.register(HistoryRecords)