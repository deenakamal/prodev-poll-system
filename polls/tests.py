from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Poll, Option, Vote

User = get_user_model()


class PollsAPITest(TestCase):
    """
    Test suite for Polls API (poll creation, voting, and results).
    """

    def setUp(self):
        self.client = APIClient()
        self.poll = Poll.objects.create(question="What's your favorite color?")
        self.option1 = Option.objects.create(poll=self.poll, text="Red")
        self.option2 = Option.objects.create(poll=self.poll, text="Blue")
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.force_authenticate(user=self.user)

    def test_list_polls(self):
        """
        Ensure poll list API returns available polls.
        """
        url = reverse("poll-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # pagination returns {"count": X, "results": [...]}
        self.assertGreaterEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["question"], self.poll.question)

    def test_vote_success(self):
        """
        Ensure a user can vote once successfully.
        """
        url = reverse("vote-create")
        payload = {"poll": self.poll.id, "option": self.option1.id}
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check vote exists in DB
        exists = Vote.objects.filter(poll=self.poll, option=self.option1, user=self.user).exists()
        self.assertTrue(exists)

    def test_prevent_duplicate_vote(self):
        """
        Ensure a user cannot vote twice on the same poll.
        """
        url = reverse("vote-create")
        payload = {"poll": self.poll.id, "option": self.option1.id}
        first_vote = self.client.post(url, payload)
        self.assertEqual(first_vote.status_code, status.HTTP_201_CREATED)

        # Try second vote
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_poll_results(self):
        """
        Ensure poll results API returns results dict.
        """
        url = reverse("poll-results", args=[self.poll.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)
        self.assertEqual(response.data["results"], {"Red": 0, "Blue": 0})
