from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


class UserProfile(models.Model):
	# map with existing user model from django
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user")

	def __str__(self):
		return self.user.username
	
	# creates a new profile when new django user is created.
	@receiver(post_save, sender=User)
	def createUserProfile(sender, instance, created, **kwargs):
		# if new user is created
		if created:
			# create a new user profile
			UserProfile.objects.create(user=instance)