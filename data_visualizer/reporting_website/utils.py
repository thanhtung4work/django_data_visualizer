import pandas as pd
import matplotlib as mpl
mpl.use('Agg')
colors=['#ff6961', '#ffb480', '#f8f38d', '#42d6a4', '#08cad1', '#59adf6', '#9d94ff', '#c780e8']
mpl.rcParams['axes.prop_cycle'] = mpl.cycler(color=colors)

import matplotlib.pyplot as plt
import pylab
from matplotlib.ticker import StrMethodFormatter
from django.core.files.storage import default_storage
import os
from django.http import HttpResponse
from io import StringIO
from matplotlib.backends.backend_pdf import PdfPages
from django.conf import settings
import uuid

df = pd.DataFrame()

def clean_up():
  global df
  # remove nan
  df = df.dropna(axis = 0, how = 'all')
  df = df[df['Order Date'].str[0:2] != 'Or']

  # convert to correct type
  df['Quantity Ordered'] = pd.to_numeric(df['Quantity Ordered'])
  df['Price Each'] = pd.to_numeric(df['Price Each'])
  df['Order ID'] = pd.to_numeric(df['Order ID'])

  # Month column
  df['Month'] = df['Order Date'].str[0:2]
  df['Month'] = df['Month'].astype('int32')

  # Convert order data
  df['Order Date'] = pd.to_datetime(df['Order Date'])
  df['Order Hour'] = df['Order Date'].dt.hour
  df['Order Minute'] = df['Order Date'].dt.minute

  # Total sales
  df['Total sales'] = df['Quantity Ordered'] * df['Price Each']
  # City
  def get_city(address):
    return address.split(',')[1].strip()
  def get_state(address):
    return address.split(',')[2].strip().split(' ')[0]
  df['City'] = df['Purchase Address'].apply(lambda x : f'{get_city(x)} ({get_state(x)})')

def handle_uploaded_file(file_name):
  f = default_storage.open(os.path.join('', file_name), 'r')
  global df 
  df = pd.read_csv(f)
  clean_up()

def get_monthly_sales_graph(return_type='graph'):
  months = range(1, 13)
  sales_by_month = df.groupby('Month').sum()
  # create your image as usual, e.g. pylab.plot(...)
  
  fig = plt.figure(figsize=(16, 9))
  plt.bar(months, sales_by_month['Total sales'])
  plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))
  plt.title('Tổng doanh thu mỗi tháng', size=32)
  plt.xticks(months, size=16)
  plt.xlabel('Tháng', size=16)
  plt.ylabel('Doanh thu', size=16)
  plt.tight_layout()
  
  if return_type =='fig':
    return fig
  
  graph = StringIO()
  fig.savefig(graph, format='svg')
  graph.seek(0)
  data = graph.getvalue()
  
  return data

def get_city_sales_graph(return_type='graph'):
  sales_by_city = df.groupby('City').sum()

  fig = plt.figure(figsize=(16, 9))
  cities = [city for city, df in df.groupby('City')]

  plt.bar(cities, sales_by_city['Total sales'])
  plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))
  plt.title('Tổng doanh thu của từng thành phố', size=32)
  plt.xticks(cities, rotation=10, size=12)
  plt.xlabel('Thành phố', size=16)
  plt.ylabel('Doanh thu', size=16)
  plt.grid()

  if return_type =='fig':
    return fig

  graph = StringIO()
  fig.savefig(graph, format='svg')
  graph.seek(0)
  data = graph.getvalue()
  
  return data

def get_product_sold_together_graph_2(return_type='graph'):
  group_df = df[df.duplicated(['Order ID'], keep=False)].copy()
  group_df['Product Group'] = group_df.groupby('Order ID')['Product'].transform(lambda x: ','.join(x))
  group_df = group_df[['Order ID', 'Product Group']].drop_duplicates()

  from itertools import combinations
  from collections import Counter

  counter = Counter()
  for row in group_df['Product Group']:
    prod_list = row.split(',')
    counter.update(Counter(combinations(prod_list, 2)))

  pairs = []
  pairs_count = []
  for key, value in counter.most_common(10):
    pairs.append(' ,\n'.join(key))
    pairs_count.append(value)

  fig = plt.figure(figsize=(16, 9))
  plt.barh(pairs, pairs_count)
  plt.title('Bộ đôi sản phẩm được mua cùng nhau', size=32)
  plt.xlabel('Số lượng')
  plt.xticks(fontsize=14)
  plt.ylabel('Sản phẩm')
  for x, y in zip(pairs_count, pairs):
    plt.text(x, y, str(x), ha='left', va='center', fontsize=14)

  plt.tight_layout()
  
  if return_type =='fig':
    return fig

  graph = StringIO()
  fig.savefig(graph, format='svg')
  graph.seek(0)
  data = graph.getvalue()
  
  return data

