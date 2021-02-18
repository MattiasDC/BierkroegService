$(document).ready(function(){

    function createUser(row) {
      name = $("#name").val()
      return $.post($("#create-user-url").data('url'),
          { 'name' : name },
          function(name) {
            row.find("td:first").text(name)
            roles = row.find("td").slice(2,-1).each(function(i, e) {
              $(e).html("<div class=\"form-check\">\
                             <input class=\"form-check-input\" type=\"checkbox\">\
                         </div>")
            })
            registerClick()
          })
    }

    function isValidUser(row) {
        return $("#name").val()
    }

    function deleteUser(row, deletedCallback) {
      id = row.find("td:first").text()
      deletedCallback($.post($("#delete-user-url").data('url'), { 'name' : id }))
    }

    function registerClick() {
      $(".form-check-input").click(function() {
        $.post($("#set-role-url").data('url'), { 'name' : $(this).parents('tr').find('td:first').text(),
                                                 'role' : get_roles()[$(this).closest('td').index()-2],
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