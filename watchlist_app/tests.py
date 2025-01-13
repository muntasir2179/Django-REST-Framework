from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from .api import serializers
from . import models

# Create your tests here.


# test cases for streamplatform
class StreamPlatformTestCase(APITestCase):
    def setUp(self):
        # creating a test user
        self.user = User.objects.create_user(username="testcase", password="testpassword")
        self.token = Token.objects.get_or_create(user=self.user)[0]
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        # creating a platform data
        self.stream = models.StreamPlatform.objects.create(name="Netflix", about="#1 Platform", website="https://www.netflix.com")
    
    
    # test for creating a stream platform as a normal user
    def test_streamplatform_create(self):
        data = {
            "name": "Netflix",
            "about": "#1 Streaming Platform",
            "website": "https://netflix.com"
        }
        response = self.client.post(reverse('streamplatform-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)    # we ar trying to add a stream platform as a normal user but this action can only be done as a admin


    # test for accessing stream platform as a normal user
    def test_streamplatform_list(self):
        response = self.client.get(reverse('streamplatform-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    
    # method for testing individual stream platform accessing as a normal user
    def test_streamplatform_ind(self):
        response = self.client.get(reverse('streamplatform-detail', args=(self.stream.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    
    # test for updating stream platform as a normal user
    def test_streamplatform_update(self):
        data = {
            "name": "Netflix - update",
            "about": "#1 Streaming Platform",
            "website": "https://netflix.com"
        }
        response = self.client.put(reverse('streamplatform-detail', args=(self.stream.id,)), data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    
    # test for deleting stream platform as a normal user
    def test_streamplatform_delete(self):
        response = self.client.delete(reverse('streamplatform-detail', args=(self.stream.id,)))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)



# test cases for watchlist
class WatchListTestCase(APITestCase):
    def setUp(self):
        # creating a test user
        self.user = User.objects.create_user(username="testcase", password="testpassword")
        self.token = Token.objects.get_or_create(user=self.user)[0]
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        # creating a platform data
        self.stream = models.StreamPlatform.objects.create(name="Netflix", about="#1 Platform", website="https://www.netflix.com")
        
        # creating a watchlist
        self.watchlist = models.WatchList.objects.create(
            platform=self.stream,
            title="Example Movie",
            storyline="This is a good movie!",
            active=True
        )
    
    
    # test case for creating stream platform as a normal user
    def test_watchlist_create(self):
        data = {
            "title": "Marvel",
            "storyline": "This is a good movie!",
            "active": True,
            "platform": self.stream.id
        }
        response = self.client.post(reverse('watch-list'), data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    
    # test for retrieving watchlist as a normal user
    def test_watchlist_list(self):
        response = self.client.get(reverse('watch-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    
    # test for retrieving individual watchlist as a normal user
    def test_watchlist_ind(self):
        response = self.client.get(reverse('watch-details', args=(self.watchlist.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # we can check for other values and objects as well
        self.assertEqual(models.WatchList.objects.count(), 1)
        self.assertEqual(models.WatchList.objects.get().title, 'Example Movie')

    
    # test for updating individual watchlist as a normal user
    def test_watchlist_update(self):
        data = {
            "title": "Marvel",
            "storyline": "This is a good movie!",
            "active": True,
            "platform": self.stream.id
        }
        response = self.client.put(reverse('watch-details', args=(self.watchlist.id,)), data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    # test for deleting individual watchlist as a normal user
    def test_watchlist_delete(self):
        response = self.client.delete(reverse('watch-details', args=(self.watchlist.id,)))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)



# test cases for reviews
class ReviewTestCase(APITestCase):
    def setUp(self):
        # creating a test user
        self.user = User.objects.create_user(username="testcase", password="testpassword")
        self.token = Token.objects.get_or_create(user=self.user)[0]
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        # creating a platform data
        self.stream = models.StreamPlatform.objects.create(name="Netflix", about="#1 Platform", website="https://www.netflix.com")
        
        # creating a watchlist for testing review create and retrieve
        self.watchlist = models.WatchList.objects.create(
            platform=self.stream,
            title="Example Movie",
            storyline="This is a good movie!",
            active=True
        )
        
        # creating a second watchlist for testing update
        self.watchlist2 = models.WatchList.objects.create(
            platform=self.stream,
            title="Example Movie",
            storyline="This is a good movie!",
            active=True
        )
        
        # creating a review for testing update
        self.review = models.Reviews.objects.create(
            review_user=self.user,
            rating=5,
            description="Great Movie!",
            watchlist=self.watchlist2,
            active=True
        )
    
    
    # testing review creating endpoint
    def test_review_create(self):
        data = {
            "review_user": self.user,
            "rating": 5,
            "description": "Great Movie!",
            "watchlist": self.watchlist,
            "active": True
        }
        
        response = self.client.post(reverse('review-create', args=(self.watchlist.id,)), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # testing if a user can review a movie two times
        response2 = self.client.post(reverse('review-create', args=(self.watchlist.id,)), data=data)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)

    
    # testing creating review as unauthenticated user
    def test_review_create_unauth(self):
        data = {
            "review_user": self.user,
            "rating": 5,
            "description": "Great Movie!",
            "watchlist": self.watchlist,
            "active": True
        }
        
        self.client.force_authenticate(user=None)   # setting user as none means logout
        response = self.client.post(reverse('review-create', args=(self.watchlist.id,)), data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    
    # testing for updating a review
    def test_review_update(self):
        data = {
            "review_user": self.user,
            "rating": 5,
            "description": "Great Movie! - update",
            "watchlist": self.watchlist,
            "active": True
        }
        
        response = self.client.put(reverse('review-detail', args=(self.review.id,)), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    
    # testing for accessing all the review
    def test_review_all(self):
        response = self.client.get(reverse('review-list', args=(self.watchlist.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    
    # testing for accessing individual review
    def test_review_ind(self):
        response = self.client.get(reverse('review-detail', args=(self.review.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    
    # testing for deleting individual review
    def test_review_delete(self):
        response = self.client.delete(reverse('review-detail', args=(self.review.id,)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

