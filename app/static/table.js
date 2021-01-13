function loadTable(rowColumns, deleteFunction, validationFunction, createFunction, onEdit){
	$('[data-toggle="tooltip"]').tooltip()
	var actions = '<a class="add" title="Add" data-toggle="tooltip"><i class="material-icons">&#xE03B</i></a>' + 
	              '<a class="edit" title="Edit" data-toggle="tooltip"><i class="material-icons">&#xE254</i></a>' + 
                  '<a class="delete" title="Delete" data-toggle="tooltip"><i class="material-icons">&#xE872</i></a>'


    // Append table with add row form on add new button click
    $(".add-new").click(function(){
		$(this).attr("disabled", "disabled")
		var index = $("table tbody tr:last-child").index()
        var row = '<tr>' + rowColumns + '<td>' + actions + '</td></tr>'
    	$("table").append(row)		
		$("table tbody tr").eq(index + 1).find(".add, .edit").toggle()
        $('[data-toggle="tooltip"]').tooltip()
    })

	// Add row on add button click
	$(document).on("click", ".add", function(){
		var hasErrors = false
		var row = $(this).parents('tr')
		var input = row.find('input')
        input.each(function(){
			if(!$(this).val() || !validationFunction(row)){
				$(this).addClass("error")
				hasErrors = true
			} else{
                $(this).removeClass("error")
            }
		})

		row.find(".error").first().focus()
		if(!hasErrors){
			createFunction(row)
			input.each(function(){
				$(this).parent("td").html($(this).val())
			})			
			row.find(".add, .edit").toggle()
			$(".add-new").removeAttr("disabled")
		}		
    })

    // Edit row on edit button click
	$(document).on("click", ".edit", function(){		
		var row  = $(this).parents('tr')
		onEdit(row)
		row.find(".add, .edit").toggle()
		$(".add-new").attr("disabled", "disabled")
    })

    // Delete row on delete button click
	$(document).on("click", ".delete", function(){
		$(this).tooltip('hide')
        var row = $(this).parents("tr")
        deleteFunction(row)
        row.remove()
		$(".add-new").removeAttr("disabled")
    })
}