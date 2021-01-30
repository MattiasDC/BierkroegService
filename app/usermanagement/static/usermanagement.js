$(document).ready(function(){

    function createUser(row) {
      name = $("#name").val()
      if (!hasData(row, "id")) {
        return $.post($("#create-user-url").data('url'),
          { 'name' : name },
          function(name) { row.data("id", name) })  
      }
    }

    function isValidUser(row) {
        return $("#name").val()
    }

    function deleteUser(row, ifSuccessful) {
    	if (hasData(row, "id"))
      {
        return $.post($("#delete-user-url").data('url'),
          { 'name' : row.data('id') })  
      }
    }
	  loadTable([createStringInput('name', "")],
              deleteUser,
              isValidUser,
              createUser,
              null,
              null)

    $(this).find(".edit").remove()
})