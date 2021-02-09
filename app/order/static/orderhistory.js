$(document).ready(function () {
    
    function deleteOrder(row, ifSuccessful) {
        return $.post($("#delete-order-url").data('url'), { 'id' : row.data('id') })  
    }

    loadTable([],
              deleteOrder,
              null,
              null,
              null,
              null)

    $("#btnNew").toggle()
    $(this).find(".edit").remove()
})