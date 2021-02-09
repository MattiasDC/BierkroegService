$(document).ready(function(){

    function createProduct(row) {
      name = $("#name").val()
      if (!hasData(row,"id")) {
        return $.post($("#create-product-url").data('url'),
          { 'name' : name },
          function(id) { row.data("id", id) })  
      }
      else {
        return $.post($("#edit-product-url").data('url'),
          { 'id' : row.data('id'), 'name' : name })   
      }
    }

    function isValidProduct(row) {
        return $("#name").val()
    }

    function deleteProduct(row, ifSuccessful) {
        if (hasData(row, "id"))
      {
        return $.post($("#delete-product-url").data('url'),
          { 'id' : row.data('id') })  
      }
    }

    function onEdit(row) {
        makeColumnInput(row, 0, createStringInput.bind(null, 'name'));
    }
    
      loadTable([createStringInput('name', "")],
              deleteProduct,
              isValidProduct,
              createProduct,
              onEdit,
              null)
})