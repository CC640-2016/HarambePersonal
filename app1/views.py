from django.shortcuts import render
from .models import Task

# Create your views here.

def create_task(request):
    return render(request, 'create_task_view.html', {})

def save_task(request):
    description = request.POST.get('description')
    if description != '':
        task = Task(description=description)
        task.save()
    else:
        # tirar error
        pass
        
    return render(request, 'create_task_view.html', {})