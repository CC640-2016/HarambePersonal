from django.test import TestCase
from django.test import LiveServerTestCase
from selenium import webdriver
from .models import Task

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
        
from django.test.utils import setup_test_environment
from django.test import Client        
from django.core.urlresolvers import reverse

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