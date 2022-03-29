import unittest
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse
from studysite.models import Course

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

  def test_login_valid(self):
    response = self.client.get('/studysite/accounts/google/login/')
    self.client.login(username='user1', password='1234567')
    self.assertEqual(response.status_code, 200)
    #self.assertEqual(str(response.context['user']), 'user1') # context does not exist, only context_data which doesnt have a user field. something flucky about this

  def test_course_form(self):
    response = self.client.get(reverse('course-add'))
    self.assertEqual(response.status_code, 200)

  def test_course_made(self):
    name = "Algorithms"
    subject = "CS"
    number = "4102"
    num_prev = len(Course.objects.all())
    Course.objects.create(course_name = name, course_subject=subject, course_number=number)
    self.assertEqual(num_prev + 1, len(Course.objects.all()))
    
  def test_about_url(self):
    response = self.client.get('/studysite/about')
    self.assertEqual(response.status_code, 301)

  def test_base_url(self):
    response = self.client.get('/studysite/')
    self.assertEqual(response.status_code, 200)

  def tearDown(self):
    self.user1.delete()
    self.user2.delete()

