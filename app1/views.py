from django.shortcuts import render

# Create your views here.

def create_task(request):
    return render(request, 'create_task_view.html', {})
