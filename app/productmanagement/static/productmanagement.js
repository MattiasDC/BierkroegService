$(document).ready(function(){

    function createProduct(row) {
    }

    function isValidProduct(row) {
        return true
    }

    function deleteProduct(row) {
    	
    }

    function onEdit(row) {
        makeColumnInput(row, 0, createStringInput.bind(null, 'name'));
    }
    
	  loadTable([createStringInput('name', "")],
              deleteProduct,
              isValidProduct,
              createProduct,
              onEdit)
})