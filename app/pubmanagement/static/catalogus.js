$(document).ready(function(){

    function createBeerPubProduct(row) {
    }

    function isValidBeerPubProduct(row) {
      return $("#price").val() && $("#price").val() > 0 && $("#productDropDown").closest('td').data('product-id') != undefined
    }

    function deleteBeerPubProduct(row) {
    	
    }

    function onEdit(row) {
        var productName = row.find('td').eq(0).text()
        row.find('td').eq(0).html(createProductInput(products,
                                                     productName));
        $("#productDropDown").val(productName);
        makeColumnInput(row, 1, createFloatInput.bind(null, 'price'));
    }

    function createProductInput(products, initialButtonValue) {
      var input = `<div class="dropdown">
                      <button class="btn btn-secondary btn-block dropdown-toggle" style-width="100%"" type="button" id="productDropDown" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                       ` + initialButtonValue + 
                      `</button>
                      <div class="dropdown-menu" aria-labelledby="productDropDown">`

      var i
      for (i = 0; i < products.length; i++) {
        input +=     '<a class="dropdown-item" data-id=' + products[i].id + '>' + products[i].name + '</a>'
      } 

      input +=       `</div>
                   </div>
                   <script>
                      $(".dropdown-item").click(function(){
                       $("#productDropDown").html($(this).text());
                       $("#productDropDown").val($(this).text());
                       $("#productDropDown").closest('td').data('product-id', $(this).data('id'))
                      });
                   </script>`

      return input
    }

	  loadTable([createProductInput(products, "Product"), createFloatInput('price', "")],
              deleteBeerPubProduct,
              isValidBeerPubProduct,
              createBeerPubProduct,
              onEdit)
})