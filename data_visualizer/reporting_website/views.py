from django.shortcuts import render, redirect
#import
import os
from django.conf import settings
from django.http import HttpResponse, Http404, FileResponse
from .forms import DocumentForm
from . import utils
from django.utils.functional import SimpleLazyObject

# Create your views here.
def home(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            file_obj = form.save()
            file_obj.save()
            
            request.session['file_name'] = file_obj.file.name
            
            file_name = request.session['file_name']
            # utils.handle_uploaded_file(file_name)
            
            # return redirect(statistical)
            return redirect(statistical)
    
    form = DocumentForm()
    context = {
        'form': form
    }
        
    return render(request,'home.html', context)

def statistical(request):
    if request.session.has_key('file_name'):
        file_name = request.session['file_name']
        utils.handle_uploaded_file(file_name)
        
        return render(request, 'statistical.html')
    return render(request, 'unimported_file.html')

def present(request):
    if request.session.has_key('file_name'):
        # file_name = request.session['file_name']
        # utils.handle_uploaded_file(file_name)
        
        return render(request, 'present.html')
    return render(request, 'unimported_file.html')

def exportpdf(request):
    if request.session.has_key('file_name'):
        file_path = utils.get_report_file()
        print(file_path)
        if os.path.exists(file_path):
            return FileResponse(open(file_path, 'rb'))
        raise Http404
    else:
        return

def dummy_api(request):
    if request.session.has_key('file_name'):
        if utils.df.shape[0] == 0:
            file_name = request.session['file_name']
            utils.handle_uploaded_file(file_name)
        if request.GET['graph'] == 'city_sales_graph':
            response = HttpResponse(content=utils.get_city_sales_graph())
            response['Content-Type'] = 'image/svg+xml'
            return response
        if request.GET['graph'] == 'monthly_sales_graph':
            response = HttpResponse(content=utils.get_monthly_sales_graph())
            response['Content-Type'] = 'image/svg+xml'
            return response
        if request.GET['graph'] == 'product_sales_percentage_graph':
            response = HttpResponse(content=utils.get_product_sales_percentage_graph())
            response['Content-Type'] = 'image/svg+xml'
            return response
        if request.GET['graph'] == 'product_sold_together_graph_2':
            response = HttpResponse(content=utils.get_product_sold_together_graph_2())
            response['Content-Type'] = 'image/svg+xml'
            return response
        if request.GET['graph'] == 'quantity_total_sales_graph':
            response = HttpResponse(content=utils.get_quantity_total_sales_graph())
            response['Content-Type'] = 'image/svg+xml'
            return response
    return HttpResponse('Nice!')