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

    function isValid(row) {
        return $("#startDate").val() && $("#endDate").val() && startBeforeEnd()
    }

    function getIdFromRow(row) {
        return row.find("td:first").text()
    }

    function createBeerPub(row) {
        startDate = getStartDate()
        endDate = getEndDate()
        if (getIdFromRow(row) == -1) {
            return $.post($("#create-beer-pub-url").data('url'),
                { 'startDate' : startDate.toJSON(), 'endDate' : endDate.toJSON() },
                function(id) {
                    row.find("td:first").text(id)
                    var placeHolder = $("#catalogus-beer-pub-url-placeholder").data('placeholder')
                    var link = $("#catalogus-beerPub-url").data('url').replace(placeHolder, getIdFromRow(row))
                    row.find('td').eq(3).html("<a href=" + link + ">Catalogus</a>");
                  })    
        }
        else {
            return $.post($("#edit-beer-pub-url").data('url'),
                { 'id' : getIdFromRow(row), 'startDate' : startDate.toJSON(), 'endDate' : endDate.toJSON() })        
        }
        
    }

    function deleteBeerPub(row, deletedCallback) {
        if (getIdFromRow(row) == -1)
        { // We don't want a confirmation box when the beer pub does not exist yet
            deletedCallback($.post($("#delete-beer-pub-url").data('url'), { 'id' : getIdFromRow(row) }))
        }
        else
        {
            $("#confirmDeletion").modal("show")
                $("#confirmDeleteButton").off("click").click(function () {
                    deletedCallback($.post($("#delete-beer-pub-url").data('url'), { 'id' : getIdFromRow(row) }))
                    $("#confirmDeletion").modal("hide")
            })
        }
    }

    function onEdit(row) {
        makeColumnInput(row, 1, createDateInput.bind(null, 'startDate'));
        makeColumnInput(row, 2, createDateInput.bind(null, 'endDate'));
    }

    loadTable([createDateInput('startDate', ''), createDateInput('endDate', ''), ""],
              deleteBeerPub,
              isValid,
              createBeerPub,
              onEdit,
              null)
})