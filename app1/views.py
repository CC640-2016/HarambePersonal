from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .models import Task

# Create your views here.

def create_task(request):
    return render(request, 'create_task_view.html', {})

def save_task(request):
    description = request.POST.get('description')
    tasks_same_name = Task.objects.filter(description=description)
    if description != '' and len(tasks_same_name) == 0:
        task = Task(description=description)
        task.save()
    else:
        # tirar error
        pass
        
    return render(request, 'create_task_view.html', {})
    
def list_tasks(request):
    tasks = Task.objects.all()
    context = {'task_list' : tasks}
    return render(request, 'task_list.html', context)

    
def delete_task(request, task_id=None):
    tasks = Task.objects.all()
    context = {'task_list' : tasks}
    delete = Task.objects.get(pk=task_id).delete()
    return render(request, 'task_list.html', context)
    
def task_edition(request, task_id=None):
    task = Task.objects.all().filter(id=task_id)[0]
    context = {'task' : task}
    return render(request, 'edit_task.html', context)
    
def edit_task(request, task_id=None):
    description = request.POST.get('description')
    task = Task.objects.all().filter(id=str(task_id))[0]
    task.description = description
    task.save()
    return HttpResponseRedirect(reverse('app1:task_list'))
    
def finish_task(request, task_id=None):
    task = Task.objects.all().filter(id=str(task_id))[0]
    task.is_finished = True
    task.save()
    return HttpResponseRedirect(reverse('app1:task_list'))