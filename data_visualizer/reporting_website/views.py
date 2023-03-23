from django.shortcuts import render
#import
from django.http import HttpResponse
from .forms import DocumentForm
from . import utils

# Create your views here.
def home(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            file_obj = form.save()
            file_obj.save()
            
            request.session['file_name'] = file_obj.file.name
            
            file_name = request.session['file_name']
            return render(request, 'statistical.html', {'file_name': file_name})
    
    form = DocumentForm()
    context = {
        'form': form
    }
        
    return render(request,'home.html', context)

def statistical(request):
    if request.session.has_key('file_name'):
        file_name = request.session['file_name']
        utils.handle_uploaded_file(file_name)
        context = {
            'file_name': file_name,
            'monthly_sales_graph': utils.get_monthly_sales_graph()
        }
        return render(request, 'statistical.html', context)
    return render(request, 'statistical.html')

def present(request):
    return render(request, 'present.html')

def exportpdf(request):
    return render(request, 'exportPDF.html')

def dummy_view(request):
    if request.session.has_key('file_name'):
        file_name = request.session['file_name']
        utils.handle_uploaded_file(file_name)
        return HttpResponse
    return HttpResponse('OK!')