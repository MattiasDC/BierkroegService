$(document).ready(function(){

    function createUser(row) {
      name = $("#name").val()
      if (!hasData(row, "id")) {
        return $.post($("#create-user-url").data('url'),
          { 'name' : name },
          function(name) {
            row.data("id", name)
            roles = row.find("td").slice(1,-1).each(function(i, e) {
              $(e).html("<div class=\"form-check\">\
                             <input class=\"form-check-input\" type=\"checkbox\">\
                         </div>")
            })
            registerClick()
          })  
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

    function registerClick() {
      $(".form-check-input").click(function() {
        $.post($("#set-role-url").data('url'), { 'name' : $(this).parents('tr').data('id'),
                                                 'role' : get_roles()[$(this).closest('td').index()-1],
                                                 'enable' : $(this).is(':checked')})
       })
    }

	  loadTable([createStringInput('name', ""), "", ""],
              deleteUser,
              isValidUser,
              createUser,
              null,
              null)

    $(this).find(".edit").remove()
    registerClick()
    
})