from django.db import models
import time
from datetime import date

# User model
class User(models.Model):
	email = models.CharField(max_length=100, primary_key=True)
	firstname = models.CharField(max_length=255)
	surname = models.CharField(max_length=255, default='')
	age = models.CharField(max_length=255)
	gender = models.CharField(max_length=30)
	dominanthand = models.CharField(max_length=30)
	password = models.CharField(max_length=255, default='')
# Colour model
class Colour(models.Model):
	colourID = models.IntegerField(default=0, primary_key=True)
	hexcode = models.CharField(max_length=10, default='#ffffff')
# Sound model
class Sound(models.Model):
	soundID = models.IntegerField(default=0, primary_key=True)
	instrument = models.CharField(max_length=100)
	pitch = models.CharField(max_length=10)
# AttemptOne model
class AttemptOne(models.Model):
	userOne = models.CharField(max_length=100) # User email
	colourOne = models.CharField(max_length=10, default='#ffffff') # Colour hex
	soundOne = models.CharField(default=0, max_length=3) # Sound id
# AttemptTwo model
class AttemptTwo(models.Model):
	userTwo = models.CharField(max_length=100) # User email
	colourTwo = models.CharField(max_length=10, default='#ffffff') # Colour hex
	soundTwo = models.CharField(default=0, max_length=3) # Sound id
