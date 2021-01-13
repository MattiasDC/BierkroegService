$(document).ready(function(){

    function createBeerPubProduct(row) {
    }

    function isValidBeerPubProduct(row) {
        return $("#price").val() > 0
    }

    function deleteBeerPubProduct(row) {
    	
    }

    function onEdit(row) {
        row.find('td').eq(1).html(createFloatInput('price', row.find('td').eq(1).text()));
    }
    
	  loadTable('<td></td>' + '<td>' + createFloatInput('price', "") + '<td/>',
              deleteBeerPubProduct,
              isValidBeerPubProduct,
              createBeerPubProduct,
              onEdit)
})