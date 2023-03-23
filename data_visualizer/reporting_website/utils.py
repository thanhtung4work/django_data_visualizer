import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pylab
from matplotlib.ticker import StrMethodFormatter
from django.core.files.storage import default_storage
import os
from django.http import HttpResponse
from io import StringIO

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
  print(df.head())

def get_monthly_sales_graph():
  months = range(1, 13)
  sales_by_month = df.groupby('Month').sum()

  response = HttpResponse(content_type="image/png")
  # create your image as usual, e.g. pylab.plot(...)
  
  fig = plt.figure(figsize=(16, 9))
  plt.bar(months, sales_by_month['Total sales'])
  plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))
  plt.title('Total sales for each month')
  plt.xticks(months)
  plt.xlabel('Month')
  plt.ylabel('Total sales')
  
  graph = StringIO()
  fig.savefig(graph, format='svg')
  graph.seek(0)
  data = graph.getvalue()
  
  return data
