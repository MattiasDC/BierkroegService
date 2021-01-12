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
            '<td></td>' + 
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

    function getIdFromRow(row) {
    	return row[0].getAttribute("data-id")
    }

    function createBeerPub(startDate, endDate, row) {
    	if (!row[0].hasAttribute("data-id")) {
    		$.post($("#create-beerPub-url").data('url'),
    			{ 'startDate' : startDate.toJSON(), 'endDate' : endDate.toJSON() },
    			function(id) {
    				row[0].setAttribute("data-id", id)
    				var placeHolder = $("#manage-beerPub-url-placeholder").data('placeholder')
    				var link = $("#manage-beerPub-url").data('url').replace(placeHolder, getIdFromRow(row))
    				row.find('td').eq(2).html("<a href=" + link + ">Catalogus</a>");
	  			})	
    	}
    	else {
    		$.post($("#edit-beerPub-url").data('url'),
    			{ 'id' : getIdFromRow(row), 'startDate' : startDate.toJSON(), 'endDate' : endDate.toJSON() })		
    	}
    	
    }

    function deleteBeerPub(row) {
    	$.post($("#delete-beerPub-url").data('url'), { 'id' : getIdFromRow(row) })	
    }

	// Add row on add button click
	$(document).on("click", ".add", function(){
		var hasErrors = false
		var row = $(this).parents('tr')
		var input = row.find('input[type="date"]')
        input.each(function(){
			if(!$(this).val() || !startBeforeEnd()){
				$(this).addClass("error")
				hasErrors = true
			} else{
                $(this).removeClass("error")
            }
		})

		row.find(".error").first().focus()
		if(!hasErrors){
			createBeerPub(getStartDate(), getEndDate(), row)
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
		row.find('td').eq(0).html('<input type="Date" class="form-control" name="startDate" id="startDate" value="' + row.find('td').eq(0).text() + '">');
        row.find('td').eq(1).html('<input type="Date" class="form-control" name="endDate" id="endDate" value="' + row.find('td').eq(1).text() + '">');
		row.find(".add, .edit").toggle()
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