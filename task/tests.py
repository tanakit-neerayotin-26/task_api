from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Task


class TaskAPITests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='alice', password='pass123!')
        self.user2 = User.objects.create_user(username='bob', password='pass123!')
        self.task1 = Task.objects.create(
            title='Alice task', owner=self.user1
        )

    def test_anonymous_user_cannot_list_tasks(self):
        response = self.client.get('/api/task/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_user_create_task(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.post('/api/task/', data={
            'title':'Alice test login'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_user_not_authorized(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(f'/api/task/{self.task1.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_login_user_cannot_delete_others_task(self):
          self.client.force_authenticate(user=self.user2)
          response = self.client.delete(f'/api/task/{self.task1.id}/')
          self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
          self.assertTrue(Task.objects.filter(id=self.task1.id).exists())

    def test_login_user_no_title_create_task(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.post('/api/task/', data={
            'title': ''
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_user_update_title_task(self):
            self.client.force_authenticate(user=self.user1)
            response = self.client.patch(f'/api/task/{self.task1.id}/', data={
                'title': 'Update test'
            })
            print(response.data)
            self.task1.refresh_from_db()
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(self.task1.title, 'Update test')

    def test_login_user_get_request_task(self):
         Task.objects.create(title='Alice task2 test', owner=self.user1, status='done')
         self.client.force_authenticate(user=self.user1)
         response = self.client.get(f'/api/task/?status=done')
         self.assertEqual(len(response.data), 1)
         self.assertEqual(response.data[0]['status'], 'done')
            
    
            
                

