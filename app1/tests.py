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
        response = self.client.get('/')
        self.assertEquals(response.status_code, 404)
        response = self.client.get(reverse('app1:create_task'))
        response.status_code = 200
        self.assertTrue('submit' in response.content)
        self.assertContains(response, 'submit')
        
class CreateTaskTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.c =  Client()
        
    def test_task_post(self):
        response = self.c.post(reverse('app1:save_task'), {'description': 'jugar lol'})
        response2 = self.c.post(reverse('app1:save_task'), {'description':'comer'})
        self.assertEquals(2, len(Task.objects.all()))
        self.assertEquals('jugar lol', Task.objects.all()[0].description)
        self.assertEquals(False, Task.objects.all()[1].is_finished)
        

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
