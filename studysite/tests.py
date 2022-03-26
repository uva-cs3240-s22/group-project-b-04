import unittest
from django.contrib.auth.models import User
from django.test import Client

#https://docs.djangoproject.com/en/4.0/topics/testing/tools/#:~:text=Some%20of%20the%20things%20you%20can%20do%20with,with%20a%20template%20context%20that%20contains%20certain%20values.

class LoginTest(unittest.TestCase):
  def setup(self):
    user1 = User.objects.create_user(username='user1', password='1234567')
    user2 = User.objects.create_user(username='user2', password='89101112')
    user1.save()
    user2.save()
    self.client = Client()
  def test_login(self):
    self.assertTrue(2 > 1)
    # c = Client()
    response = self.client.get(reverse('login'))
    # #login(username='user1', password='1234567')
    self.assertEqual(response.status_code, 200)
    #self.assertEqual(str(response.context['user']), 'user1')

