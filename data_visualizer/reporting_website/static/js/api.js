$.ajax({
  async: false,
  type: 'GET',
  url: '/dummy_api?graph=monthly_sales_graph',
  dataType: "xml",
  success: (svg) => {
    $('#monthly-sales').html(svg.rootElement.outerHTML);
    console.log('done monthly')
  }
})
$.ajax({
  async: false,
  type: 'GET',
  url: '/dummy_api?graph=city_sales_graph',
  dataType: "xml",
  success: (svg) => {
    $('#city-sales').html(svg.rootElement.outerHTML);
    console.log('done city')
  }
})
$.ajax({
  async: false,
  type: 'GET',
  url: '/dummy_api?graph=product_sales_percentage_graph',
  dataType: "xml",
  success: (svg) => {
    $('#product_sales_percentage_graph').html(svg.rootElement.outerHTML);
    console.log('done city')
  }
})
$.ajax({
  async: false,
  type: 'GET',
  url: '/dummy_api?graph=product_sold_together_graph_2',
  dataType: "xml",
  success: (svg) => {
    $('#product_sold_together_graph_2').html(svg.rootElement.outerHTML);
    console.log('done city')
  }
})
$.ajax({
  async: false,
  type: 'GET',
  url: '/dummy_api?graph=quantity_total_sales_graph',
  dataType: "xml",
  success: (svg) => {
    $('#quantity_total_sales_graph').html(svg.rootElement.outerHTML);
    console.log('done city')
  }
})