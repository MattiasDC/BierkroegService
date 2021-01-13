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

    function createDateInput(name, value) {
    	return '<input type="Date" class="form-control" name="' + name + '" id="' + name + '" value="' + value + '"/>'
    }

    function onEdit(row) {
    	row.find('td').eq(0).html(createDateInput('startDate', row.find('td').eq(0).text()));
        row.find('td').eq(1).html(createDateInput('endDate', row.find('td').eq(1).text()));
    }

	loadTable('<td>' + createDateInput('startDate', '') + '</td>' +
              '<td>' + createDateInput('endDate', '') + '</td>' +
              '<td></td>',
              deleteBeerPub,
              startBeforeEnd,
              createBeerPub,
              onEdit)
})