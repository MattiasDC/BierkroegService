// A robust rounding algorithm (see https://stackoverflow.com/a/12830454 for issues with Math.round and float.toFixed)
function roundNumber(num, scale) {
  if (!("" + num).includes("e")) {
    return +(Math.round(num + "e+" + scale)  + "e-" + scale);
  } else {
    var arr = ("" + num).split("e");
    var sig = ""
    if (+arr[1] + scale > 0) {
      sig = "+";
    }
    return +(Math.round(+arr[0] + "e" + sig + (+arr[1] + scale)) + "e-" + scale);
  }
}

function addRowToOrder(productName, price, id) {
  var rowId = $("#order >tbody >tr").length;
  rowId = rowId + 1;
  
  var row = $('#order').bootstrapTable('getRowByUniqueId', id);
  if (row != null) {
  	row['amount'] += 1
  	$("#order").bootstrapTable('updateByUniqueId', {id: id, row: row});
    return;
  }
  $('#order').bootstrapTable('insertRow', {
    index: rowId,
    row: {"product":productName, "price":price, "id":id, "amount":1}
  });
};

function deleteRowFromOrder(id) {
  $('#order').bootstrapTable('remove', { field: 'id', values: [id] })
};

function amountButtonFormatter(value, row, index) {
    return [
      '<a class="decrement" href="javascript:void(0)" title="Decrement">',
      '<i class="glyphicon glyphicon-minus"></i>',
      '</a>',
      '&nbsp;' + row['amount'] + '&nbsp;',
      '<a class="increment" href="javascript:void(0)" title="Increment">',
      '<i class="glyphicon glyphicon-plus"></i>',
      '</a>'
    ].join('');
  };

function recalculateOrderSummary() {
	var data = $('#order').bootstrapTable('getData')
	var nofProducts = 0
	var totalPrice = 0
	for (index = 0; index < data.length; index++) {
		var amount = data[index]['amount']
		nofProducts += amount
		totalPrice += data[index]['price']*amount
	}

	$("#orderSummary").bootstrapTable('updateCell', {index: 0, field: 'nofProducts', value: nofProducts});
	$("#orderSummary").bootstrapTable('updateCell', {index: 0, field: 'totalPrice', value: roundNumber(totalPrice, 2)});

  $("#sendOrder").prop('disabled', totalPrice == 0)
}

window.operateEvents = {
    'click .increment': function (e, value, row, index) {
      $("#order").bootstrapTable('updateCell', {index: index, field: 'amount', value: row['amount'] + 1});
    },
    'click .decrement': function (e, value, row, index) {
      var amount = row['amount'];
      if (amount == 1) {
	    deleteRowFromOrder(row['id']);
	    return;
      }
      $("#order").bootstrapTable('updateCell', {index: index, field: 'amount', value: amount - 1});
    }
};

function initTable(table) {
    table = table.bootstrapTable('destroy').bootstrapTable({
      locale: "nl-NL",
      uniqueId: 'id',
      columns: [
        {
          title: 'Product',
          field: 'product',
          type: 'String'
        },
        {
          title: 'Prijs <span style="color:#808080">(€)</span>',
          field: 'price',
          type: 'Float'
        },
        {
          title: 'Aantal',
          field: 'amount',
          type: 'Number',
          visible: false
        },
        {
       	  title: 'Aantal',
          field: 'AmountEdit',
          events: window.operateEvents,
          formatter: amountButtonFormatter,
          width: '100px',
          align: 'center',
        },
        {
          title: 'Id',
          field: 'id',
          type: 'String',
          visible: false
        },],
        onPostBody: recalculateOrderSummary
    })
  }

$(document).ready(function(){
  // Filtering search list
  $("#productListInput").on("keyup", function(k) {
  	if (k.keyCode == 13)
  	{
  	var firstVisible = $('#productList').find('li:visible:first');
  	if (firstVisible.length == 0)
  		return;
  	addRowToOrder(firstVisible[0].dataset.product,
  				  parseFloat(firstVisible[0].dataset.price),
  				  firstVisible[0].dataset.id);
  	$(this).val('');
  	}
    var value = $(this).val().toLowerCase();
    $("#productList li").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
  });

  $("li").on("click",function() {
    addRowToOrder($(this)[0].dataset.product,
    			  parseFloat($(this)[0].dataset.price),
    			  $(this)[0].dataset.id)
  });

  initTable($("#order"));

  $("#sendOrder").prop('disabled', true)

  $("#confirmOrderButton").click(function() {
    var tableInput = $("#tableInput").val()
    if (!tableInput) {
      $("#tableInput").addClass("is-invalid")
      return
    }

    $("#tableInput").removeClass("is-invalid")
    $("#confirmOrder").modal("hide")
  })
});