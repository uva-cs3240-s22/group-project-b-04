import unittest
from django.contrib.auth.models import User
from django.test import Client

#https://docs.djangoproject.com/en/4.0/topics/testing/tools/#:~:text=Some%20of%20the%20things%20you%20can%20do%20with,with%20a%20template%20context%20that%20contains%20certain%20values.

class LoginTest(unittest.TestCase):
  def setUp(self):
    self.user1 = User.objects.create_user(username='user1', password='1234567')
    self.user2 = User.objects.create_user(username='user2', password='89101112')
    self.user1.save()
    self.user2.save()
    self.client = Client()

  def test_true(self):
    self.assertTrue(True)

  def test_login(self):
    response = self.client.get('/accounts/login/')
    self.client.login(username='user1', password='1234567')
    self.assertEqual(response.status_code, 200)
    self.assertEqual(str(response.context['user']), 'user1') # context does not exist, only context_data which doesnt have a user field. something flucky about this

  def tearDown(self):
    self.user1.delete()
    self.user2.delete()

