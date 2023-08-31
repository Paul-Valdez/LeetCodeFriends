from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title + "\n" + self.description


class UserProfile(models.Model):
    # Define fields to store the necessary data
    username = models.CharField(max_length=255, unique=True)
    totalSolved = models.IntegerField()
    easySolved = models.IntegerField()
    mediumSolved = models.IntegerField()
    hardSolved = models.IntegerField()
    acceptanceRate = models.FloatField()
    ranking = models.IntegerField()
    contributionPoints = models.IntegerField()
    reputation = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    location = models.CharField(max_length=255, null=True)
    phoneNumber = models.IntegerField(unique=True, null=True)

    def __str__(self):
        return self.username

#
class LCGlobalData(models.Model):
    #id = models.PositiveIntegerField(primary_key=True)
    timestamp = models.DateTimeField(default=timezone.now)
    totalQuestions = models.IntegerField(default=-1)
    totalEasy = models.IntegerField(default=-1)
    totalMedium = models.IntegerField(default=-1)
    totalHard = models.IntegerField(default=-1)
'''
    def __str__(self):
        return self.id
#'''