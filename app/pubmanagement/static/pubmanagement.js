$(document).ready(function(){
	$('[data-toggle="tooltip"]').tooltip()
	var actions = '<a class="add" title="Add" data-toggle="tooltip"><i class="material-icons">&#xE03B</i></a>' + 
	              '<a class="edit" title="Edit" data-toggle="tooltip"><i class="material-icons">&#xE254</i></a>' + 
                  '<a class="delete" title="Delete" data-toggle="tooltip"><i class="material-icons">&#xE872</i></a>'

	// Append table with add row form on add new button click
    $(".add-new").click(function(){
		$(this).attr("disabled", "disabled")
		var index = $("table tbody tr:last-child").index()
        var row = '<tr>' +
            '<td><input type="date" class="form-control" name="startDate" id="startDate"></td>' +
            '<td><input type="date" class="form-control" name="endDate" id="endDate"></td>' +
			'<td>' + actions + '</td>' +
        '</tr>'
    	$("table").append(row)		
		$("table tbody tr").eq(index + 1).find(".add, .edit").toggle()
        $('[data-toggle="tooltip"]').tooltip()
    })

    function getStartDate() {
    	return new Date($("#startDate").val())
    }

    function getEndDate() {
    	return new Date($("#endDate").val())
    }

    function startBeforeEnd() {
    	return getStartDate() < getEndDate()
    }

    function createBeerPub(startDate, endDate, row) {
    	if (!row[0].hasAttribute("data-id")) {
    		$.post($("#create-beerPub-url").data('url'),
    			{ 'startDate' : startDate.toJSON(), 'endDate' : endDate.toJSON() },
    			function(id) {
    				row[0].setAttribute("data-id", id)
	  			})	
    	}
    	else {
    		$.post($("#edit-beerPub-url").data('url'),
    			{ 'id' : row[0].getAttribute("data-id"), 'startDate' : startDate.toJSON(), 'endDate' : endDate.toJSON() })		
    	}
    	
    }

    function deleteBeerPub(row) {
    	$.post($("#delete-beerPub-url").data('url'), { 'id' : row[0].getAttribute("data-id") })	
    }

	// Add row on add button click
	$(document).on("click", ".add", function(){
		var hasErrors = false
		var input = $(this).parents("tr").find('input[type="date"]')
        input.each(function(){
			if(!$(this).val() || !startBeforeEnd()){
				$(this).addClass("error")
				hasErrors = true
			} else{
                $(this).removeClass("error")
            }
		})

		$(this).parents("tr").find(".error").first().focus()
		if(!hasErrors){
			createBeerPub(getStartDate(), getEndDate(), $(this).parents("tr"))
			input.each(function(){
				$(this).parent("td").html($(this).val())
			})			
			$(this).parents("tr").find(".add, .edit").toggle()
			$(".add-new").removeAttr("disabled")
		}		
    })

    // Edit row on edit button click
	$(document).on("click", ".edit", function(){		
        $(this).parents("tr").find("td:not(:last-child)").each(function(i){
        	var id = "startDate"
        	if (i == 1)
        		id = "endDate"
			$(this).html('<input type="Date" class="form-control" name="'+ id + '" id="' + id + '" value="' + $(this).text() + '">')
		})		
		$(this).parents("tr").find(".add, .edit").toggle()
		$(".add-new").attr("disabled", "disabled")
    })

	// Delete row on delete button click
	$(document).on("click", ".delete", function(){
		$(this).tooltip('hide')
        var row = $(this).parents("tr")
        deleteBeerPub(row)
        row.remove()
		$(".add-new").removeAttr("disabled")
    })

})