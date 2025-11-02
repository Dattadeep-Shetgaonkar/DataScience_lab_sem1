
from django.db import models

class NetflixShow(models.Model):
	show_id = models.CharField(max_length=20, unique=True)
	type = models.CharField(max_length=20)
	title = models.CharField(max_length=255)
	director = models.CharField(max_length=255, blank=True, null=True)
	cast = models.TextField(blank=True, null=True)
	country = models.CharField(max_length=255, blank=True, null=True)
	date_added = models.CharField(max_length=50, blank=True, null=True)
	release_year = models.IntegerField()
	rating = models.CharField(max_length=10)
	duration = models.CharField(max_length=50)
	listed_in = models.CharField(max_length=255)
	description = models.TextField()

	def __str__(self):
		return self.title
