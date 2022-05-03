from http import HTTPStatus
import unittest
from urllib import response
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
#from sqlite3 import IntegrityError
from django.test import Client
from django.urls import reverse
from studysite.models import *
import datetime
from .forms import *
from django.core.files.uploadedfile import SimpleUploadedFile


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

    try:
      self.userprofile1 = UserProfile.objects.create(user=self.user1, year="1", major="CS", bio="I like to study")
    except IntegrityError:
      #print("USer id print:",type(UserProfile.objects.filter(user=self.user1)[0]))
      userprofile1 = UserProfile.objects.filter(user=self.user1)[0]
      userprofile1.delete()
      self.userprofile1 = UserProfile.objects.create(user=self.user1, year="1", major="CS", bio="I like to study")
    self.userprofile1.save()

    try:
      self.userprofile2 = UserProfile.objects.create(user=self.user2, year="2", major="MATH", bio="I don't like to study")
    except IntegrityError:
      #print("USer id print:",type(UserProfile.objects.filter(user=self.user1)[0]))
      userprofile2 = UserProfile.objects.filter(user=self.user2)[0]
      userprofile2.delete()
      self.userprofile2 = UserProfile.objects.create(user=self.user2, year="2", major="MATH", bio="I don't like to study")
    self.userprofile2.save()

    self.user1.userprofile.save()
    self.user2.userprofile.save()

    self.client = Client()


  def test_true(self):
    self.assertTrue(True)

  def test_login_valid(self):
    response = self.client.get('/studysite/accounts/google/login/', secure=True)
    self.client.login(username='user1', password='1234567')
    self.assertEqual(response.status_code, 302)

  def test_course_list(self):
    response = self.client.get(reverse('course-finder', kwargs={'filtered':'all',}), secure=True)
    self.assertEqual(response.status_code, 302)

  def test_message(self):
    num_prev = len(Message.objects.all())
    message = Message(from_user = self.user1, to_user = self.user2, msg_content = "Hey Studdy Buddy")
    self.user2.userprofile.num_alerts = self.user2.userprofile.num_alerts + 1
    self.user2.save()
    message.save()

    self.assertEqual(self.user2.userprofile.num_alerts, 1)
    self.assertEqual(self.user1.userprofile.num_alerts, 0)
    self.assertEqual(message.msg_content, "Hey Studdy Buddy")
    self.assertEqual(len(Message.objects.all()), num_prev + 1)
    message.delete()
    self.assertEqual(len(Message.objects.all()), num_prev)


  def test_friend_request(self):
    num_prev = len(FriendRequest.objects.all())
    fr = FriendRequest(from_user = self.user1, to_user = self.user2)
    self.user2.userprofile.num_alerts = self.user2.userprofile.num_alerts + 1
    self.user2.save()
    fr.save()

    self.assertEqual(self.user2.userprofile.num_alerts, 1)
    self.assertEqual(self.user1.userprofile.num_alerts, 0)
    self.assertEqual(len(FriendRequest.objects.all()), num_prev + 1)
    fr.delete()
    self.assertEqual(len(FriendRequest.objects.all()), num_prev)

  def tearDown(self):
    self.user1.delete()
    self.user2.delete()

    self.userprofile1.delete()
    self.userprofile2.delete()



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

    try:
      self.userprofile1 = UserProfile.objects.create(user=self.user1, year="1", major="CS", bio="I like to study")
    except IntegrityError:
      userprofile1 = UserProfile.objects.filter(user=self.user1)[0]
      userprofile1.delete()
      self.userprofile1 = UserProfile.objects.create(user=self.user1, year="1", major="CS", bio="I like to study")
    self.userprofile1.save()

    try:
      self.userprofile2 = UserProfile.objects.create(user=self.user2, year="2", major="MATH", bio="I don't like to study")
    except IntegrityError:
      userprofile2 = UserProfile.objects.filter(user=self.user2)[0]
      userprofile2.delete()
      self.userprofile2 = UserProfile.objects.create(user=self.user2, year="2", major="MATH", bio="I don't like to study")
    self.userprofile2.save()

    self.user1.userprofile.save()
    self.user2.userprofile.save()

    self.client = Client()

  def test_about_url(self):
    response = self.client.get(reverse('about'), secure=True)
    self.assertEqual(response.status_code, 200)

  def test_base_url(self):
    response = self.client.get(reverse('index'), secure=True)
    self.assertEqual(response.status_code, 200)

  def test_auth_profile_url(self):
    self.client.get('/studysite/accounts/google/login/', secure=True)
    self.client.login(username='user1', password='1234567')
    response = self.client.get(reverse('profile', kwargs={'username': 'user1'}), secure=True)
    self.assertEqual(response.status_code, 200)

  def test_unauth_profile_url(self):
    response = self.client.get(reverse('profile', kwargs={'username': 'wronguser'}), secure=True)
    self.assertEqual(response.status_code, 302)

  def test_auth_dashboard_url(self):
    self.client.get('/studysite/accounts/google/login/', secure=True)
    self.client.login(username='user1', password='1234567')
    response = self.client.get(reverse('dashboard', kwargs={'username': 'user1'}), secure=True)
    self.assertEqual(response.status_code, 200)

  def test_unauth_dashboard_url(self):
    response = self.client.get(reverse('dashboard', kwargs={'username': 'wronguser'}), secure=True)
    self.assertEqual(response.status_code, 302)

  def test_contact_us_form_url(self):
    response = self.client.get('/studysite/contact/')
    self.assertEqual(response.status_code, 301)

  def test_contact_us_form_url_with_data(self):
    response = self.client.get('/studysite/contact/', data={'first_name': 'John', 'last_name': 'Doe', 'email': 'john.doe@gmail.com', 'question': 'How are you?'})
    self.assertEqual(response.status_code, 301)
    
  # def test_user_profile_form_url(self):
  #   response = self.client.get('/studysite/'+self.user1.username+'/profile/edit_profile', secure=True)
  #   self.assertEqual(response.status_code, HTTPStatus.OK)

  def tearDown(self):
    self.user1.delete()
    self.user2.delete()

    self.userprofile1.delete()
    self.userprofile2.delete()

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

    self.course1.save()

    self.client = Client()
    
  def test_user_course_add(self):
    self.course1.course_roster.add(self.user2)
    self.course1.save()
    self.assertEqual(self.user2, self.course1.course_roster.all()[0])

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

