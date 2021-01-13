$(document).ready(function(){

    function createProduct(row) {
    }

    function isValidProduct(row) {
        return true
    }

    function deleteProduct(row) {
    	
    }

    function onEdit(row) {
        row.find('td').eq(1).html(createStringInput('name', row.find('td').eq(0).text()));
    }
    
	  loadTable('<td>' + createStringInput('name', "") + '</td>',
              deleteProduct,
              isValidProduct,
              createProduct,
              onEdit)
})