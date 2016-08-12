from django.test import TestCase, Client, RequestFactory
from django.test import LiveServerTestCase
from .models import Task
from django.test.utils import setup_test_environment
from django.core.urlresolvers import reverse


class TaskModelTest(TestCase):
    
    task = None

    def setUp(self):
        self.task = Task()
        self.task.description = "Ir al supermercado."        
        self.task.is_finished = False
        self.task.save()

    def tearDown(self):
        pass

    def test_task_model(self):
        """ Se pueden guardar las tareas """
        
        self.assertTrue(True)
        
        all_tasks_in_database = Task.objects.all()
        self.assertEquals(len(all_tasks_in_database), 1)
        only_task_in_database = all_tasks_in_database[0]
        self.assertEquals(only_task_in_database, self.task)

        # and check that it's saved its two attributes: question and pub_date
        self.assertEquals(only_task_in_database.description, "Ir al supermercado.")
        self.assertFalse(only_task_in_database.is_finished)
        

class view_tests(TestCase):
    client = None
    
    def setUp(self):
        setup_test_environment()
        # create an instance of the client for our use
        self.client = Client()
    
    def test_view(self):
        response = self.client.get(reverse('app1:create_task'))
        response.status_code = 200
        self.assertTrue('submit' in response.content)
        self.assertContains(response, 'submit')
        
        
class CreateTaskTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.c =  Client()
        response = self.c.post(reverse('app1:save_task'), {'description': 'jugar lol'})
        response2 = self.c.post(reverse('app1:save_task'), {'description':'comer'})
        
    def test_task_post(self):
        self.assertEquals(2, len(Task.objects.all()))
        self.assertEquals('jugar lol', Task.objects.all()[0].description)
        
    def test_task_starts_unfinished(self):
        self.assertEquals(False, Task.objects.all()[0].is_finished)
                

class list_tasks_view_tests(TestCase):
    
    def setUp(self):
        setup_test_environment()
        # create an instance of the client for our use
        self.client = Client()
        response = self.client.post(reverse('app1:save_task'), {'description': 'jugar lol'})
        response2 = self.client.post(reverse('app1:save_task'), {'description':'comer'})
    
    def test_view(self):
        response = self.client.get(reverse('app1:task_list'))
        response.status_code = 200
        self.assertContains(response, 'Lista de Tareas')
        self.assertContains(response, 'comer')
        
class delete_task_tests(TestCase):
    def setUp(self):
        setup_test_environment()
        # create an instance of the client for our use
        self.client = Client()
        self.client.post(reverse('app1:save_task'), {'description': 'jugar lol'})
        self.client.post(reverse('app1:save_task'), {'description':'comer'})
        
    def test_delete(self):
        self.client.post(reverse('app1:delete_task', args=(1,)))
        self.assertEquals(1, len(Task.objects.all()))
        response = self.client.get(reverse('app1:task_list'))
        self.assertContains(response, 'comer')
        

class EditTask(TestCase):
    
    def setUp(self):
        setup_test_environment()
        self.client = Client()
        response = self.client.post(reverse('app1:save_task'), {'description': 'jugar lol'})
        response2 = self.client.post(reverse('app1:save_task'), {'description':'comer'})
        
    def test_view(self):
        response = self.client.get(reverse('app1:edit_task_view', args=(1,)))
        response.status_code = 200
        self.assertContains(response, 'jugar lol')
        self.assertContains(response, 'submit')
        
    def test_edit_task(self):
        response = self.client.post(reverse('app1:edit_task', args=(1,)), {'description': 'beber'})
        self.assertEquals(2, len(Task.objects.all()))
        self.assertEquals('beber', Task.objects.all().filter(id=1)[0].description)
        
class FinishTask(TestCase):
    
    def setUp(self):
        setup_test_environment()
        self.client = Client()
        response = self.client.post(reverse('app1:save_task'), {'description': 'jugar lol'})
        
    def test_view(self):
        response = self.client.get(reverse('app1:task_list'))
        response.status_code = 200
        self.assertContains(response, 'jugar lol')
        self.assertContains(response, 'Terminar')
        
    def test_finish_task(self):
        self.assertEquals(False, Task.objects.all().filter(id=1)[0].is_finished)
        self.assertEquals('jugar lol', Task.objects.all().filter(id=1)[0].description)
        response = self.client.post(reverse('app1:finish_task', args=(1,))) # arg 1 es el id del post a ponerle que termino
        self.assertEquals(1, len(Task.objects.all()))
        self.assertEquals('jugar lol', Task.objects.all().filter(id=1)[0].description)
        self.assertEquals(True, Task.objects.all().filter(id=1)[0].is_finished)
       
        
class ListNonFinishedTasksView(TestCase):
    
    def setUp(self):
        setup_test_environment()
        self.client = Client()
        response = self.client.post(reverse('app1:save_task'), {'description': 'jugar lol'})
        response = self.client.post(reverse('app1:finish_task', args=(1,)))
        response2 = self.client.post(reverse('app1:save_task'), {'description': 'jugar dota'})
        
    def test_view(self):
        response = self.client.get(reverse('app1:task_list_finished'))
        response.status_code = 200
        self.assertNotContains(response, 'jugar lol')
        self.assertContains(response, 'jugar dota')
        

