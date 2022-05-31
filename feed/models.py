from django.db import models

# Create your models here.
class Post(models.Model):
	content = models.CharField(max_length=280)
	date = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.content