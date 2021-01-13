$(document).ready(function(){
	function getStartDate() {
    	return new Date($("#startDate").val())
    }

    function getEndDate() {
    	return new Date($("#endDate").val())
    }

    function startBeforeEnd(row) {
    	return getStartDate() < getEndDate()
    }

    function getIdFromRow(row) {
    	return row[0].getAttribute("data-id")
    }

    function createBeerPub(row) {
    	startDate = getStartDate()
    	endDate = getEndDate()
    	if (!row[0].hasAttribute("data-id")) {
    		$.post($("#create-beerPub-url").data('url'),
    			{ 'startDate' : startDate.toJSON(), 'endDate' : endDate.toJSON() },
    			function(id) {
    				row[0].setAttribute("data-id", id)
    				var placeHolder = $("#catalogus-beerPub-url-placeholder").data('placeholder')
    				var link = $("#catalogus-beerPub-url").data('url').replace(placeHolder, getIdFromRow(row))
    				row.find('td').eq(2).html("<a href=" + link + ">Catalogus</a>");
	  			})	
    	}
    	else {
    		$.post($("#edit-beerPub-url").data('url'),
    			{ 'id' : getIdFromRow(row), 'startDate' : startDate.toJSON(), 'endDate' : endDate.toJSON() })		
    	}
    	
    }

    function deleteBeerPub(row) {
    	if (row[0].hasAttribute("data-id"))
    		$.post($("#delete-beerPub-url").data('url'), { 'id' : getIdFromRow(row) })	
    }

    function onEdit(row) {
    	makeColumnInput(row, 0, createDateInput.bind(null, 'startDate'));
        makeColumnInput(row, 1, createDateInput.bind(null, 'endDate'));
    }

	loadTable([createDateInput('startDate', ''), createDateInput('endDate', ''), ""],
              deleteBeerPub,
              startBeforeEnd,
              createBeerPub,
              onEdit)
})