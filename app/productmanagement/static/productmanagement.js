$(document).ready(function(){

    function getIdFromRow(row) {
      return row[0].getAttribute("data-id")
    }

    function createProduct(row) {
      name = $("#name").val()
      if (!row[0].hasAttribute("data-id")) {
        $.post($("#create-product-url").data('url'),
          { 'name' : name },
          function(id) {
            row[0].setAttribute("data-id", id)
          })  
      }
      else {
        $.post($("#edit-product-url").data('url'),
          { 'id' : getIdFromRow(row), 'name' : name })   
      }
    }

    function isValidProduct(row) {
        return true
    }

    function deleteProduct(row) {
    	if (row[0].hasAttribute("data-id"))
        $.post($("#delete-product-url").data('url'), { 'id' : getIdFromRow(row) })  
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