class StudyEventTest(unittest.TestCase):
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
    self.course1.save()
    
    self.event1 = StudyEvent(owner = self.user1, 
                             course = self.course1, 
                             max_users = 8, 
                             time = datetime.datetime(2020, 5, 17, 8, 5, 20), 
                             description = "Study at Clemons",
                             event_id = "10")

    self.event1.save()

    self.client = Client()


  def test_event_made(self):
    owner = self.user1
    course = self.course1
    max_users = 8
    time = datetime.datetime(2020, 5, 17, 8, 5, 20)
    description = "Study at Clemons"
    event_id = "10"

    num_prev = len(StudyEvent.objects.all())
    event = StudyEvent(owner = owner, 
                             course = course, 
                             max_users = max_users, 
                             time = time, 
                             description = description,
                             event_id = event_id)
    event.save()
    self.assertEqual(num_prev + 1, len(StudyEvent.objects.all()))
    event.delete()

  def test_event_deleted(self):
    owner = self.user1
    course = self.course1
    max_users = 8
    time = datetime.datetime(2020, 5, 17, 8, 5, 20)
    description = "Study at Clemons"
    event_id = "10"

    event, created = StudyEvent.objects.get_or_create(owner = owner, 
                             course = course, 
                             max_users = max_users, 
                             time = time, 
                             description = description,
                             event_id = event_id)
    num_prev = len(StudyEvent.objects.all())
    event.delete()
    self.assertEqual(num_prev - 1, len(StudyEvent.objects.all()))

  def test_user_event_add(self):
    self.event1.users.add(self.user2)
    self.event1.save()
    self.assertEqual(self.user2, self.event1.users.all()[0])
    #self.client.get('/studysite/accounts/google/login/')
    #self.client.login(username='user1', password='1234567')
    #self.client.get(reverse('course-finder'))

  def tearDown(self):
    if self.event1 in StudyEvent.objects.all():
      self.event1.delete()
    if self.course1 in Course.objects.all():
      self.course1.delete()
    self.user1.delete()
    self.user2.delete()


# make a unit test for the forms.py class
class FormTest(unittest.TestCase):
  # make a unit tests for UserProfileForm that verifies every field is present
  # initialize the form with a userprofile and fields filling the fields object

  def setUp(self):
    try:
      self.user1 = User.objects.create_user(username='user1', password='1234567')
    except IntegrityError:
      user1 = User.objects.filter(username='user1')[0]
      user1.delete()
      self.user1 = User.objects.create_user(username='user1', password='1234567')
      
    self.user1.save()

    try:
      self.userprofile1 = UserProfile.objects.create(user=self.user1, year="1", major="CS", bio="I like to study")
    except IntegrityError:
      userprofile1 = UserProfile.objects.filter(user=self.user1)[0]
      userprofile1.delete()
      self.userprofile1 = UserProfile.objects.create(user=self.user1, year="1", major="CS", bio="I like to study")
    self.userprofile1.save()

    self.client = Client()

  def test_user_profile_form(self):
    form = UserProfileForm(data={'year': self.user1.userprofile.year, 'major': self.user1.userprofile.major, 'bio': self.user1.userprofile.bio})
    #form = UserProfileForm(instance=self.user1.userprofile)
    #print(form.data)
    #self.assertTrue(form.is_valid())
    #verify every field in the form is correct
    self.assertEqual(form.data['year'], self.user1.userprofile.year)
    self.assertEqual(form.data['major'], self.user1.userprofile.major)
    self.assertEqual(form.data['bio'], self.user1.userprofile.bio)

    # self.assertTrue(form.is_valid())

    #self.assertEqual(form.fields['year'], self.user2.first_name)
    #self.assertEqual(form.fields['major'], self.user2.last_name)
    #self.assertEqual(form.fields['bio'], self.user2.email)
    #self.assertEqual(form.fields['image'].initial, self.user2.question)


  def test_contact_us_form(self):
    form = ContactUsForm(data={'first_name': 'John', 'last_name': 'Doe', 'email': 'john.doe@gmail.com', 'question': 'How are you?'})

    self.assertEqual(form.data['first_name'], 'John')
    self.assertEqual(form.data['last_name'], 'Doe')
    self.assertEqual(form.data['email'], 'john.doe@gmail.com')
    self.assertEqual(form.data['question'], 'How are you?')


  # def test_invalid_contact_us_form(self):
  #   form = ContactUsForm(data={'first_name': 'John', 'last_name': 'Doe', 'email': 'john.doe@gmail.com', 'question': 'How are you?', "test": "test"})
  #   self.assertFalse(form.is_valid())
  
  def tearDown(self):
    self.user1.delete()
    self.userprofile1.delete()