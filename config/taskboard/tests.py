from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Task
from rest_framework import status

User = get_user_model()

class TaskAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='alice', password='pass123')
        self.user2 = User.objects.create_user(username='bob', password='pass123')
        self.client.login(username='alice', password='pass123')
    

    def test_create_task(self):
        url = reverse('task-list')
        data = {'title': 'Test', 'description': 'desc', 'priority': 2}
        resp = self.client.post(url,data,format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.first().owner, self.user)   

    def test_owner_scope(self):
        Task.objects.create(title='BobTask', owner=self.user2)
        url = reverse('task-list')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data['results']), 0)

class TaskUIActionsTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='alice', password='pass123', email='alice@example.com')
        self.client.login(username='alice', password='pass123')
        self.task = Task.objects.create(title='T1', owner=self.user)
    
    def test_update_status_post(self):
        url = reverse('taskboard:update_status', args=[self.task.pk])
        resp = self.client.post(url, {'status': Task.STATUS_DONE})
        self.assertEqual(resp.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.status, Task.STATUS_DONE)
    
    def test_delete_only_when_done(self):
        # attempt delete when not done
        url = reverse('taskboard:delete_task', args=[self.task.pk])
        resp = self.client.post(url)
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(Task.objects.filter(pk=self.task.pk).exists())

        # mark done then delete
        self.task.status = Task.STATUS_DONE
        self.task.save()
        resp = self.client.post(url)
        self.assertEqual(resp.status_code, 302)
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())