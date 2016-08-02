from django.shortcuts import render
from django.http import HttpResponse
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