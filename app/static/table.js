function loadTable(rowColumns, deleteFunction, validationFunction, createFunction, onEdit, afterAdd){
	$('[data-toggle="tooltip"]').tooltip()
	var actions = '<a class="add" title="Add" data-toggle="tooltip"><i class="material-icons">&#xE03B</i></a>' + 
	              '<a class="edit" title="Edit" data-toggle="tooltip"><i class="material-icons">&#xE254</i></a>' + 
                  '<a class="delete" title="Delete" data-toggle="tooltip"><i class="material-icons">&#xE872</i></a>'

    // Append table with add row form on add new button click
    $(".add-new").click(function(){
		var index = $("table tbody tr:last-child").index()
        var row = '<tr>' + wrapInTableColumns(rowColumns) + wrapInTableColumn(actions) + '</tr>'
    	$("table").append(row)		
		$("table tbody tr").eq(index + 1).find(".add, .edit").toggle()
        $('[data-toggle="tooltip"]').tooltip()
        if (afterAdd)
        	afterAdd()
        $("table tbody tr").eq(index + 1).children().first('td').children().first().focus()
    })

    function handleAdd() {
    	var hasErrors = false
		var row = $(this).parents('tr')
		var input = row.find('input').add(row.find('button'))

        input.each(function(){
			if(!validationFunction(row)){
				$(this).addClass("error")
				hasErrors = true
			} else{
                $(this).removeClass("error")
            }
		})

		row.find(".error").first().focus()
		if(!hasErrors){
			var create = createFunction(row)
            if (create)
                create.done(function () {
                                input.each(function(){
                                    $(this).closest("td").text($(this).val())
                                    $(this).remove()
                                })          
                                row.find(".add, .edit").toggle()
                            })
                      .fail(function (e) {
                        if (e.responseJSON) {
                          errorMessage = e.responseJSON.error
                          alertModal(errorMessage.substring(errorMessage.indexOf(":")))
                        }
                      })
		}
    }

	// Add row on add button click
	$(document).on("click", ".add", handleAdd)

    // Edit row on edit button click
	$(document).on("click", ".edit", function(){
		var row  = $(this).parents('tr')
		onEdit(row)
		row.find(".add, .edit").toggle()
    })

    // Delete row on delete button click
	$(document).on("click", ".delete", function(){
		$(this).tooltip('hide')
        var row = $(this).parents("tr")
        var del = deleteFunction(row)
        if (del)
        	del.done(function () {row.remove()})
           	   .fail(function (e) {
           	   	  if (e.responseJSON) {
           	   	  	errorMessage = e.responseJSON.error
            	  	alertModal(errorMessage.substring(errorMessage.indexOf(":")))
           	   	  }
            	})
        else
        	row.remove()
    })
}