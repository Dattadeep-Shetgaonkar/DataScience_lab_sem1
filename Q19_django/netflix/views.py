
from django.shortcuts import render
from .models import NetflixShow

def show_list(request):
	shows = NetflixShow.objects.all()
	return render(request, 'netflix/show_list.html', {'shows': shows})
