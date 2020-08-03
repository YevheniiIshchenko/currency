from django.urls import path

from rate import views

app_name = 'rate'

urlpatterns = [
    path('show/', views.RateListView.as_view(), name='show-rate'),
    path('download-xlsx/', views.RateDownloadCSV.as_view(), name='download-csv'),
]
