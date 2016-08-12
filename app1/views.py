from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .models import Task
from django.db.models import Max

# Create your views here.

def create_task(request):
    return render(request, 'create_task_view.html', {})

def save_task(request):
    description = request.POST.get('description')
    tasks_same_name = Task.objects.filter(description=description)
    if description != '' and len(tasks_same_name) == 0:
        priority = get_last_priority() + 1
        task = Task(description=description, priority=priority)
        task.save()
        
    else:
        # tirar error
        pass
        
    return HttpResponseRedirect(reverse('app1:task_list'))
    
def list_tasks(request, filtering=None):
    tasks = Task.objects.all().order_by('priority')
    if filtering is True:
        context = {'task_list' : tasks, 'filtering' : True}
    else: 
        context = {'task_list' : tasks}
    return render(request, 'task_list.html', context)
    
def list_tasks_finished(request):
    return list_tasks(request, True);
    
def delete_task(request, task_id=None):
    task = Task.objects.get(pk=task_id)
    fix_next_tasks(task.priority)
    delete = task.delete()
    
    return HttpResponseRedirect(reverse('app1:task_list'))
    
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
    
def increase_task_priority(request, task_id=None):
    task = Task.objects.get(pk=task_id)
    if task.priority == 1:
        # Tirar error
        pass
    else:
        other_priority = task.priority - 1
        other = Task.objects.get(priority=other_priority)
        task.priority = task.priority - 1
        other.priority = other.priority + 1
        task.save()
        other.save()
    
    return HttpResponseRedirect(reverse('app1:task_list'))
    
def decrease_task_priority(request, task_id=None):
    task = Task.objects.get(pk=task_id)
    if task.priority == get_last_priority():
        # Tirar error
        pass
    else:
        other_priority = task.priority + 1
        other = Task.objects.get(priority=other_priority)
        task.priority = task.priority + 1
        other.priority = other.priority - 1
        task.save()
        other.save()
    
    return HttpResponseRedirect(reverse('app1:task_list'))
    
    
    
    
    
def get_last_priority():
    priority = Task.objects.all().aggregate(Max('priority'))['priority__max']
    if priority is None:
        return 0
    else:
        return priority
        
def fix_next_tasks(priority):
    tasks = Task.objects.filter(priority__gt=priority)
    for task in tasks:
        task.priority = task.priority - 1
        task.save()