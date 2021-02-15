$(document).ready(function(){

    function createProduct(row) {
      name = $("#name").val()
      idCol = row.find("td:first")
      id = idCol.text()
      if (id == -1) {
        return $.post($("#create-product-url").data('url'),
          { 'name' : name },
          function(id) { idCol.text(id) })  
      }
      else {
        return $.post($("#edit-product-url").data('url'),
          { 'id' : id, 'name' : name })   
      }
    }

    function isValidProduct(row) {
        return $("#name").val()
    }

    function deleteProduct(row, ifSuccessful) {
      id = row.find("td:first").text()
      return $.post($("#delete-product-url").data('url'), { 'id' : id })
    }

    function onEdit(row) {
        makeColumnInput(row, 1, createStringInput.bind(null, 'name'));
    }
    
      loadTable([createStringInput('name', "")],
              deleteProduct,
              isValidProduct,
              createProduct,
              onEdit,
              null)
})