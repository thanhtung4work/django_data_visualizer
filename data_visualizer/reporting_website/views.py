from django.shortcuts import render
#import
from django.http import HttpResponse

# Create your views here.
def home(request):
    return render(request,'home.html')

def statistical(request):
    return render(request, 'statistical.html')

def present(request):
    return render(request, 'present.html')

def exportpdf(request):
    return render(request, 'exportPDF.html')
