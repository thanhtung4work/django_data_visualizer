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
        
        context = {
            'file_name': file_name,
            'monthly_sales_graph': utils.get_monthly_sales_graph(),
            'city_sales_graph': utils.get_city_sales_graph(),
            'product_sold_together_graph_2': utils.get_product_sold_together_graph_2(),
            'product_sales_percentage_graph': utils.get_product_sales_percentage_graph(),
            'quantity_total_sales_graph': utils.get_quantity_total_sales_graph(),
            'hourly_order_graph': utils.get_hourly_order_graph(),
        }
        
        return render(request, 'statistical.html', context)
    return render(request, 'statistical.html')

def present(request):
    if request.session.has_key('file_name'):
        # file_name = request.session['file_name']
        # utils.handle_uploaded_file(file_name)
        graphs = {
            'monthly_sales_graph': 'a',#utils.get_monthly_sales_graph(),
            # 'city_sales_graph': utils.get_city_sales_graph(),
            # 'product_sold_together_graph_2': utils.get_product_sold_together_graph_2(),
            # 'product_sales_percentage_graph': utils.get_product_sales_percentage_graph(),
            # 'quantity_total_sales_graph': utils.get_quantity_total_sales_graph(),
            # 'hourly_order_graph': utils.get_hourly_order_graph(),
        }
        context = {
            'graphs': graphs
        }
        return render(request, 'present.html', context)
    return render(request, 'present.html')

def exportpdf(request):
    if request.session.has_key('file_name'):
        file_path = utils.get_report_file()
        print(file_path)
        if os.path.exists(file_path):
            return FileResponse(open(file_path, 'rb'))
        raise Http404
    else:
        return

def dummy_view(request):
    if request.session.has_key('file_name'):
        file_name = request.session['file_name']
        utils.handle_uploaded_file(file_name)
        return HttpResponse
    return HttpResponse('OK!')