from django.urls import path
from app import views

urlpatterns = [
    path('', views.index, name="index.html"),
    path('insert', views.insertData, name = "insertData"),
    path('update/<id>', views.updateData, name = "updateData"),
    path('delete/<id>', views.deleteData, name = "deleteData"),
    path('export-vcf/', views.export_vcf, name='export_vcf'),
    path('import-vcf/', views.import_vcf, name='import_vcf'),
    path('merge_contacts/', views.merge_contacts, name='merge_contacts'),
    path('merge/', views.merge_duplicate_contacts, name='merge_contacts'),

]

