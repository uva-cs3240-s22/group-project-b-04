import unittest
from urllib import response
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.test import Client
from django.urls import reverse
from studysite.models import Course

#https://docs.djangoproject.com/en/4.0/topics/testing/tools/#:~:text=Some%20of%20the%20things%20you%20can%20do%20with,with%20a%20template%20context%20that%20contains%20certain%20values.

class LoginTest(unittest.TestCase):

  def setUp(self):
    try:
      self.user1 = User.objects.create_user(username='user1', password='1234567')
    except IntegrityError:
      user1 = User.objects.filter(username='user1')[0]
      user1.delete()
      self.user1 = User.objects.create_user(username='user1', password='1234567')
    try:
      self.user2 = User.objects.create_user(username='user2', password='89101112')
    except IntegrityError:
      user2 = User.objects.filter(username='user2')[0]
      user2.delete()
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

  def tearDown(self):
    self.user1.delete()
    self.user2.delete()



class URLTest(unittest.TestCase):

  def setUp(self):
    try:
      self.user1 = User.objects.create_user(username='user1', password='1234567')
    except IntegrityError:
      user1 = User.objects.filter(username='user1')[0]
      user1.delete()
      self.user1 = User.objects.create_user(username='user1', password='1234567')
    try:
      self.user2 = User.objects.create_user(username='user2', password='89101112')
    except IntegrityError:
      user2 = User.objects.filter(username='user2')[0]
      user2.delete()
      self.user2 = User.objects.create_user(username='user2', password='89101112')
    self.user1.save()
    self.user2.save()
    self.client = Client()

  def test_about_url(self):
    response = self.client.get('/studysite/about')
    self.assertEqual(response.status_code, 301)

  def test_base_url(self):
    response = self.client.get('/studysite/')
    self.assertEqual(response.status_code, 200)

  def test_auth_profile_url(self):
    self.client.get('/studysite/accounts/google/login/')
    self.client.login(username='user1', password='1234567')
    response = self.client.get(reverse('profile', kwargs={'username': 'user1'}))
    self.assertEqual(response.status_code, 200)

  def test_unauth_profile_url(self):
    response = self.client.get(reverse('profile', kwargs={'username': 'wronguser'}))
    self.assertEqual(response.status_code, 302)

  def test_auth_dashboard_url(self):
    self.client.get('/studysite/accounts/google/login/')
    self.client.login(username='user1', password='1234567')
    response = self.client.get(reverse('dashboard', kwargs={'username': 'user1'}))
    self.assertEqual(response.status_code, 200)

  def test_unauth_dashboard_url(self):
    response = self.client.get(reverse('dashboard', kwargs={'username': 'wronguser'}))
    self.assertEqual(response.status_code, 302)
    
  def tearDown(self):
    self.user1.delete()
    self.user2.delete()

class CourseTest(unittest.TestCase):
  def setUp(self):
    try:
      self.user1 = User.objects.create_user(username='user1', password='1234567')
    except IntegrityError:
      user1 = User.objects.filter(username='user1')[0]
      user1.delete()
      self.user1 = User.objects.create_user(username='user1', password='1234567')
    try:
      self.user2 = User.objects.create_user(username='user2', password='89101112')
    except IntegrityError:
      user2 = User.objects.filter(username='user2')[0]
      user2.delete()
      self.user2 = User.objects.create_user(username='user2', password='89101112')
      
    self.user1.save()
    self.user2.save()

    self.course1 = Course(course_name = "Algorithms", course_subject="CS", course_number="4102")
    if self.course1 in Course.objects.all():
      coursedel = Course.objects.get(course_subject="CS", course_number="4102")
      coursedel.delete()
      self.course1.save()

    self.client = Client()
    
  # def test_user_course_add(self):
  #   self.client.get('/studysite/accounts/google/login/')
  #   self.client.login(username='user1', password='1234567')
  #   self.client.get(reverse('course-finder'))

  def test_course_made(self):
    name = "Theory of Computation "
    subject = "CS"
    number = "3102"
    num_prev = len(Course.objects.all())
    course = Course(course_name = name, course_subject=subject, course_number=number)
    course.save()
    self.assertEqual(num_prev + 1, len(Course.objects.all()))
    course.delete()

  def test_course_deleted(self):
    course, created = Course.objects.get_or_create(course_name="Data Structures", course_subject="cs", course_number="2100")
    num_prev = len(Course.objects.all())
    course.delete()
    self.assertEqual(num_prev - 1, len(Course.objects.all()))

  def tearDown(self):
    if self.course1 in Course.objects.all():
      self.course1.delete()
    self.user1.delete()
    self.user2.delete()