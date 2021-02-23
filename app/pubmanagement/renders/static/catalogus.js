$(document).ready(function(){

    function createBeerPubProduct(row) {
      var price = $("#price").val()
      var beerPubId = $("#beerPub-id").data('id')
      var productId = row.find("td:first").text()
      var isEdit = row.data('isEdit')
      if (!isEdit) {
        return $.post($("#create-beerPubProduct-url").data('url'),
          { 'price' : price, 'beerPubId' : beerPubId, 'productId' : productId },
          function() { row.data("exists", 'true') })  
      }
      else {
        row.data("isEdit", false)
        return $.post($("#edit-beerPubProduct-url").data('url'),
          { 'beerPubId' : beerPubId, 'productId' : productId, 'price' : price })   
      }
    }

    function isValidBeerPubProduct(row) {
      return $("#price").val() && $("#price").val() > 0 && row.find("td:first").text() != -1
    }

    function deleteBeerPubProduct(row, deletedCallback) {
      var beerPubId = $("#beerPub-id").data('id')
      deletedCallback($.post($("#delete-beerPubProduct-url").data('url'),
                      { 'productId' : row.find("td:first").text(),
                        'beerPubId' : beerPubId }))
    }

    function onEdit(row) {
        row.data("isEdit", true)
        var productName = row.find('td').eq(1).text()
        row.find('td').eq(1).html(createProductInput(productName));
        $("#productDropDown").val(productName);
        makeColumnInput(row, 2, createFloatInput.bind(null, 'price'));
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
      $.getJSON($("#possible-products-url").data('url'),
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
              $("#productDropDown").closest('tr').find('td:first').text($(this).data('id'))
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