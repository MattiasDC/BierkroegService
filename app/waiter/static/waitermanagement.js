$(document).ready(function(){

    function createWaiter(row) {
      name = $("#name").val()
      if (!hasData(row, "id")) {
        return $.post($("#create-waiter-url").data('url'),
          { 'name' : name },
          function(name) { row.data("id", name) })  
      }
    }

    function isValidWaiter(row) {
        return $("#name").val()
    }

    function deleteWaiter(row, ifSuccessful) {
    	if (hasData(row, "id"))
      {
        return $.post($("#delete-waiter-url").data('url'),
          { 'name' : row.data('id') })  
      }
    }
	  loadTable([createStringInput('name', "")],
              deleteWaiter,
              isValidWaiter,
              createWaiter,
              null,
              null)
})