class CheckPrioritiesAddTasks(TestCase):
    
    def setUp(self):
        setup_test_environment()
        # create an instance of the client for our use
        self.client = Client()
        response = self.client.post(reverse('app1:save_task'), {'description': 'jugar lol'})
        response2 = self.client.post(reverse('app1:save_task'), {'description':'comer'})
        
    def test_check_priorities(self):
        task1 = Task.objects.get(description='jugar lol')
        task2 = Task.objects.get(description='comer')
        self.assertEquals(1, task1.priority)
        self.assertEquals(2, task2.priority)
      
      
class CheckPrioritiesDeleteTask(TestCase):
    
    def setUp(self):
        setup_test_environment()
        # create an instance of the client for our use
        self.client = Client()
        response = self.client.post(reverse('app1:save_task'), {'description': 'task1'})
        response2 = self.client.post(reverse('app1:save_task'), {'description':'task2'})
        response3 = self.client.post(reverse('app1:save_task'), {'description':'task3'})
        response4 = self.client.post(reverse('app1:save_task'), {'description':'task4'})
        
    def test_check_priorities(self):
        response = self.client.post(reverse('app1:delete_task', args=(2,)))
        task1 = Task.objects.get(pk=1)
        task3 = Task.objects.get(pk=3)
        task4 = Task.objects.get(pk=4)
        self.assertEquals(1, task1.priority)
        self.assertEquals(2, task3.priority)
        self.assertEquals(3, task4.priority)
        
        
class IncreaseTaskPriority(TestCase):
    
    def setUp(self):
        setup_test_environment()
        # create an instance of the client for our use
        self.client = Client()
        response = self.client.post(reverse('app1:save_task'), {'description': 'task1'})
        response2 = self.client.post(reverse('app1:save_task'), {'description':'task2'})
        
    def test_increase_priority(self):
        response = self.client.post(reverse('app1:increase_task_priority', args=(2,)))
        task1 = Task.objects.get(pk=1)
        task2 = Task.objects.get(pk=2)
        self.assertEquals(2, task1.priority)
        self.assertEquals(1, task2.priority)
        
        
class IncreaseTaskPriorityFail(TestCase):
    
    def setUp(self):
        setup_test_environment()
        # create an instance of the client for our use
        self.client = Client()
        response = self.client.post(reverse('app1:save_task'), {'description': 'task1'})
        response2 = self.client.post(reverse('app1:save_task'), {'description':'task2'})
        
    def test_increase_priority(self):
        response = self.client.post(reverse('app1:increase_task_priority', args=(1,)))
        task1 = Task.objects.get(pk=1)
        task2 = Task.objects.get(pk=2)
        self.assertEquals(1, task1.priority)
        self.assertEquals(2, task2.priority)
        
        
class DecreaseTaskPriority(TestCase):
    
    def setUp(self):
        setup_test_environment()
        # create an instance of the client for our use
        self.client = Client()
        response = self.client.post(reverse('app1:save_task'), {'description': 'task1'})
        response2 = self.client.post(reverse('app1:save_task'), {'description':'task2'})
        
    def test_decrease_priority(self):
        response = self.client.post(reverse('app1:decrease_task_priority', args=(1,)))
        task1 = Task.objects.get(pk=1)
        task2 = Task.objects.get(pk=2)
        self.assertEquals(2, task1.priority)
        self.assertEquals(1, task2.priority)
        
        
class DecreaseTaskPriorityFail(TestCase):
    
    def setUp(self):
        setup_test_environment()
        # create an instance of the client for our use
        self.client = Client()
        response = self.client.post(reverse('app1:save_task'), {'description': 'task1'})
        response2 = self.client.post(reverse('app1:save_task'), {'description':'task2'})
        
    def test_decrease_priority(self):
        response = self.client.post(reverse('app1:decrease_task_priority', args=(2,)))
        task1 = Task.objects.get(pk=1)
        task2 = Task.objects.get(pk=2)
        self.assertEquals(1, task1.priority)
        self.assertEquals(2, task2.priority)
        
class CleanTaskList(TestCase):
    
    def setUp(self):
        setup_test_environment()
        self.client = Client()
        response = self.client.post(reverse('app1:save_task'), {'description': 'task1'})
        response2 = self.client.post(reverse('app1:save_task'), {'description':'task2'})
        
    def test_clean_list(self):
        response = self.client.post(reverse('app1:clean_task_list'))
        all_tasks = Task.objects.all()
        self.assertEquals(0, len(all_tasks))
        
class CleanTaskListView(TestCase):
    
    def setUp(self):
        setup_test_environment()
        self.client = Client()
        response = self.client.post(reverse('app1:save_task'), {'description': 'task1'})
        response2 = self.client.post(reverse('app1:save_task'), {'description':'task2'})
    
    def test_list_nonempty(self):
        response = self.client.get(reverse('app1:task_list'))
        response.status_code = 200
        self.assertContains(response, 'task1')
        self.assertContains(response, 'task2')
        self.assertContains(response, 'Limpiar lista')
    
    def test_list_empty(self):
        response = self.client.post(reverse('app1:clean_task_list'))
        response.status_code = 200
        self.assertNotContains(response, 'task1')
        self.assertNotContains(response, 'task2')