def get_product_sales_percentage_graph():
  def my_level_list(label, data, sum):
    list = []
    for i in range(len(data)):
      if (data[i]*100/sum) > 3: # 3%
        list.append(label[i])
      else:
        list.append('')
    return list

  def my_autopct(pct):
    return ('%.1f%%' % pct) if pct > 3 else ''

  def my_explode(label, data, sum):
    list = []
    for i in range(len(data)):
      percentage = data[i]*100/sum
      if (percentage) > 10: # 10%
        list.append(0.1)
      elif (percentage) > 5: # 10%
        list.append(0.05)
      else:
        list.append(0)
    return list
  product_data = df.groupby('Product')
  total_sales_product = product_data.sum()['Total sales']
  products = [prod for prod, df in product_data]
  overall_sales = df['Total sales'].sum()

  fig = plt.figure(figsize=(16,9))
  plt.pie(total_sales_product, labels=my_level_list(products, total_sales_product, overall_sales), autopct=my_autopct, explode=my_explode(products, total_sales_product, overall_sales))
  plt.title('Phần trăm tổng doanh thu của các sản phẩm', size=32)
  
  graph = StringIO()
  fig.savefig(graph, format='svg')
  graph.seek(0)
  data = graph.getvalue()
  
  return data

def get_quantity_total_sales_graph():
  product_data = df.groupby('Product')
  quantity_order = product_data.sum()['Quantity Ordered']
  total_sales_product = product_data.sum()['Total sales']
  products = [prod for prod, df in product_data]

  fig, ax1 = plt.subplots(figsize=(16,9))
  ax2 = ax1.twinx()
  ax1.bar(products, quantity_order, label='Số lượng sản phẩm đã bán', color=colors[0])
  ax2.plot(products, total_sales_product, color=colors[1], marker='o', markersize=5, linewidth=3, label='Tổng doanh thu')
  ax1.set_xlabel('Sản phẩm', size=16)
  ax1.set_ylabel('Số lượng', color=colors[0], size=16)
  ax1.set_xticklabels(products, rotation='vertical', size=10)
  ax2.set_ylabel('Doanh thu', color=colors[1], size=16)
  ax2.yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))
  plt.grid()

  plt.title('Số lượng đã bán và doanh thu từ sản phẩm', size=32)
  plt.tight_layout()
  
  graph = StringIO()
  fig.savefig(graph, format='svg')
  graph.seek(0)
  data = graph.getvalue()
  
  return data

def get_hourly_order_graph():
  count_by_hour = df.groupby('Order Hour').size().reset_index(name='Count')
  hours = [hour for hour, df in df.groupby('Order Hour')]

  fig = plt.figure(figsize=(16, 9))
  plt.plot(hours, df.groupby('Order Hour').count(), linewidth=5, marker='o')
  plt.title('Số lượng đơn đặt hàng theo giờ trong ngày', size=32)
  for x, y in zip(hours, count_by_hour['Count'].to_numpy()):
    plt.text(x, y, str(y), va='center', ha='center', size=14)
  plt.grid()
  plt.xticks(hours)
  plt.xlabel('Hour', size=16)
  plt.ylabel('Total sales', size=16)
  plt.tight_layout()

  graph = StringIO()
  fig.savefig(graph, format='svg')
  graph.seek(0)
  data = graph.getvalue()
  
  return data

def get_report_file():
  file_name = str(uuid.uuid4()) + '.pdf'
  file_name = os.path.join(settings.MEDIA_ROOT, 'reports', file_name)
  pdf = PdfPages(file_name)
  
  pdf.savefig(get_monthly_sales_graph(return_type='fig'))
  pdf.savefig(get_city_sales_graph(return_type='fig'))
  pdf.savefig(get_product_sold_together_graph_2(return_type='fig'))

  pdf.close()
  return file_name