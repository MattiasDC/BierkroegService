$(document).ready(function(){

    function createBeerPubProduct(row) {
      var price = $("#price").val()
      var beerPubId = $("#beerPub-id").data('id')
      if (!hasData(row, "exists")) {
        $.post($("#create-beerPubProduct-url").data('url'),
          { 'price' : price, 'beerPubId' : beerPubId, 'productId' : row.data("product-id") },
          function() { row.data("exists", 'true') })  
      }
      else {
        $.post($("#edit-beerPubProduct-url").data('url'),
          { 'beerPubId' : beerPubId, 'productId' : row.data("product-id"), 'price' : price })   
      }
    }

    function isValidBeerPubProduct(row) {
      return $("#price").val() && $("#price").val() > 0 && hasData($("#productDropDown").closest('tr'), 'product-id')
    }

    function deleteBeerPubProduct(row) {
    	if (hasData(row, "product-id"))
      {
        var beerPubId = $("#beerPub-id").data('id')
        $.post($("#delete-beerPubProduct-url").data('url'), { 'productId' : row.data("product-id"),
                                                              'beerPubId' : beerPubId })  
      }
    }

    function onEdit(row) {
        var productName = row.find('td').eq(0).text()
        row.find('td').eq(0).html(createProductInput(productName));
        $("#productDropDown").val(productName);
        makeColumnInput(row, 1, createFloatInput.bind(null, 'price'));
    }

    function createProductInput(initialButtonValue) {
      return `<div class="dropdown">
                 <button class="btn btn-secondary btn-block dropdown-toggle text-left" style-width="100%"" type="button" id="productDropDown" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                  ` + initialButtonValue + 
                 `</button>
                 <div class="dropdown-menu" aria-labelledby="productDropDown"></div>
              </div>`
    }

    function fillDropDown() {
      $.getJSON($("#products-url").data('url'),
        function (productsString) {
          products = JSON.parse(productsString)
          var i
          for (i = 0; i < products.length; i++) {
            var ele = document.createElement("a");
            ele.classList = "dropdown-item";
            ele.innerText = products[i].name;
            ele.setAttribute("data-id", products[i].id)
            ele.addEventListener("click", function(e) {
              $("#productDropDown").html($(this).text());
              $("#productDropDown").val($(this).text());
              $("#productDropDown").closest('tr').data('product-id', $(this).data('id'))
            }, false);
            $(".dropdown-menu")[0].appendChild(ele)
          }
         })
    }

	  loadTable([createProductInput("Product"), createFloatInput('price', "")],
              deleteBeerPubProduct,
              isValidBeerPubProduct,
              createBeerPubProduct,
              onEdit,
              fillDropDown)
})