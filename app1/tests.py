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
        
