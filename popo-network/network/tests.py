from django.test import TestCase

# Create your tests here.
from .models import Post, User

class NetworkTestCase(TestCase):

    def setUp(self):

        # Create airports.
        a1 = User.objects.create(username='user1',email='user1@test.com',password='password1')
        a2 = User.objects.create(username='user2',email='user2@test.com',password='password2')
        a3 = User.objects.create(username='user3',email='user3@test.com',password='password3')
        a4 = User.objects.create(username='user4',email='user4@test.com',password='password4')
        a5 = User.objects.create(username='user5',email='user5@test.com',password='password5')
        a6 = User.objects.create(username='user6',email='user6@test.com',password='password6')
                
        a2.followers.add(a1)
        a2.followers.add(a5)
        a2.followers.add(a6)
        
        a2.following.add(a1)
       
    def following_count(self):
        a = User.objects.get(id=a2.id)
        self.assertEqual(a.user_following.count(), 1)

    def follower_count(self):
        a =User.objects.get(id=a2.id)
        self.assertEqual(a.user_followers.count(), 3)
        
        
        

        
     
        
    
        


        
        
        
        
        
        