from django.conf.urls import url

from . import views

app_name = 'polls'
urlpatterns = [
    url(r'^create_task$', views.create_task, name='create_task')
]