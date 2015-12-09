from django.shortcuts import render_to_response
from django.http import HttpResponse

def index(request):
	#with open('html/index.html', 'r') as html_file:
	#	html = html_file.read()
	return render_to_response('index.html')
#return HttpResponse("This will be a video!")
