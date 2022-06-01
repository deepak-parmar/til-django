from django.db import models

# Create your models here.
class Post(models.Model):
	content = models.CharField(max_length=280)
	dateCreated = models.DateTimeField(auto_now_add=True)
	dateModified = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.content