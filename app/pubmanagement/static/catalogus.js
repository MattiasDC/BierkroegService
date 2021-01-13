$(document).ready(function(){

    function createBeerPubProduct(row) {
    }

    function isValidBeerPubProduct(row) {
        return $("#price").val() > 0
    }

    function deleteBeerPubProduct(row) {
    	
    }

    function onEdit(row) {
        makeColumnInput(row, 1, createFloatInput.bind(null, 'price'));
    }
    
	  loadTable(["", createFloatInput('price', "")],
              deleteBeerPubProduct,
              isValidBeerPubProduct,
              createBeerPubProduct,
              onEdit)
})