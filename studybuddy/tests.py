from django.contrib.auth.models import User
from django.test import Client

class LoginTest(unittest.TestCase):
  def setup(self):
    user1 = User.objects.create_user(username='user1', password='1234567')
    user2 = User.objects.create_user(username='user2', password='89101112')
    user1.save()
    user2.save()
  def test_login(self):
    c = Client()
    response = c.post('', {'username': 'user1', 'password': 1234567'})
    self.assertEqual(response.status_code, 200)
    self.assertEqual(str(response.context['user']), 'user1')
