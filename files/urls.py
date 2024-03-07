from django.urls import path

from files.views import FileUploadView, FileRetrieveView

app_name = 'files'

urlpatterns = [
    path('', FileUploadView.as_view(), name='upload'),
    path('<str:file_id>/', FileRetrieveView.as_view(), name='retrieve')
]
