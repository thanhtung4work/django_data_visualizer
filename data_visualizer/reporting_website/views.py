from django.shortcuts import render
<<<<<<< HEAD
#import
from django.http import HttpResponse

# Create your views here.
def home(request):
    return render(request,'home.html')

def statistical(request):
    return render(request, 'statistical.html')
=======
from django.http import HttpResponse

def home(request):
  return HttpResponse('Hello world')
>>>>>>> a54b7a94a1f0b74208c7a4dbcf2b6e362c95a73e
