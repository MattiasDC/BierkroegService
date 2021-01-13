$(document).ready(function(){

    function createBeerPubProduct(row) {
    }

    function isValidBeerPubProduct(row) {
        return true
    }

    function deleteBeerPubProduct(row) {
    	
    }

    function onEdit(row) {
        row.find('td').eq(1).html('<input type="float" class="form-control" name="price" id="price" value="' + row.find('td').eq(1).text() + '">');
    }
    
	loadTable('<td></td>' + '<td><input type="float" class="form-control" name="price" id="price" value=""/>',
              deleteBeerPubProduct,
              isValidBeerPubProduct,
              createBeerPubProduct,
              onEdit)
})