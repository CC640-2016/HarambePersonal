from django.conf.urls import url

from . import views

app_name = 'polls'
urlpatterns = [
    url(r'^create_task$', views.create_task, name='create_task'),
    url(r'^save_task$', views.save_task, name='save_task'),
    url(r'^task_list$', views.list_tasks, name='task_list'),
    url(r'^delete_task/(?P<task_id>[0-9]+)$', views.delete_task, name='delete_task'),
]